from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psutil
import time
import os
import docker

app = FastAPI()


@app.get("/status")
def get_status():
    # CPU als 0..1
    cpu = psutil.cpu_percent(interval=0.2) / 100.0

    # RAM als 0..1
    mem = psutil.virtual_memory()
    ram = mem.percent / 100.0

    # Netzwerk über 0.8 Sek. messen (etwas schneller als 1s)
    net1 = psutil.net_io_counters()
    time.sleep(0.8)
    net2 = psutil.net_io_counters()

    down_bps = net2.bytes_recv - net1.bytes_recv
    up_bps = net2.bytes_sent - net1.bytes_sent

    down_mbps = down_bps * 8 / 1_000_000
    up_mbps = up_bps * 8 / 1_000_000

    # CPU-Temperatur (kann auf manchen Systemen None sein)
    cpu_temp = None
    try:
      temps = psutil.sensors_temperatures(fahrenheit=False)
      if temps:
          # irgendeinen Sensor nehmen, meistens "coretemp" o.ä.
          first_key = next(iter(temps))
          entries = temps[first_key]
          if entries:
              cpu_temp = float(entries[0].current)
    except Exception:
        cpu_temp = None

    # Load Average (nur Linux/Unix)
    load_1 = load_5 = load_15 = None
    try:
        l1, l5, l15 = os.getloadavg()
        load_1, load_5, load_15 = float(l1), float(l5), float(l15)
    except Exception:
        pass

    # Root-Disk-Auslastung (0..1)
    disk = psutil.disk_usage("/")
    disk_usage = disk.percent / 100.0

    # Swap-Auslastung (0..1)
    swap = psutil.swap_memory()
    swap_usage = swap.percent / 100.0 if swap.total > 0 else 0.0

    # Uptime in Sekunden
    uptime_sec = time.time() - psutil.boot_time()

    return {
        "cpu": cpu,
        "ram": ram,
        "down_mbps": down_mbps,
        "up_mbps": up_mbps,
        "cpu_temp": cpu_temp,       # °C oder null
        "load_1": load_1,
        "load_5": load_5,
        "load_15": load_15,
        "disk_usage": disk_usage,   # 0..1
        "swap_usage": swap_usage,   # 0..1
        "uptime_sec": uptime_sec,
    }


def _format_ports(ports: list) -> str:
    """Formatiert die Ports-Liste der Docker API zu einem lesbaren String.

    Eingabe (Docker /containers/json API):
      [{"IP": "0.0.0.0", "PrivatePort": 80, "PublicPort": 8080, "Type": "tcp"}, ...]

    Ausgabe: "0.0.0.0:8080->80/tcp, :::8080->80/tcp"
    """
    if not ports:
        return ""
    parts = []
    for p in ports:
        private = p.get("PrivatePort", "")
        proto = p.get("Type", "tcp")
        public = p.get("PublicPort")
        ip = p.get("IP", "")
        if public:
            parts.append(f"{ip}:{public}->{private}/{proto}")
        else:
            parts.append(f"{private}/{proto}")
    return ", ".join(parts)


@app.get("/containers")
def get_containers():
    """Gibt alle Docker Container (laufend + gestoppt) als JSON-Array zurück.

    Benötigt Zugriff auf den Docker-Socket:
      docker run ... -v /var/run/docker.sock:/var/run/docker.sock ...
    """
    try:
        client = docker.from_env()
        # client.api.containers() ruft GET /containers/json auf und liefert
        # u.a. das lesbare "Status"-Feld ("Up 2 hours", "Exited (0) 3 days ago")
        # sowie das maschinenlesbare "State"-Feld ("running", "exited", ...).
        raw = client.api.containers(all=True)
        result = []
        for c in raw:
            names = c.get("Names", [])
            name = names[0] if names else ""
            ports_str = _format_ports(c.get("Ports", []))
            result.append({
                "ID": c.get("Id", "")[:12],
                "Names": name,
                "Image": c.get("Image", ""),
                "Status": c.get("Status", ""),   # "Up 2 hours" / "Exited (0) …"
                "State": c.get("State", ""),     # "running" / "exited" / "paused"
                "Ports": ports_str,
            })
        return result
    except docker.errors.DockerException as e:
        return JSONResponse(status_code=503, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
