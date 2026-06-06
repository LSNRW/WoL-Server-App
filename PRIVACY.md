# Datenschutzerklärung

**App:** WOL & Server – Wake-on-LAN & Server Manager
**Stand:** 6. Juni 2026

> Diese Erklärung beschreibt, welche Daten die mobile App
> **„WOL & Server"** verarbeitet. Wenn du die App nicht installierst,
> findet keinerlei Datenverarbeitung statt.

---

## 1. Verantwortlicher

Verantwortlich für die Datenverarbeitung im Sinne der Datenschutz-Grund­verordnung
(DSGVO) ist:

**Lindemann Solutions NRW – Tobias Lindemann**
Rathelbecker Weg 14
40699 Erkrath
Deutschland

Telefon: +49 211 95072038
E-Mail: <datenschutz@lsnrw.de>

---

## 2. Kurzfassung

- Die App verarbeitet **ausschließlich** Daten, die du selbst eingibst
  (z. B. Server-Adressen, SSH-Zugangsdaten).
- Diese Daten werden **nur lokal auf deinem Gerät** gespeichert.
- Es findet **keine Übertragung an uns oder an Dritte** statt – außer
  zu den Servern, die du selbst konfigurierst.
- Es gibt **kein Tracking, keine Analytics, keine Werbung und keine
  Crash-Berichte**.
- Wir betreiben **keine eigenen Server**, mit denen die App spricht.

---

## 3. Welche Daten werden verarbeitet?

### 3.1 Daten, die du eingibst und die lokal gespeichert werden

Damit die App ihre Funktion erfüllen kann, speicherst du in den
Server-Einstellungen Daten wie:

- frei wählbarer Name des Servers
- MAC-Adresse, Broadcast-IP und Port für Wake-on-LAN
- SSH-Host, SSH-Port, SSH-Benutzername
- SSH-Passwort **oder** SSH-Private-Key
- Port für den optionalen Status-Dienst
- frei definierbare Schnellbefehle
- gewählter App-Stil (hell/dunkel/System)

**Speicherort:**

| Datentyp | Speicherort | Verschlüsselung |
|---|---|---|
| Allgemeine Server-Konfiguration | App-eigener Speicher (`SharedPreferences`) | Schutz durch Geräte-Sandbox des Betriebssystems |
| **SSH-Passwörter und SSH-Keys** | iOS-Keychain bzw. Android-Keystore | systemseitig verschlüsselt |

Diese Daten verlassen dein Gerät nicht. Sie werden auch nicht an uns
übertragen, gesichert oder synchronisiert.

### 3.2 Verbindungen zu Servern, die du selbst angibst

Die App stellt – ausgelöst durch dich – folgende Verbindungen her, **direkt
zu den von dir konfigurierten Servern**:

- **Wake-on-LAN:** Senden eines „Magic Packet" als UDP-Broadcast in deinem
  lokalen Netzwerk.
- **SSH-Verbindung** zum von dir angegebenen Host: für die SSH-Konsole, die
  Steuerung von Docker-Containern und das optionale Installieren des
  Backend-Dienstes.
- **HTTP-Anfragen** an den von dir angegebenen Status-Endpunkt (in der Regel
  Port 8000) für die Live-Anzeige von CPU-, RAM-, Netzwerk- und
  Container-Daten.

Alle diese Verbindungen gehen ausschließlich an die Adressen, die du selbst
eingegeben hast. Es gibt keinerlei „Backend" oder Vermittlungs-Server, der
von uns betrieben wird.

### 3.3 Daten, die die App ausdrücklich **nicht** verarbeitet

- ❌ Keine Telemetrie- oder Nutzungsdaten
- ❌ Keine Analytics (Google Analytics, Firebase, Adjust o. ä.)
- ❌ Keine Werbung und keine Werbe-IDs
- ❌ Keine Crash-Reports an externe Dienste
- ❌ Keine Standortdaten
- ❌ Keine Kontakte, Kalender, Fotos, Mikrofon oder Kamera
- ❌ Kein Zugriff auf Adressbuch oder andere Apps
- ❌ Keine Push-Notifications über externe Dienste (siehe Abschnitt 6)

---

## 4. Rechtsgrundlage

Die Verarbeitung der unter Abschnitt 3.1 genannten Daten erfolgt auf
Grundlage von **Art. 6 Abs. 1 lit. b DSGVO** (Erfüllung des
Nutzungsvertrags – ohne diese Daten kann die App ihre Funktion nicht
erbringen) sowie **Art. 6 Abs. 1 lit. f DSGVO** (berechtigtes Interesse
an einem funktionierenden Dienst).

