from flask import Flask, jsonify
import psutil
import platform
import os
import time

psutil.cpu_percent(interval=None)

app = Flask(__name__)


def format_uptime(seconds):
    seconds = int(time.time() - seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days}d {hours}h {minutes}m"


def get_system_info():
    try:
        temps = (psutil.sensors_temperatures(),)
        cpu_temp = temps["coretemp"][0].current if "coretemp" in temps else None
    except Exception:
        cpu_temp = None
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
        "os": platform.system(),
        "os_version": platform.version(),
        "hostname": platform.node(),
        "load_avg": os.getloadavg(),
        "uptime": format_uptime(psutil.boot_time()),
        "cpu_temp": cpu_temp,
    }


@app.route("/api/system", methods=["GET"])
def system_data():
    return jsonify(get_system_info())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
