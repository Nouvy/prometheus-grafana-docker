# Stack de supervision — Prometheus + Grafana

## Démarrage rapide

```bash
docker compose up -d
```

| Service | URL | Accès |
|---------|-----|-------|
| Grafana | http://localhost:3000 | admin / admin123 |
| Prometheus | non exposé — accès via Grafana | — |
| Alertmanager | non exposé — accès via Grafana | — |
| cAdvisor | non exposé — accès via Grafana | — |

## Structure

```
prometheus-grafana-docker/
├── docker-compose.yml
├── prometheus/
│   ├── prometheus.yml          ← Cibles de scrape
│   ├── alertmanager.yml        ← Config emails alertes
│   └── rules/
│       └── alerts.yml          ← Règles d'alertes
├── grafana/
│   └── provisioning/
│       ├── datasources/        ← Prometheus auto-configuré (uid: prometheus)
│       └── dashboards/
├── blackbox/
│   └── blackbox.yml            ← Sondes HTTP/TCP/ICMP/DNS
├── snmp-exporter/
│   └── snmp.yml                ← Config équipements réseau SNMP
└── scripts/
    └── patch_dashboards.py     ← Patch automatique des dashboards importés
```

## Patch automatique des dashboards — ${DS_PROMETHEUS}

Certains dashboards communautaires (ex: Windows Exporter, Node Exporter) utilisent
`${DS_PROMETHEUS}` comme référence à la datasource. Sans correction, Grafana affiche
`Datasource ${DS_PROMETHEUS} was not found`.

Le service `grafana-init` corrige automatiquement ce problème au démarrage :
il parcourt tous les dashboards importés et remplace `${DS_PROMETHEUS}` par l'UID
réel de la datasource (`prometheus`).

```bash
# S'exécute automatiquement au démarrage
docker compose up -d

# Après avoir importé un nouveau dashboard manuellement
docker compose run --rm grafana-init
```

## Agents à installer sur les machines supervisées

### Linux / macOS — node_exporter (port 9100)
```bash
# Linux
wget https://github.com/prometheus/node_exporter/releases/latest/download/node_exporter-1.8.2.linux-amd64.tar.gz
tar xvf node_exporter-*.tar.gz && sudo cp node_exporter-*/node_exporter /usr/local/bin/

# macOS
brew install node_exporter && brew services start node_exporter
```

### Windows — windows_exporter (port 9182)
Télécharger le MSI : https://github.com/prometheus-community/windows_exporter/releases
```powershell
msiexec /i windows_exporter-x.x.x-amd64.msi ENABLED_COLLECTORS="cpu,cs,logical_disk,memory,net,os,service,system" /quiet
```

## Dashboards Grafana à importer (Dashboards → Import)

| ID | Dashboard |
|----|-----------|
| 1860 | Node Exporter Full (Linux/macOS) |
| 10467 | Windows Exporter |
| 7249 | SNMP Exporter |
| 13659 | Blackbox Exporter |
| 193 | Docker & cAdvisor |

## Recharger la config Prometheus sans redémarrage

```bash
curl -X POST http://localhost:9090/-/reload
```