---

## 5. Speicherdauer

Sämtliche unter Abschnitt 3.1 genannten Daten bleiben so lange auf deinem
Gerät, bis du

- sie in der App **manuell löschst** (Server entfernen) oder
- die App **deinstallierst**.

In beiden Fällen werden die Daten – auch die in Keychain/Keystore
gespeicherten Passwörter/Keys – vom Betriebssystem entfernt.

---

## 6. Push-Benachrichtigungen

Du kannst pro Server lokale Benachrichtigungen aktivieren („Server online /
offline").

- Diese Benachrichtigungen werden **lokal auf deinem Gerät erzeugt**
  (Bibliothek `flutter_local_notifications`).
- Es wird **kein** Push-Dienst wie Apple APNs oder Google FCM verwendet.
- Auf Android wird ein periodischer Hintergrund-Check (alle 15 Minuten,
  Bibliothek `workmanager`) ausgeführt, der ausschließlich deinen
  eigenen Server kontaktiert.

---

## 7. Empfänger / Weitergabe

Wir geben deine Daten **nicht weiter**. Datenflüsse entstehen nur:

- **zu den Servern, die du selbst angibst** – diese erreichst du direkt;
  ein „Umweg" über unsere Infrastruktur findet nicht statt.
- **gegenüber Apple bzw. Google** im Rahmen des Bezugs der App über den
  App Store / Google Play Store. Hierfür gelten die jeweiligen
  Datenschutzbestimmungen von Apple
  (<https://www.apple.com/legal/privacy/>) bzw. Google
  (<https://policies.google.com/privacy>).

Eine Übermittlung in Drittländer außerhalb der EU findet durch uns
**nicht** statt.

---

## 8. Verwendete Open-Source-Komponenten

Die App ist mit dem Flutter-Framework von Google entwickelt und nutzt
unter anderem die Open-Source-Bibliotheken `dartssh2`, `xterm`,
`fl_chart`, `flutter_secure_storage`, `flutter_local_notifications`,
`shared_preferences`, `http`, `provider`, `workmanager`,
`file_picker` und `uuid`. Diese Bibliotheken laufen ausschließlich auf
deinem Gerät und kommunizieren nicht eigenständig mit Dritten.

Die App-Update-Funktion für den optionalen Backend-Dienst lädt das
Container-Image von **GitHub Container Registry (ghcr.io)** und/oder
**Docker Hub (docker.io)** – und zwar **direkt durch deinen Server**,
nicht durch die App selbst. Dabei gelten die Datenschutz­bestimmungen
von GitHub und Docker.

---

## 9. Deine Rechte als betroffene Person

Du hast nach der DSGVO insbesondere folgende Rechte:

- **Auskunft** über die zu deiner Person gespeicherten Daten (Art. 15)
- **Berichtigung** unrichtiger Daten (Art. 16)
- **Löschung** („Recht auf Vergessenwerden", Art. 17)
- **Einschränkung der Verarbeitung** (Art. 18)
- **Datenübertragbarkeit** (Art. 20)
- **Widerspruch** gegen die Verarbeitung (Art. 21)
- **Widerruf** einer erteilten Einwilligung mit Wirkung für die Zukunft
  (Art. 7 Abs. 3)

Da wir technisch **keine Daten von dir empfangen oder speichern**, kannst
du diese Rechte für die in dieser App verarbeiteten Daten in vollem
Umfang durch das Löschen einzelner Einträge in der App oder durch
Deinstallation der App ausüben.

Für Rückfragen schreibe an die in Abschnitt 1 genannte E-Mail-Adresse.

---

## 10. Beschwerderecht bei der Aufsichtsbehörde

Du hast das Recht, dich bei einer Datenschutz-Aufsichtsbehörde zu
beschweren. Für Nordrhein-Westfalen zuständig ist:

**Landesbeauftragte für Datenschutz und Informationsfreiheit
Nordrhein-Westfalen (LDI NRW)**
Kavalleriestraße 2–4, 40213 Düsseldorf
<https://www.ldi.nrw.de>

---

## 11. Änderungen dieser Datenschutzerklärung

Wir können diese Datenschutzerklärung anpassen, wenn sich der
Funktionsumfang der App ändert oder neue rechtliche Anforderungen
gelten. Die jeweils aktuelle Fassung ist in der App und unter
<https://github.com/LSNRW/WoL-Server-App/blob/main/PRIVACY.md>
verfügbar. Das oben genannte Datum kennzeichnet den Stand dieser
Fassung.
