#!/usr/bin/env python3
"""Free preflight and balance guards for billed DataForSEO runs.

Both checks cost $0. Pattern adopted from DataForSEO's own Claude skills, which
make a free utility call to confirm connectivity before any paid work rather
than discovering a broken setup after the first billed call.

Free endpoints used (verified $0 in the account price table, 2026-09-17):
  GET /v3/appendix/user_data
  GET /v3/ai_optimization/llm_mentions/locations_and_languages
"""
import base64, hashlib, json, os, sys, time, urllib.error, urllib.request

BASE = "https://api.dataforseo.com"
USER_DATA = "/v3/appendix/user_data"
LLM_LOCATIONS = "/v3/ai_optimization/llm_mentions/locations_and_languages"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # dfs_guard sits next to this file
# Same file the MCP guard hook writes, so MCP and REST spend sit in one record.
VAULT_LOG = os.environ.get("DFS_GUARD_VAULT_LOG") or os.path.join(os.environ.get("DFS_BRAIN_VAULT") or os.path.join(os.path.expanduser("~"), "Documents", "DataForSEO Brain", "vault"), "_attachments", "dfs-calls.jsonl")


def credentials():
    """DATAFORSEO_LOGIN is the vendor-canonical name; USERNAME kept as alias."""
    login = os.environ.get("DATAFORSEO_LOGIN") or os.environ.get("DATAFORSEO_USERNAME")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        sys.exit("set DATAFORSEO_LOGIN (or DATAFORSEO_USERNAME) and DATAFORSEO_PASSWORD")
    return login, password


class Blocked(RuntimeError):
    """The guard refused a REST call before it was sent. Nothing was billed."""


class OutOfBalance(RuntimeError):
    """HTTP 402 / status 402xx: the balance is exhausted. Stop the run; retrying only repeats the failure."""


REPEAT_BLOCK_S = 3600
_run_spent = 0.0      # actual cost of REST calls made by this process


def run_cap():
    """Per-process ceiling in USD on actual REST spend (env DFS_RUN_CAP, default $2)."""
    try:
        return float(os.environ.get("DFS_RUN_CAP") or 2.0)
    except ValueError:
        return 2.0


def default_source():
    """parent/script.py, so a weekly rankings/rank_check.py is told apart from another rank_check.py."""
    arg = os.path.abspath(sys.argv[0]) if sys.argv and sys.argv[0] else "python"
    return os.environ.get("DFS_SOURCE") or "/".join(arg.replace("\\", "/").split("/")[-2:])


def call_hash(endpoint, payload):
    return hashlib.sha1((endpoint + json.dumps(payload, sort_keys=True, default=str)).encode()).hexdigest()[:16]


def recent_rest_hashes(now, window=REPEAT_BLOCK_S, max_lines=3000):
    try:
        with open(VAULT_LOG, encoding="utf-8") as f:
            lines = f.readlines()[-max_lines:]
    except OSError:
        return {}
    seen = {}
    for line in lines:
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("phase") == "rest" and r.get("hash") and now - r.get("t", 0) < window:
            seen[r["hash"]] = r.get("t", 0)
    return seen


