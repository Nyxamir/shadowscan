import platform
import subprocess


def _run(cmd: list[str]) -> str:
    cp = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return (cp.stdout or "").strip()


def get_basic_system_info() -> dict:
    return {
        "hostname": platform.node(),
        "os": platform.system(),
        "kernel": platform.release(),
        "arch": platform.machine(),
        "python": platform.python_version(),
    }


def get_uptime_seconds() -> int:
    try:
        with open("/proc/uptime", "r", encoding="utf-8") as f:
            first = f.read().split()[0]
            return int(float(first))
    except Exception:
        return -1


def get_logged_in_users() -> list[dict]:
    out = _run(["who"])
    users: list[dict] = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            users.append({"user": parts[0], "tty": parts[1], "raw": line})
    return users
