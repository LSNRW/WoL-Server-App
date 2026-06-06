# WoL & Server – Backend

> Server-seitiges Backend zur **„WOL & Server"**-App von
> [Lindemann Solutions NRW](https://github.com/LSNRW) — liefert
> System- und Docker-Statistiken über HTTP.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Platforms](https://img.shields.io/badge/arch-amd64%20%7C%20arm64-blue)
![Build](https://github.com/LSNRW/WoL-Server-App/actions/workflows/wol-status-image.yml/badge.svg)

---

Dieses Repo enthält den Quellcode für **`wol-status`** – einen schlanken
FastAPI-Dienst, der auf jedem Linux-Host läuft und der „WOL & Server"-App
die Live-Daten für den Status- und den Docker-Tab liefert.

| Was du suchst | Wo es steht |
|---|---|
| **Was ist das & warum?** | [`wol-status/README.md`](wol-status/README.md) |
| **Installations-Anleitung** (3 Wege) | [`wol-status/INSTALL.md`](wol-status/INSTALL.md) |
| **Quellcode** | [`wol-status/`](wol-status/) |
| **CI / Image-Build** | [`.github/workflows/wol-status-image.yml`](.github/workflows/wol-status-image.yml) |

## Schnellstart

```bash
docker run -d \
  --name wol-status \
  --restart unless-stopped \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  ghcr.io/lsnrw/wol-status:latest
```

Vollständige Anleitung inkl. Docker-Installation, Compose-Datei und der
One-Tap-Variante direkt aus der App: **[INSTALL.md](wol-status/INSTALL.md)**.

## Die App

Die zugehörige **mobile App** für iOS und Android (Wake-on-LAN, SSH-Konsole,
Docker-Tab und Live-Status) ist über App Store und Play Store erhältlich.
Der App-Quellcode ist nicht Teil dieses Repos.

## Lizenz

[MIT](LICENSE) — Copyright © 2026 Lindemann Solutions NRW Tobias Lindemann.
