# from flask import Flask, jsonify
# from flask_cors import CORS

# import psutil
# import socket
# import requests

# import platform
# import os
# import time

# psutil.cpu_percent(interval=None)

# app = Flask(__name__)
# CORS(app)


# def format_uptime(seconds):
#     seconds = int(time.time() - seconds)
#     days, seconds = divmod(seconds, 86400)
#     hours, seconds = divmod(seconds, 3600)
#     minutes, seconds = divmod(seconds, 60)
#     return f"{days}d {hours}h {minutes}m"

# def get_ip_locale():
#     try:
#         s.connect(("8.8.8.8", 80))
#         return s.getsockname()[0]
#     except Exception:
#         return "127.0.0.1"
#     finally:
#         s.close()

# def get_system_info():
#     try:
#         temps = psutil.sensors_temperatures()
#         cpu_temp = temps["coretemp"][0].current if "coretemp" in temps else None
    
#     except Exception:
#         cpu_temp = None

#         # Rete istantanea: byte totali in/out
#         net_io = psutil.net_io_counters()
#         bytes_sent = net_io.bytes_sent
#         bytes_recv = net_io.bytes_recv
        
#     return {
#         "cpu_percent": psutil.cpu_percent(interval=1),
#         "cpu_cores": psutil.cpu_count(logical=False),
#         "cpu_threads": psutil.cpu_count(logical=True),
#         "memory": psutil.virtual_memory()._asdict(),
#         "disk": psutil.disk_usage("/")._asdict(),
#         "os": platform.system(),
#         "os_version": platform.version(),
#         "hostname": platform.node(),
#         "load_avg": os.getloadavg(),
#         "uptime": format_uptime(psutil.boot_time()),
#         "cpu_temp": cpu_temp,
#         "ip_interno": get_ip_locale(),
#         "ip_esterno": requests.get('https://api.ipify.org').text,
#         "network_bytes_sent": bytes_sent,
#         "network_bytes_recv": bytes_recv,
#     }


# @app.route("/api/system", methods=["GET"])
# def system_data():
#     return jsonify(get_system_info())


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


from flask import Flask, jsonify
from flask_cors import CORS

import psutil
import socket
import requests

import platform
import os
import time

app = Flask(__name__)
CORS(app)

def format_uptime(boot_time):
    seconds = int(time.time() - boot_time)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days}d {hours}h {minutes}m"

def format_bytes(size):
    # Formatta bytes in KB, MB, GB, TB
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def get_ip_locale():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

def get_system_info():
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps["coretemp"][0].current if "coretemp" in temps else None
    except Exception:
        cpu_temp = None

    # CPU% istantanea (non blocca)
    cpu_percent = psutil.cpu_percent(interval=None)
    # Memoria aggiornata
    memory = psutil.virtual_memory()._asdict()
    # Disco (spazio usato e libero)
    disk = psutil.disk_usage("/")._asdict()
    # Rete byte inviati e ricevuti
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv

    boot_time = psutil.boot_time()

    return {
        "cpu_percent": cpu_percent,
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "memory": memory,
        "disk": disk,
        "os": platform.system(),
        "os_version": platform.version(),
        "hostname": platform.node(),
        "load_avg": os.getloadavg(),
        "uptime": format_uptime(boot_time),
        "cpu_temp": cpu_temp,
        "ip_interno": get_ip_locale(),
        "ip_esterno": requests.get('https://api.ipify.org').text,
        "network_bytes_sent": format_bytes(bytes_sent),
        "network_bytes_recv": format_bytes(bytes_recv),
    }

@app.route("/api/system", methods=["GET"])
def system_data():
    return jsonify(get_system_info())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
