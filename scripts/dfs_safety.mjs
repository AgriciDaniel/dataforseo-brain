// Guarded DataForSEO calls for Node scripts: every request goes through the Python dfs_safety.call
// (guard rules, run cap, stop on 402, exact-cost logging with a source tag) via dfs_bridge.py.
//
//   import { dfsCall, closeDfs } from "<home>/.claude/skills/dataforseo-brain/scripts/dfs_safety.mjs";
//   const data = await dfsCall("serp/google/organic/live/advanced", [{ keyword: "x", location_code: 2840 }],
//                              { source: "my-script" });
//   closeDfs();
//
// A blocked call or an exhausted balance throws DfsStop: nothing was billed, so stop the run, don't retry.
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const BRIDGE = join(dirname(fileURLToPath(import.meta.url)), "dfs_bridge.py");

export class DfsStop extends Error {
  constructor(kind, message) {
    super(message);
    this.name = "DfsStop";
    this.kind = kind;
  }
}

let child = null;
let nextId = 1;
const pending = new Map();

function bridge() {
  if (child) return child;
  child = spawn(process.env.DFS_PYTHON || "python", [BRIDGE], { stdio: ["pipe", "pipe", "inherit"] });
  createInterface({ input: child.stdout }).on("line", (line) => {
    const reply = JSON.parse(line);
    const waiter = pending.get(reply.id);
    if (!waiter) return;
    pending.delete(reply.id);
    if (reply.ok) waiter.resolve(reply.data);
    else if (reply.kind === "blocked" || reply.kind === "out_of_balance") waiter.reject(new DfsStop(reply.kind, reply.error));
    else waiter.reject(new Error(reply.error));
  });
  child.on("exit", (code) => {
    for (const w of pending.values()) w.reject(new Error(`dfs_bridge exited (${code})`));
    pending.clear();
    child = null;
  });
  return child;
}

export function dfsCall(path, payload = null, { source, confirmCost = false, allowRepeat = false, timeout = 120 } = {}) {
  const id = nextId++;
  const req = { id, path, payload, source, confirm_cost: confirmCost, allow_repeat: allowRepeat, timeout };
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
    bridge().stdin.write(JSON.stringify(req) + "\n");
  });
}

export function closeDfs() {
  if (child) child.stdin.end();
}
