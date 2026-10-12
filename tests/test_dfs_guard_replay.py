import json, os, subprocess, sys, tempfile, collections, importlib.util, datetime

HOOK = os.environ.get('DFS_GUARD_PATH') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'dfs_guard.py')
tmp = tempfile.mkdtemp()
os.environ['DFS_GUARD_STATE'] = tmp
os.environ['DFS_GUARD_VAULT_LOG'] = os.path.join(tmp, 'vault.jsonl')
spec = importlib.util.spec_from_file_location('g', HOOK)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
C = 'mcp__dataforseo__'


def d(tool, inp, log=(), session='s1', now=1e9):
    return g.decide(tool, inp, session, now, list(log))[0]


cases = [
    ('google ads 9 kw -> deny', d(C + 'kw_data_google_ads_search_volume', {'keywords': ['a'] * 9, 'location_name': 'Canada'}), 'deny'),
    ('google ads 800 kw -> allow', d(C + 'kw_data_google_ads_search_volume', {'keywords': [str(i) for i in range(800)], 'location_name': 'Canada'}), 'allow'),
    ('labs overview 9 kw -> allow', d(C + 'dataforseo_labs_google_keyword_overview', {'keywords': ['a'] * 9}), 'allow'),
    ('ranked_keywords no limit -> modify', d(C + 'dataforseo_labs_google_ranked_keywords', {'target': 'x.com'}), 'modify'),
    ('ranked_keywords limit 100 -> modify', d(C + 'dataforseo_labs_google_ranked_keywords', {'target': 'x.com', 'limit': 100}), 'modify'),
    ('ranked_keywords limit 20 -> allow', d(C + 'dataforseo_labs_google_ranked_keywords', {'target': 'x.com', 'limit': 20}), 'allow'),
    ('targets as string -> deny', d(C + 'backlinks_bulk_referring_domains', {'targets': '["a.com"]'}), 'deny'),
    ('limit as string -> deny', d(C + 'business_data_business_listings_search', {'limit': '5', 'location_coordinate': '1,2,3'}), 'deny'),
    ('serp no depth -> modify', d(C + 'serp_organic_live_advanced', {'keyword': 'k', 'language_code': 'en'}), 'modify'),
    ('serp depth 100 -> ask', d(C + 'serp_organic_live_advanced', {'keyword': 'k', 'depth': 100}), 'ask'),
    ('serp depth 10 -> allow', d(C + 'serp_organic_live_advanced', {'keyword': 'k', 'depth': 10}), 'allow'),
    ('llm_response -> ask', d(C + 'ai_optimization_llm_response', {'llm_type': 'chat_gpt', 'user_prompt': 'q'}), 'ask'),
    ('chatgpt scraper -> allow', d(C + 'ai_optimization_chat_gpt_scraper', {'keyword': 'q', 'location_name': 'Canada'}), 'allow'),
    ('llm mentions -> ask', d(C + 'ai_opt_llm_ment_agg_metrics', {'target': [{'domain': 'x.com'}]}), 'ask'),
    ('api_request google ads small -> deny', d('mcp__dataforseo__api_request', {'path': '/v3/keywords_data/google_ads/search_volume/live', 'data': [{'keywords': ['a', 'b']}]}), 'deny'),
    ('api_request llm_responses -> ask', d('mcp__dataforseo__api_request', {'path': '/v3/ai_optimization/chat_gpt/llm_responses/live', 'data': {'user_prompt': 'q'}}), 'ask'),
    ('docs_search -> allow', d('mcp__dataforseo__docs_search', {'url': 'x'}), 'allow'),
    ('backlinks_summary -> allow', d(C + 'backlinks_summary', {'target': 'x.com'}), 'allow'),
]
ep, p = 'backlinks_summary', {'target': 'x.com'}
h = g.call_hash(ep, p)
cases += [
    ('repeat within 1h -> deny', d(C + ep, p, [{'phase': 'pre', 'hash': h, 't': 1e9 - 600, 'session': 'sX'}]), 'deny'),
    ('repeat after 5h -> ask', d(C + ep, p, [{'phase': 'pre', 'hash': h, 't': 1e9 - 5 * 3600, 'session': 'sX'}]), 'ask'),
    ('11th Google Ads call in a minute -> deny', d(C + 'kw_data_google_ads_search_volume', {'keywords': [str(i) for i in range(800)]}, [{'phase': 'pre', 'hash': str(i), 't': 1e9 - 5, 'session': 's1', 'endpoint': 'kw_data_google_ads_search_volume', 'est': 0.0} for i in range(10)]), 'deny'),
    ('31st other call in a minute -> deny', d(C + 'backlinks_summary', {'target': 'new.com'}, [{'phase': 'pre', 'hash': str(i), 't': 1e9 - 5, 'session': 's2', 'endpoint': 'backlinks_summary', 'est': 0.0} for i in range(30)]), 'deny'),
    ('session crosses $0.50 -> ask', d(C + 'backlinks_summary', {'target': 'y.com'}, [{'phase': 'pre', 'hash': 'z', 't': 1e9 - 4000, 'session': 's1', 'est': 0.49}]), 'ask'),
]
bad = [(n, got, exp) for n, got, exp in cases if got != exp]
print(f'unit cases: {len(cases) - len(bad)}/{len(cases)} pass', bad or '')

