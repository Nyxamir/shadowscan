from .ports import get_listening_ports
from .utils import get_basic_system_info, get_uptime_seconds, get_logged_in_users


def collect_snapshot() -> dict:
    system = get_basic_system_info()
    uptime = get_uptime_seconds()
    users = get_logged_in_users()
    ports = get_listening_ports()

    return {
        "system": system,
        "uptime_seconds": uptime,
        "logged_in_users": users,
        "listening_ports": ports,
    }
