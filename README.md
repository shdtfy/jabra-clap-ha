# Jabra Double Clap for Home Assistant

![Jabra Double Clap](jabra_clap/logo.png)

Eine experimentelle Home-Assistant-App zur Erkennung von Doppelklatschen über ein angeschlossenes Jabra-Audiogerät.

**Entwickelt von Filo**

## Funktionen

- Doppelklatsch-Erkennung über einen Jabra Link 390
- Erkennung kurzer, scharfer Klatschimpulse statt einfacher Lautstärkeschwellen
- Auswertung von Peak, RMS, Rise Factor, Crest Factor, Sharpness und Impulsdauer
- Einstellbares Zeitfenster zwischen beiden Klatschern
- Lokaler Home-Assistant-Webhook als Trigger
- Einstellbare Empfindlichkeit
- Keine Speicherung oder Aufzeichnung von Audiodaten
- Kann parallel zu Home Assistant Assist Satellite betrieben werden

## Installation

1. Öffne in Home Assistant:

   **Einstellungen → Apps → App-Store → Repositories**

2. Füge dieses Repository hinzu:

   `https://github.com/shdtfy/jabra-clap-ha`

3. Suche im App-Store nach **Jabra Double Clap**.

4. Installiere die App.

5. Öffne anschließend den Tab **Konfiguration**.

6. Vergib eine eigene, zufällige `webhook_id`.

7. Starte die App und prüfe den Tab **Protokoll**.

## Webhook einrichten

Die App enthält absichtlich keine feste Webhook-ID.

Jede Installation sollte eine eigene, zufällige ID verwenden.

Beispiel:

`jabra_double_clap_DEINE_ZUFALLS_ID`

Behandle die Webhook-ID wie ein Passwort und veröffentliche sie nicht in einem öffentlichen Repository.

In der Home-Assistant-Automation muss exakt dieselbe ID verwendet werden.

## Beispiel-Automation

Dieses Beispiel schaltet eine Schlafzimmerlampe bei jedem erkannten Doppelklatschen um:

```yaml
alias: Schlafzimmer - Doppelklatschen Licht
triggers:
  - trigger: webhook
    webhook_id: DEINE_WEBHOOK_ID
    allowed_methods:
      - POST
    local_only: true

actions:
  - action: light.toggle
    target:
      entity_id: light.schlafzimmer

mode: single
```

Passe `light.schlafzimmer` an die Entity-ID deiner gewünschten Lampe oder Lichtgruppe an.

## Wie die Erkennung funktioniert

Jabra Double Clap reagiert nicht einfach auf jedes laute Geräusch.

Ein möglicher Klatscher wird anhand mehrerer Signalmerkmale bewertet:

- **Peak**  
  Maximale Lautstärkespitze.

- **RMS**  
  Durchschnittliche Signalenergie.

- **Rise Factor**  
  Bewertet, wie stark sich ein Geräusch vom normalen Raumpegel abhebt.

- **Crest Factor**  
  Verhältnis zwischen Lautstärkespitze und durchschnittlichem Pegel.

- **Sharpness**  
  Bewertet, wie kurz und scharf ein Geräusch ist.

- **Impulsdauer**  
  Ein Klatscher muss innerhalb einer kurzen Zeit wieder abfallen.

Erst wenn zwei passende Klatschimpulse innerhalb des eingestellten Zeitfensters erkannt werden, wird der Home-Assistant-Webhook ausgelöst.

## Unterstützte Hardware

Entwickelt und getestet mit:

- Jabra Speak2 75
- Jabra Link 390
- Home Assistant OS
- Assist Satellite

Andere PulseAudio-kompatible Mikrofone können ebenfalls funktionieren.

## Datenschutz

Jabra Double Clap:

- speichert keine Audiodateien
- zeichnet keine Gespräche auf
- transkribiert keine Sprache
- analysiert ausschließlich laufende Audiosignalwerte
- verwendet einen lokalen Home-Assistant-Webhook

## Status

Die App befindet sich aktuell im experimentellen Stadium.

Je nach Raum, Mikrofonposition, Abstand, Fernseher, Musik und anderen Hintergrundgeräuschen kann Feintuning erforderlich sein.

## Dokumentation

Eine ausführliche Beschreibung aller Einstellungen und Hinweise zum Feintuning findest du hier:

[`jabra_clap/DOCS.md`](jabra_clap/DOCS.md)

## Repository-Struktur

```text
jabra-clap-ha/
├── LICENSE
├── README.md
├── repository.yaml
└── jabra_clap/
    ├── CHANGELOG.md
    ├── DOCS.md
    ├── Dockerfile
    ├── README.md
    ├── clap.py
    ├── config.yaml
    ├── icon.png
    └── logo.png
```

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## Autor

**Filo**

Home Assistant Projekt: **Jabra Double Clap**
