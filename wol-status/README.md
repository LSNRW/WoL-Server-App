# wol-status

> Schlanker FastAPI-Dienst, der System- und Docker-Statistiken über HTTP
> bereitstellt — das Backend zur **„WOL & Server"**-App.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Platforms](https://img.shields.io/badge/arch-amd64%20%7C%20arm64-blue)
![Python](https://img.shields.io/badge/python-3.12-blue)

---

## Worum geht's

Die [„WOL & Server"-App](#beziehung-zur-app) kann Server per Wake-on-LAN
aufwecken, eine SSH-Konsole öffnen und Docker-Container steuern – das geht
**ohne** dieses Backend.

Für den **Live-Status-Tab** (CPU, RAM, Netzwerk, Temperatur, Load, Disk, Swap,
Uptime, Container-Liste) braucht die App aber einen kleinen Dienst auf dem
zu überwachenden Host. Genau das ist `wol-status`: rund 130 Zeilen Python,
in einem Docker-Container, der **Port 8000** öffnet und zwei Endpunkte
bereitstellt.

## Highlights

- 🪶 **Klein** – ein einziges Python-File, ~130 Zeilen, eine Handvoll Pakete.
- 🐳 **Multi-Arch-Image** – läuft nativ auf **amd64** (PC-Server, NAS) und
  **arm64** (Raspberry Pi 3+/4/5).
- 📊 **Alles, was die App-Charts brauchen** – inklusive CPU-Temperatur,
  Load-Average und echter Netzwerk-Bandbreite (nicht nur des Container-veth).
- 🔌 **Optionaler Docker-Tab** – mit gemountetem Docker-Socket listet
  `/containers` alle Container des Hosts.
- 🔄 **Auto-Start** – `restart: unless-stopped`, übersteht jeden Reboot.

## Schnellstart

> Voraussetzung: Docker ist installiert. Eine ausführliche Anleitung (inkl.
> Docker-Installation, Compose-Datei und der bequemen One-Tap-Variante aus
> der App) steht in **[INSTALL.md](INSTALL.md)**.

Das Image gibt es auf **zwei Registries** — beide aus demselben CI-Build,
beide Multi-Arch (amd64 + arm64), beide ohne Login pullbar:

| Registry | Image-Adresse |
|---|---|
| GitHub Container Registry *(Default)* | `ghcr.io/lsnrw/wol-status:latest` |
| Docker Hub *(Alternative)* | `lsnrw/wol-status:latest` |

```bash
docker run -d \
  --name wol-status \
  --restart unless-stopped \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  ghcr.io/lsnrw/wol-status:latest
```

> Falls dein Netz `ghcr.io` blockt: den letzten Tag durch
> `lsnrw/wol-status:latest` ersetzen — alles andere bleibt gleich.

Prüfen:
```bash
curl http://localhost:8000/status
```

## Endpunkte

| Methode & Pfad   | Antwort | Inhalt |
|------------------|---------|--------|
| `GET /status`     | JSON    | CPU, RAM, Netzwerk Up/Down (Mbit/s), CPU-Temp, Load-Average (1/5/15 min), Disk, Swap, Uptime |
| `GET /containers` | JSON-Array | Alle Docker-Container (laufend + gestoppt) mit Name, Image, Status, State, Ports |

Beispielausgabe `/status`:
```json
{
  "cpu": 0.013,
  "ram": 0.189,
  "down_mbps": 0.0004,
  "up_mbps": 0.0,
  "cpu_temp": 47.4,
  "load_1": 0.84, "load_5": 0.46, "load_15": 0.30,
  "disk_usage": 0.026,
  "swap_usage": 0.0,
  "uptime_sec": 11400785
}
```

Werte wie `cpu`, `ram`, `disk_usage`, `swap_usage` sind als **Anteil** kodiert
(`0..1`). Felder, die ein Host nicht liefert (z. B. CPU-Temp auf manchen
Cloud-VMs), kommen als `null`.

## Warum `--network host`?

Damit der Container **die echten Netzwerk-Interfaces** des Hosts (eth0/wlan0
etc.) misst und nicht nur seinen internen Container-Traffic – sonst zeigt die
App immer 0 Mbit/s. Gleichzeitig bindet er Port `8000` direkt auf dem Host
(deshalb kein `ports:`-Eintrag in der Compose-Datei).

CPU-Temperatur, CPU, RAM, Load usw. funktionieren in dieser Konfiguration
ohne weitere Mounts (`psutil` liest sie aus `/proc` bzw. `/sys`, die der
Container ohnehin sieht).

## Sicherheit

- 🔒 **Kein Login.** Der Dienst soll **nur im LAN** erreichbar sein – bitte
  nicht ungeschützt ins Internet exposen.
- 📜 **Docker-Socket ist optional und read-only.** Die App liest darüber nur;
  Start/Stop/Restart von Containern laufen über SSH, nicht über diesen Socket.
  Wer den Docker-Tab nicht braucht, kann den Mount weglassen.
- ✅ **Quellcode ist überschaubar.** Du findest die komplette Logik in
  [`app.py`](app.py).

## Beziehung zur App

`wol-status` ist das Server-Pendant zur **„WOL & Server"**-App
(Wake-on-LAN-, SSH-, Docker- und Status-Manager für mehrere Server,
iOS/Android via Flutter).

Die App funktioniert grundsätzlich auch ohne dieses Backend – Wake-on-LAN,
SSH-Konsole und der Docker-Tab (per SSH `docker ps`) hängen nicht davon ab.
Nur der Status-Tab und die schnelle `/containers`-Abfrage benötigen
`wol-status`.

Wer keine Lust hat, das Backend manuell zu installieren, kann es **direkt
aus der App heraus** mit einem Tap einrichten – die App führt im Hintergrund
genau die Schritte aus diesem README per SSH aus.

## Updates

```bash
docker pull ghcr.io/lsnrw/wol-status:latest
docker rm -f wol-status
# danach den Run-Befehl von oben erneut ausführen
```

In der App: gleicher Button **„Backend installieren / aktualisieren"** in
den Server-Einstellungen – er erkennt eine bestehende Installation und
aktualisiert sie auf die neueste Version.

## Mitwirken

PRs sind willkommen, besonders für:
- weitere Statuswerte (z. B. spezifische Disks, GPU-Temperatur, smartctl)
- bessere CPU-Temp-Erkennung auf exotischer Hardware
- Tests

## Lizenz

[MIT](LICENSE) – sehr permissiv, gerne für eigene Projekte verwenden.
