# Stack de supervision — Prometheus + Grafana

## Démarrage rapide

```bash
docker compose up -d
```

| Service | URL | Accès |
|---------|-----|-------|
| Grafana | http://localhost:3000 | admin / admin123 |
| Prometheus | http://localhost:9090 | — |
| Alertmanager | http://localhost:9093 | — |
| cAdvisor | http://localhost:8080 | — |

## Structure

```
supervision/
├── docker-compose.yml
├── prometheus/
│   ├── prometheus.yml          ← Cibles de scrape
│   ├── alertmanager.yml        ← Config emails alertes
│   └── rules/
│       └── alerts.yml          ← Règles d'alertes
├── grafana/
│   └── provisioning/
│       ├── datasources/        ← Prometheus auto-configuré
│       └── dashboards/
├── blackbox/
│   └── blackbox.yml            ← Sondes HTTP/TCP/ICMP/DNS
└── snmp-exporter/
    └── snmp.yml                ← Config équipements réseau SNMP
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
