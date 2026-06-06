# wol-status – Installation für App-Nutzer

Damit die **„WOL & Server"**-App den Status-Tab (CPU/RAM/Netz/Temperatur)
und den Docker-Tab anzeigen kann, läuft auf dem zu überwachenden Server
ein kleiner Dienst namens `wol-status` auf Port **8000**.

Es gibt drei Wege, ihn zu installieren – such dir den bequemsten aus:

| Weg | Aufwand | Voraussetzungen |
|---|---|---|
| **A. In der App** (One-Tap) | 30 Sekunden | SSH-Zugang ist schon in der App eingerichtet |
| **B. Einzeiler im Terminal** | 1 Minute | SSH-Zugang zum Server, Docker installiert |
| **C. docker-compose.yml** | 2 Minuten | wie B, ein bisschen Datei-Verwaltung |

> **Was die App ohne dieses Backend kann:** Wake-on-LAN, SSH-Konsole und der
> Docker-Tab funktionieren auch ohne. Nur der Live-Status-Tab braucht es.

---

## Voraussetzung: Docker

Falls auf dem Server **noch kein Docker** läuft, einmalig installieren:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Danach einmal ab- und wieder anmelden, damit die Gruppenmitgliedschaft greift.
```

Prüfen:
```bash
docker ps     # sollte ohne sudo eine (ggf. leere) Tabelle ausgeben
```

---

## Weg A – Direkt aus der App installieren (empfohlen)

1. App öffnen → den Server auswählen, auf dem das Backend installiert werden soll.
2. **Zahnrad** ⚙️ unten links antippen → **Einstellungen**.
3. Ganz unten: **„Backend installieren"**.
4. Image-Adresse bestätigen (vorausgefüllt) und auf **Installieren** tippen.

Die App führt im Hintergrund per SSH genau die Schritte aus Weg B aus.
Wenn fertig, antwortet `http://<server>:8000/status` automatisch – der
Status-Tab füllt sich.

---

## Weg B – Einzeiler

Per SSH einloggen und ausführen:

```bash
docker run -d \
  --name wol-status \
  --restart unless-stopped \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  ghcr.io/lsnrw/wol-status:latest
```

> Das Image gibt es auf zwei Registries — beide aus demselben CI-Build,
> beide **Multi-Arch** (amd64 + arm64), beide ohne Login pullbar:
>
> | Registry | Image-Adresse |
> |---|---|
> | GitHub Container Registry | `ghcr.io/lsnrw/wol-status:latest` |
> | Docker Hub | `lsnrw/wol-status:latest` |
>
> Falls dein Netz `ghcr.io` blockt, einfach den letzten Tag oben durch
> `lsnrw/wol-status:latest` ersetzen.

Prüfen:
```bash
curl http://localhost:8000/status
```

---

## Weg C – docker-compose.yml

1. Datei `docker-compose.yml` anlegen mit dem Inhalt aus
   [`docker-compose.prebuilt.yml`](docker-compose.prebuilt.yml).
2. Starten:
   ```bash
   docker compose up -d
   ```
3. Logs ansehen / Status prüfen:
   ```bash
   docker compose logs -f
   curl http://localhost:8000/status
   ```

---

## In der App eintragen

Egal welchen Weg du gewählt hast, in der App brauchst du diese Felder:

| Feld | Wert |
|---|---|
| **Name** | Beliebig, z. B. „Server" |
| **SSH-Host** | IP/Hostname des Servers |
| **SSH-Port** | 22 |
| **SSH-User / Auth** | wie gewohnt |
| **Status-Port** | **8000** |
| **Docker-Tab anzeigen** | ✅ wenn du den Docker-Socket gemountet hast |
| **MAC-Adresse / Broadcast-IP** | nur wenn du Wake-on-LAN nutzen willst |

Anschließend **„Verbindung testen"** → sollte `SSH: OK | Status: OK` zeigen.

---

## Sicherheit

- Der Dienst hat **keine Authentifizierung**. Bitte **nicht** ins Internet
  exposen – Port 8000 sollte nur im LAN erreichbar sein.
- Der Docker-Socket ist **read-only** gemountet; die App listet darüber nur
  Container, sie startet/stoppt sie über SSH.
- Wenn du den Docker-Tab nicht brauchst, kannst du den Socket-Mount weglassen
  – der `/status`-Endpunkt funktioniert auch ohne.

---

## Updates

```bash
docker pull ghcr.io/lsnrw/wol-status:latest
docker rm -f wol-status
# danach den Run-Befehl von oben erneut ausführen (oder `docker compose up -d`)
```

Über die App: gleicher Button **„Backend installieren"** – er erkennt eine
bestehende Installation und aktualisiert sie auf die neueste Version.
