import json
from datetime import datetime, timezone
from pathlib import Path


def default_report_path(report_dir: Path | None = None) -> Path:
    base = report_dir if report_dir else Path.home() / ".shadowscan" / "reports"
    base.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return (base / f"report_{ts}.json").resolve()


def write_report_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
