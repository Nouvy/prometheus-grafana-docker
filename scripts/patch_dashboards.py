"""
Patch automatique des dashboards Grafana.
Remplace ${DS_PROMETHEUS} par l'UID réel de la datasource Prometheus.
S'exécute au démarrage de la stack via docker compose.
"""
import urllib.request
import urllib.error
import json
import time
import base64
import os

GRAFANA     = os.getenv("GRAFANA_URL",      "http://grafana:3000")
GF_USER     = os.getenv("GF_ADMIN_USER",    "admin")
GF_PASS     = os.getenv("GF_ADMIN_PASSWORD","admin123")
DS_UID      = os.getenv("DS_UID",           "prometheus")
PLACEHOLDER = "${DS_PROMETHEUS}"

CREDS   = base64.b64encode(f"{GF_USER}:{GF_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {CREDS}", "Content-Type": "application/json"}

def api(method, path, data=None):
    url  = GRAFANA + path
    body = json.dumps(data).encode() if data else None
    req  = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

# ── Attendre que Grafana soit prêt ────────────────────────────────────────────
print("Waiting for Grafana...", flush=True)
for attempt in range(60):
    try:
        api("GET", "/api/health")
        print("Grafana is ready.", flush=True)
        break
    except Exception:
        time.sleep(2)
else:
    print("ERROR: Grafana did not start in time.", flush=True)
    exit(1)

# ── Récupérer tous les dashboards ─────────────────────────────────────────────
dashboards = api("GET", "/api/search?type=dash-db")
print(f"Found {len(dashboards)} dashboard(s).", flush=True)

patched_count = 0
for d in dashboards:
    uid  = d["uid"]
    resp = api("GET", f"/api/dashboards/uid/{uid}")
    dashboard   = resp["dashboard"]
    serialized  = json.dumps(dashboard)

    if PLACEHOLDER in serialized:
        print(f"  Patching: {d['title']} ({uid})", flush=True)
        patched = json.loads(serialized.replace(PLACEHOLDER, DS_UID))
        api("POST", "/api/dashboards/db", {
            "dashboard": patched,
            "overwrite": True,
            "folderId":  0,
        })
        print(f"  ✓ Done", flush=True)
        patched_count += 1

print(f"\n{patched_count} dashboard(s) patched.", flush=True)
