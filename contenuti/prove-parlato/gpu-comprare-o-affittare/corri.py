import json, os, sys, time, pathlib, urllib.request, concurrent.futures as cf
S = pathlib.Path(sys.argv[1]); modelli = sys.argv[2:]
prompt = (S/"prompt.md").read_text()
def chiama(m):
    t = time.time()
    req = urllib.request.Request("https://api.poe.com/v1/chat/completions",
        data=json.dumps({"model": m, "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Authorization": "Bearer " + os.environ["POE_API_KEY"], "Content-Type": "application/json"})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=600))
        testo = d["choices"][0]["message"]["content"]; u = d.get("usage")
    except Exception as e:
        testo, u = f"ERRORE: {e} {getattr(e,'read',lambda:b'')()[:300]}", None
    (S/f"out-{m}.md").write_text(testo)
    return m, round(time.time()-t), u and u.get("total_tokens"), len(testo.split())
with cf.ThreadPoolExecutor(12) as ex:
    for r in ex.map(chiama, modelli): print(*r)
