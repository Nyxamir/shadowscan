import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .collect import collect_snapshot
from .ports import parse_ports_csv, evaluate_port_alerts
from .report import default_report_path, write_report_json


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="shadowscan",
        description="Linux system audit tool (JSON output + saved reports + port alerts).",
    )
    p.add_argument("--json", action="store_true", help="Print JSON to stdout.")
    p.add_argument("--out", type=str, default="", help="Write report JSON to this file path.")
    p.add_argument(
        "--report-dir",
        type=str,
        default="",
        help="Directory to save timestamped report (if --out not provided).",
    )
    p.add_argument(
        "--alert-ports",
        type=str,
        default="22,23,80,443,445,3389,5432,6379,9200,27017,3306",
        help="Comma-separated port list to warn on if listening.",
    )
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    return p


def main() -> None:
    args = build_parser().parse_args()

    snapshot = collect_snapshot()
    alert_ports = parse_ports_csv(args.alert_ports)
    alerts = evaluate_port_alerts(snapshot.get("listening_ports", []), alert_ports)
    snapshot["alerts"] = alerts

    snapshot["meta"] = {
        "tool": "shadowscan",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": "1",
    }

    # Decide output path
    out_path: Path
    if args.out:
        out_path = Path(args.out).expanduser().resolve()
    else:
        report_dir = Path(args.report_dir).expanduser().resolve() if args.report_dir else None
        out_path = default_report_path(report_dir)

    # Always save a report file (pro-grade behavior)
    write_report_json(snapshot, out_path)

    # Optionally print JSON to stdout
    if args.json:
        indent = 2 if args.pretty else None
        print(json.dumps(snapshot, ensure_ascii=False, indent=indent))

    # Print a short human summary
    if alerts:
        print(f"[!] Alerts: {len(alerts)} important ports are listening.")
        for a in alerts[:10]:
            print(f"    - port {a['port']} ({a['proto']}): {a['reason']}")
    else:
        print("[+] No port alerts triggered.")

    print(f"[+] Report saved: {out_path}")
