import re
import subprocess
from typing import Iterable


def _run(cmd: list[str]) -> str:
    cp = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return (cp.stdout or "").strip()


def get_listening_ports() -> list[dict]:
    """Best-effort listener listing using `ss` (Linux)."""
    out = _run(["ss", "-lntuap"])
    lines = out.splitlines()

    ports: list[dict] = []
    for line in lines:
        if not line or line.startswith("Netid") or line.startswith("State"):
            continue

        parts = re.split(r"\s+", line, maxsplit=6)
        if len(parts) < 5:
            continue

        proto = parts[0].lower()
        local = parts[4]
        proc = parts[6] if len(parts) >= 7 else ""

        m = re.search(r":(\d+)$", local)
        if not m:
            continue
        port = int(m.group(1))

        ports.append(
            {
                "proto": proto,
                "port": port,
                "local": local,
                "process": proc,
            }
        )
    return ports


def parse_ports_csv(s: str) -> set[int]:
    ports: set[int] = set()
    for chunk in (c.strip() for c in s.split(",")):
        if not chunk:
            continue
        if chunk.isdigit():
            p = int(chunk)
            if 1 <= p <= 65535:
                ports.add(p)
    return ports


def evaluate_port_alerts(listening_ports: Iterable[dict], alert_ports: set[int]) -> list[dict]:
    alerts: list[dict] = []
    for p in listening_ports:
        port = int(p.get("port", -1))
        proto = str(p.get("proto", ""))
        if port in alert_ports:
            alerts.append(
                {
                    "port": port,
                    "proto": proto,
                    "reason": "Port is in alert list and is listening",
                    "local": p.get("local", ""),
                    "process": p.get("process", ""),
                }
            )
    return sorted(alerts, key=lambda x: (x["port"], x["proto"]))
