# N Y X A M I R — ShadowScan

> 🦇 A minimal, defensive Linux audit tool — JSON output, saved reports, and port alerts.  
**GitHub:** @Nyxamir

## What it does (v0.1.0)
- Collects basic Linux system info (host/kernel/arch/python)
- Reads uptime and logged-in users
- Lists listening ports (TCP/UDP) using `ss`
- Generates a JSON report and saves it with a timestamp
- Raises alerts if “sensitive” ports are listening (customizable)

> This project is for **system auditing & monitoring** on machines you own/control.

## Install (local / dev)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
Print JSON to stdout (also saves a report automatically):
```bash
shadowscan --json --pretty
```

Save to a custom file:
```bash
shadowscan --out ./report.json --json --pretty
```

Customize alert ports:
```bash
shadowscan --alert-ports 22,80,443,5432,6379 --json
```

Default report location:
- `~/.shadowscan/reports/`

## Example output (high-level)
```json
{
  "system": {"hostname": "...", "os": "Linux", "kernel": "..."},
  "uptime_seconds": 12345,
  "logged_in_users": [],
  "listening_ports": [{"proto":"tcp","port":22,"local":"0.0.0.0:22","process":"..."}],
  "alerts": [{"port":22,"proto":"tcp","reason":"Port is in alert list and is listening"}],
  "meta": {"tool":"shadowscan","generated_at":"...","schema_version":"1"}
}
```

## Roadmap
- Add `pytest` tests
- GitHub Actions CI (lint + tests)
- Config file support (YAML/JSON) for alert rules
- Optional output formats (summary table)

## License
MIT