def rest_guard(endpoint, payload, confirm_cost=False, allow_repeat=False, now=None):
    """The MCP guard's rules applied to a REST body. Returns the (possibly patched) payload or raises Blocked."""
    import dfs_guard as g   # same folder; imported late so dfs_safety stays usable on its own
    now = now or time.time()
    tasks = payload if isinstance(payload, list) else [payload]
    patched, est = [], 0.0
    for task in tasks:
        task = task if isinstance(task, dict) else {}
        ep = "api:" + endpoint
        decision, reason, patch = g.decide("api_request", {"path": endpoint, "data": [task]}, "rest", now, [])
        if decision == "deny":
            raise Blocked(f"{endpoint}: {reason} Nothing was billed.")
        if decision == "ask":
            if g.multiplier_warning(ep, task) and not confirm_cost:
                raise Blocked(f"{endpoint}: {reason} Pass confirm_cost=True to run it anyway. Nothing was billed.")
            print(f"dfs_safety: {endpoint}: {reason}", file=sys.stderr)
        if "depth" in patch and "depth" not in task:
            task = dict(task, depth=patch["depth"])   # API default is 100 results = 10 billed pages
        if "limit" in patch:   # billed per row; scripts may page on purpose, so warn rather than change it
            print(f"dfs_safety: {endpoint}: limit={task.get('limit', 'default 100')} rows are billed per row; "
                  f"the guard's cap for this endpoint is {patch['limit']}.", file=sys.stderr)
        patched.append(task)
        est += g.estimate(ep, task)
    body = patched if isinstance(payload, list) else patched[0]
    if not allow_repeat and not g.matches(endpoint, *g.AI_ANSWER_KEYS):
        h = call_hash(endpoint, body)
        if h in recent_rest_hashes(now):
            raise Blocked(f"Identical {endpoint} call made {int((now - recent_rest_hashes(now)[h]) // 60)} min ago. "
                          "Reuse that result, or pass allow_repeat=True. Nothing was billed.")
    if _run_spent + est > run_cap():
        raise Blocked(f"This run has spent ${_run_spent:.3f}; this call (~${est:.3f}) would pass the run cap "
                      f"${run_cap():.2f} (env DFS_RUN_CAP). Nothing was billed.")
    return body


def call(path, payload=None, timeout=60, source=None, confirm_cost=False, allow_repeat=False):
    """POST (or GET when payload is None) a /v3 path or full URL; billed calls are logged.

    POSTs go through the same rules as the MCP guard first (Blocked = refused, nothing billed):
    search operators and other price multipliers need confirm_cost=True; identical calls within an
    hour need allow_repeat=True; DFS_RUN_CAP caps the process's actual spend. HTTP 402 raises OutOfBalance."""
    global _run_spent
    login, password = credentials()
    token = base64.b64encode(f"{login}:{password}".encode()).decode()
    url = path if path.startswith("http") else BASE + "/v3/" + path.lstrip("/").removeprefix("v3/")   # "serp/..." once became host "api.dataforseo.comserp"
    url = url.rstrip("/")    # LLM Mentions v2 rejects a trailing slash
    endpoint = url.split("/v3/", 1)[-1]
    if payload is not None:
        payload = rest_guard(endpoint, payload, confirm_cost, allow_repeat)
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": f"Basic {token}", "Content-Type": "application/json"},
        method="POST" if payload is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 402:
            raise OutOfBalance("DataForSEO returned 402: the balance is exhausted. Top up, then rerun; "
                               "cached results are kept.") from exc
        raise
    if str(data.get("status_code", "")).startswith("402"):
        raise OutOfBalance(f"DataForSEO {data.get('status_code')} {data.get('status_message')}: balance exhausted.")
    if payload is not None:   # billing happens on POST; a GET task_get only repeats the task's cost (balance unchanged, 2026-10-12)
        _run_spent += float(data.get("cost") or 0)
        log_rest(url, payload, data, source)
    return data