r = subprocess.run([sys.executable, HOOK, 'pre'], input=json.dumps({'tool_name': C + 'kw_data_google_ads_search_volume', 'tool_input': {'keywords': ['a', 'b']}, 'session_id': 'e2e'}), capture_output=True, text=True)
out = json.loads(r.stdout)
print('e2e deny JSON ok:', out['hookSpecificOutput']['permissionDecision'] == 'deny', '| exit', r.returncode)
r = subprocess.run([sys.executable, HOOK, 'pre'], input=json.dumps({'tool_name': C + 'backlinks_summary', 'tool_input': {'target': 'e2e.com'}, 'session_id': 'e2e'}), capture_output=True, text=True)
print('e2e allow: empty stdout', r.stdout == '', '| exit', r.returncode)
r = subprocess.run([sys.executable, HOOK, 'post'], input=json.dumps({'tool_name': C + 'backlinks_summary', 'tool_input': {'target': 'e2e.com'}, 'session_id': 'e2e', 'tool_response': {'ok': 1}}), capture_output=True, text=True)
print('e2e post logged:', sum(1 for _ in open(os.path.join(tmp, 'calls.jsonl'))), 'lines; vault copy:', os.path.exists(os.path.join(tmp, 'vault.jsonl')))
r = subprocess.run([sys.executable, HOOK, 'pre'], input='not json', capture_output=True, text=True)
print('bad stdin -> exit', r.returncode, 'stdout', repr(r.stdout))

rows = json.load(open(os.environ['DFS_CALLS_JSON'])) if os.environ.get('DFS_CALLS_JSON') else []
log, dec, why = [], collections.Counter(), collections.Counter()
for row in rows:
    if row['tool'].startswith('REST:'):
        continue
    tool = ('mcp__dataforseo__' if row['tool'] in ('api_request', 'docs_search', 'docs_index') else C) + row['tool']
    t = datetime.datetime.fromisoformat(row['ts'].replace('Z', '+00:00')).timestamp()
    decision, reason, _ = g.decide(tool, row['input'], row['sess'], t, log)
    dec[decision] += 1
    if decision != 'allow':
        why[decision + ': ' + reason[:75]] += 1
    if decision != 'deny':
        e = g.endpoint_of(tool, row['input'])
        pl = g.payload(tool, row['input'])
        log.append({'phase': 'pre', 't': t, 'session': row['sess'], 'endpoint': e, 'hash': g.call_hash(e, pl), 'est': g.estimate(e, pl)})
print('replay of', sum(dec.values()), 'real calls:', dict(dec))
for k, v in why.most_common(14):
    print(f'   {v:4d}  {k}')

# updatedInput shape, through stdin like Claude Code
r = subprocess.run([sys.executable, HOOK, 'pre'], input=json.dumps({'tool_name': C + 'dataforseo_labs_google_ranked_keywords', 'tool_input': {'target': 'z.com', 'limit': 1000}, 'session_id': 'e2e2'}), capture_output=True, text=True)
o = json.loads(r.stdout)['hookSpecificOutput']; print('e2e clamp:', o['permissionDecision'], o['updatedInput'])
r = subprocess.run([sys.executable, HOOK, 'pre'], input=json.dumps({'tool_name': 'mcp__dataforseo__api_request', 'tool_input': {'method': 'POST', 'path': '/v3/dataforseo_labs/google/ranked_keywords/live', 'data': [{'target': 'z.com'}]}, 'session_id': 'e2e3'}), capture_output=True, text=True)
o = json.loads(r.stdout)['hookSpecificOutput']; print('e2e api_request clamp:', o['permissionDecision'], o['updatedInput'])
