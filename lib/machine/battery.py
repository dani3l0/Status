import os
from .utils import get, ls_glob, exists

class Battery:

    @staticmethod
    def get_usage():
        capacity_files = ls_glob("/sys/class/power_supply", "*/capacity")
        if not capacity_files:
            return None

        cap_file = capacity_files[0]
        battery_dir = os.path.dirname(cap_file)

        capacity = get(os.path.join(battery_dir, "capacity"), isint=True)
        if capacity is None:
            return None

        status = get(os.path.join(battery_dir, "status"))
        status = status.strip() if status else "Unknown"

        health = get(os.path.join(battery_dir, "health"))
        health = health.strip() if health else "Unknown"

        temp_raw = get(os.path.join(battery_dir, "temp"), isint=True)
        temp = None
        if temp_raw is not None:
            # Handle sysfs temperature format (tenths of degrees C or millidegrees C)
            if temp_raw > 1000:
                temp = temp_raw / 1000.0
            elif temp_raw > 100:
                temp = temp_raw / 10.0
            else:
                temp = temp_raw

        voltage_raw = get(os.path.join(battery_dir, "voltage_now"), isint=True)
        if voltage_raw is None:
            voltage_raw = get(os.path.join(battery_dir, "voltage_avg"), isint=True)
        
        voltage = None
        if voltage_raw is not None:
            # Convert microvolts or millivolts to Volts
            if voltage_raw > 100000:
                voltage = voltage_raw / 1000000.0
            else:
                voltage = voltage_raw / 1000.0

        return {
            "capacity": capacity,
            "status": status,
            "health": health,
            "temp": temp,
            "voltage": voltage
        }