def log_rest(url, payload, data, source=None):
    """Append a billed REST call to the vault call log. Unlike MCP results, REST
    responses carry the exact cost, so these lines are true spend, not estimates."""
    if not isinstance(data, dict) or not data.get("cost"):
        return   # free calls (user_data, locations) would only add noise
    endpoint = url.split("/v3/", 1)[-1]
    rec = {"phase": "rest", "t": time.time(), "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "source": source or default_source(), "endpoint": endpoint, "hash": call_hash(endpoint, payload),
           "tasks": len(payload) if isinstance(payload, list) else 0, "cost": data.get("cost"),
           "status": data.get("status_code"), "tasks_error": data.get("tasks_error")}
    try:
        if os.path.isdir(os.path.dirname(VAULT_LOG)):
            with open(VAULT_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError as exc:   # the result is already paid for; warn rather than lose it
        print(f"WARNING: could not log the call to {VAULT_LOG}: {exc}", file=sys.stderr)


def balance():
    """Account balance in USD. Free call. Returns None if unavailable."""
    try:
        data = call(USER_DATA)
    except (urllib.error.URLError, OSError) as exc:
        return None, f"could not reach {USER_DATA}: {exc}"
    if data.get("status_code") != 20000:
        return None, f"{data.get('status_code')} {data.get('status_message')}"
    try:
        money = data["tasks"][0]["result"][0]["money"]
        return float(money["balance"]), None
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        return None, f"unexpected user_data shape: {exc}"


def preflight(verbose=True):
    """Confirm credentials and the llm_mentions family respond. Free. Exits on failure."""
    try:
        data = call(LLM_LOCATIONS)
    except urllib.error.HTTPError as exc:
        sys.exit(f"PREFLIGHT FAILED: HTTP {exc.code} on {LLM_LOCATIONS}\n"
                 f"  check DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD. Nothing was billed.")
    except (urllib.error.URLError, OSError) as exc:
        sys.exit(f"PREFLIGHT FAILED: cannot reach the API ({exc}). Nothing was billed.")
    if data.get("status_code") != 20000:
        sys.exit(f"PREFLIGHT FAILED: {data.get('status_code')} {data.get('status_message')}\n"
                 f"  Nothing was billed.")
    if verbose:
        print(f"preflight ok ({LLM_LOCATIONS}, $0)")
    return True


def guard(estimate, max_spend, min_balance_multiple=2.0, verbose=True):
    """Hard-stop before any billed call.

    Refuses to run when the estimate exceeds max_spend, or when the balance
    would not comfortably cover it. Both checks are free.
    """
    if estimate > max_spend:
        sys.exit(f"ABORT: estimated ${estimate:.3f} exceeds --max-spend ${max_spend:.2f}. "
                 f"Nothing was billed.")
    bal, err = balance()
    if err:
        sys.exit(f"ABORT: could not verify balance ({err}). Nothing was billed.\n"
                 f"  Override with --skip-balance-check only if you accept the risk.")
    if verbose:
        print(f"balance ${bal:.2f} | estimate ${estimate:.3f} | cap ${max_spend:.2f}")
    if bal < estimate:
        sys.exit(f"ABORT: balance ${bal:.2f} is below the estimate ${estimate:.3f}. "
                 f"Nothing was billed.")
    if bal < estimate * min_balance_multiple:
        print(f"WARNING: balance ${bal:.2f} is under {min_balance_multiple}x the estimate.",
              file=sys.stderr)
    return bal


QUEUE_BATCH = 100   # task_post takes up to 100 tasks per POST


def task_key(task):
    return str(task.get("tag") or call_hash("", task))


def queue(post_path, get_path_fmt, tasks, ids_file, source=None, poll_s=30, timeout_s=1800, confirm_cost=False):
    """Run tasks on the Standard queue (about a third of the live price) and return {key: task}.

    Rerun-safe: task ids are saved to ids_file before polling and results to <ids_file>.results.json,
    so a crash or restart never pays for a task twice. key = the task's `tag` (set one) or a hash.
    get_path_fmt has one {} for the task id, e.g. "serp/google/organic/task_get/advanced/{}"."""
    ids_path = os.path.abspath(ids_file)
    res_path = ids_path + ".results.json"
    ids = _load_json(ids_path)
    results = _load_json(res_path)
    todo = [t for t in tasks if task_key(t) not in ids]
    for i in range(0, len(todo), QUEUE_BATCH):
        chunk = todo[i:i + QUEUE_BATCH]
        data = call(post_path, chunk, timeout=120, source=source, confirm_cost=confirm_cost)
        for task, t in zip(chunk, data.get("tasks") or []):
            if t.get("status_code") == 20100:
                ids[task_key(task)] = t["id"]
            else:
                print(f"dfs_safety.queue: task {task_key(task)} not queued: {t.get('status_code')} "
                      f"{t.get('status_message')}", file=sys.stderr)
        _save_json(ids_path, ids)
    deadline = time.time() + timeout_s
    while True:
        pending = [k for k in ids if k not in results]
        for k in pending:
            t = (call(get_path_fmt.format(ids[k]), source=source).get("tasks") or [{}])[0]
            if t.get("status_code") == 20000 and t.get("result") is not None:
                results[k] = t
        _save_json(res_path, results)
        pending = [k for k in ids if k not in results]
        if not pending or time.time() > deadline:
            if pending:
                print(f"dfs_safety.queue: {len(pending)} tasks still pending; rerun later to collect them (free).",
                      file=sys.stderr)
            return results
        time.sleep(poll_s)


def _load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f)
    os.replace(tmp, path)
