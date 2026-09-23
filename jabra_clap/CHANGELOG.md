# Changelog

Alle wichtigen Änderungen an **Double Clap** werden hier dokumentiert.
## 1.1.1

- Autoren- und Maintainer-Angabe auf **Filo Mahlich** vereinheitlicht
- App-Metadaten aktualisiert

## 1.1.0

- Projekt von **Jabra Double Clap** zu **Double Clap** umbenannt
- App-Beschreibung hardwareunabhängig formuliert
- Jabra wird nur noch als getestete Hardware geführt
- Standard für `device_match` auf `auto` umgestellt
- Automatische Auswahl der Standard-PulseAudio-Eingangsquelle ergänzt
- Manuelle Auswahl anderer Mikrofone über `device_match` weiterhin möglich
- Unterstützung anderer PulseAudio-kompatibler Mikrofone deutlicher dokumentiert
- Webhook-ID wird nicht mehr im App-Protokoll ausgegeben
- Neues Double-Clap-Branding und neues Logo
- README, App-README und Dokumentation vollständig überarbeitet
- Maintainer- und Autorenangabe auf **Filo Mahlich** aktualisiert
- Interner Slug `jabra_clap` bleibt aus Kompatibilitätsgründen bestehen

## 1.0.8

- Feste Webhook-ID aus dem öffentlichen Repository entfernt
- `webhook_id` muss pro Installation individuell vergeben werden
- Webhook-ID wird in Home Assistant als Passwortfeld behandelt
- Dokumentation zur Webhook-Sicherheit ergänzt
- Öffentliche Beispiele auf neutrale Entity-IDs umgestellt
- README und Dokumentation überarbeitet
- MIT-Lizenz ergänzt
- Repository-Struktur bereinigt

## 1.0.7

- Eigenes App-Icon hinzugefügt
- Eigenes Logo/Banner hinzugefügt
- Beschreibung um **entwickelt von Filo** ergänzt
- Maintainer auf **Filo** gesetzt
- Metadaten bereinigt
- App-Darstellung im Home-Assistant-App-Store verbessert

## 1.0.3

- Erweiterte Klatsch-Erkennung eingeführt
- Crest Factor ergänzt
- Sharpness ergänzt
- Maximale Impulsdauer ergänzt
- Bessere Abgrenzung von Sprache, Musik und länger anhaltenden Geräuschen
- Klatsch-Kandidaten werden detaillierter im Protokoll ausgegeben

## 1.0.2

- Home-Assistant-Auslösung auf lokalen Webhook umgestellt
- Abhängigkeit vom Supervisor-Token entfernt
- Webhook-basierte Automation eingeführt

## 1.0.1

- Supervisor-/API-Zugriff angepasst
- Konfiguration für den Betrieb unter Home Assistant OS erweitert

## 1.0.0

- Erste funktionsfähige Version
- Doppelimpuls-Erkennung über Jabra-Mikrofoneingang
- Unterstützung für Jabra Link 390
- Einstellbare Peak-, RMS- und Zeitfensterwerte
- Auslösung eines Home-Assistant-Triggers bei erkanntem Doppelklatschen
