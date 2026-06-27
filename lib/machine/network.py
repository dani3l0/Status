import os
from .utils import get


class Network:

    @staticmethod
    def get_net():
        interface = get_default_iface_name()
        if not interface:
            return {"interface": None, "speed": -1, "rx": 0, "tx": 0}

        iface_path = f"/sys/class/net/{interface}"

        try:
            rx = get(f"{iface_path}/statistics/rx_bytes", isint=True) or 0
            tx = get(f"{iface_path}/statistics/tx_bytes", isint=True) or 0
        except FileNotFoundError:
            rx = 0
            tx = 0

        try:
            speed = get(f"{iface_path}/speed", isint=True)
            if speed is None:
                speed = -1
        except (OSError, FileNotFoundError):
            speed = -1

        return {
            "interface": interface,
            "speed": speed,
            "rx": rx,
            "tx": tx
        }


def get_default_iface_name():
    """
    Try /proc/net/route first (standard Linux), then fall back to
    scanning /sys/class/net for the first up non-loopback interface
    (needed on Termux where /proc/net/route may be unreadable).
    """
    # Method 1: standard Linux route table
    try:
        with open("/proc/net/route") as f:
            for line in f.readlines():
                try:
                    iface, dest, _, flags, _, _, _, _, _, _, _ = line.strip().split()
                    if dest != '00000000' or not int(flags, 16) & 2:
                        continue
                    return iface
                except:
                    continue
    except (PermissionError, FileNotFoundError):
        pass

    # Method 2: Termux fallback — pick first UP, non-loopback interface
    net_dir = "/sys/class/net"
    preferred_prefixes = ["wlan", "rmnet", "eth", "usb"]
    candidates = []

    if os.path.exists(net_dir):
        for iface in os.listdir(net_dir):
            if iface == "lo":
                continue
            operstate_path = os.path.join(net_dir, iface, "operstate")
            try:
                state = open(operstate_path).read().strip()
            except:
                state = "unknown"
            # Accept "up" or "unknown" (some Android interfaces report unknown)
            if state in ("up", "unknown"):
                candidates.append(iface)

    # Prefer wlan > rmnet > eth > usb > anything else
    for prefix in preferred_prefixes:
        for iface in candidates:
            if iface.startswith(prefix):
                return iface

    return candidates[0] if candidates else None
