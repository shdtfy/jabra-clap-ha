# Jabra Double Clap for Home Assistant

![Jabra Double Clap](jabra_clap/logo.png)

Eine experimentelle Home-Assistant-App zur Erkennung von Doppelklatschen über ein angeschlossenes Jabra-Audiogerät.

**Entwickelt von Filo**

## Funktionen

- Doppelklatsch-Erkennung über den Jabra Link 390
- Erkennt kurze, scharfe Klatschimpulse statt nur allgemeine Lautstärke
- Auswertung von Peak, RMS, Crest Factor, Sharpness und Impulsdauer
- Einstellbares Zeitfenster zwischen beiden Klatschern
- Lokaler Home-Assistant-Webhook als Trigger
- Einstellbare Empfindlichkeit
- Keine Speicherung von Sprach- oder Audiodaten
- Läuft parallel zu Home Assistant Assist Satellite

## Installation

1. In Home Assistant zu  
   **Einstellungen → Apps → App-Store → Repositories** gehen.

2. Dieses Repository hinzufügen:

   `https://github.com/shdtfy/jabra-clap-ha`

3. Im App-Store nach **Jabra Double Clap** suchen.

4. App installieren.

5. Unter **Konfiguration** die gewünschten Werte einstellen.

6. App starten und im **Protokoll** testen.

## Beispiel-Automation

Die App löst bei einem erkannten Doppelklatschen einen lokalen Home-Assistant-Webhook aus.

Beispiel:

```yaml
alias: Schlafzimmer - Doppelklatschen Licht
triggers:
  - trigger: webhook
    webhook_id: DEINE_WEBHOOK_ID
    allowed_methods:
      - POST
    local_only: true

actions:
  - action: switch.toggle
    target:
      entity_id:
        - switch.licht
        - switch.pv_anlage

mode: single
```

Die `webhook_id` muss mit der ID in der Konfiguration von **Jabra Double Clap** übereinstimmen.

## Wie die Erkennung funktioniert

Die App reagiert nicht einfach auf jedes laute Geräusch.

Ein möglicher Klatscher wird anhand mehrerer Merkmale bewertet:

- **Peak**  
  maximale Lautstärkespitze

- **RMS**  
  durchschnittliche Signalenergie

- **Rise Factor**  
  wie stark sich der Impuls vom normalen Raumpegel abhebt

- **Crest Factor**  
  Verhältnis zwischen Peak und durchschnittlicher Lautstärke

- **Sharpness**  
  bewertet, wie kurz und scharf das Geräusch ist

- **Impulsdauer**  
  ein Klatscher muss kurz genug sein

Erst wenn zwei passende Klatschimpulse innerhalb des eingestellten Zeitfensters erkannt werden, wird der Webhook ausgelöst.

## Unterstützte Hardware

Entwickelt und getestet mit:

- Jabra Speak2 75
- Jabra Link 390
- Home Assistant OS
- Assist Satellite

Andere PulseAudio-kompatible Mikrofone können ebenfalls funktionieren.

## Datenschutz

Die App:

- speichert keine Audiodateien
- zeichnet keine Gespräche auf
- transkribiert keine Sprache
- analysiert ausschließlich laufende Audiosignalwerte

## Status

Die App befindet sich aktuell im experimentellen Stadium.

Je nach:

- Raumgröße
- Mikrofonposition
- Hintergrundgeräuschen
- Fernseher oder Musik
- Abstand zum Mikrofon

kann Feintuning notwendig sein.

## Repository-Struktur

```text
jabra-clap-ha/
├── repository.yaml
├── README.md
├── LICENSE
└── jabra_clap/
    ├── config.yaml
    ├── Dockerfile
    ├── clap.py
    ├── icon.png
    ├── logo.png
    ├── README.md
    ├── DOCS.md
    └── CHANGELOG.md
```

## Autor

**Filo**

Home Assistant Projekt: Jabra Double Clap
