# Double Clap for Home Assistant

![Double Clap](jabra_clap/logo.png)

**Lokale Doppelklatsch-Erkennung für Home Assistant.**

Double Clap überwacht einen kompatiblen Mikrofoneingang und erkennt zwei kurze, scharfe Klatschimpulse. Bei erfolgreicher Erkennung wird ein lokaler Home-Assistant-Webhook ausgelöst.

**Entwickelt von Filo Mahlich**

## Funktionen

- Hardwareunabhängige Doppelklatsch-Erkennung
- Funktioniert mit PulseAudio-kompatiblen Mikrofoneingängen
- Automatische Auswahl der Standard-Audioquelle
- Manuelle Mikrofonwahl über `device_match`
- Auswertung von Peak, RMS, Rise Factor, Crest Factor, Sharpness und Impulsdauer
- Einstellbares Zeitfenster zwischen beiden Klatschern
- Lokaler Home-Assistant-Webhook als Trigger
- Einstellbare Empfindlichkeit
- Keine Speicherung oder Aufzeichnung von Audiodaten
- Kann parallel zu Home Assistant Assist Satellite betrieben werden

## Getestete Hardware

Entwickelt und getestet mit:

- Jabra Speak2 75
- Jabra Link 390
- Home Assistant OS
- Assist Satellite

Andere USB-Mikrofone, Konferenzlautsprecher und PulseAudio-kompatible Audioeingänge können ebenfalls funktionieren.

## Installation

1. Öffne in Home Assistant:

   **Einstellungen → Apps → App-Store → Repositories**

2. Füge dieses Repository hinzu:

   `https://github.com/shdtfy/jabra-clap-ha`

3. Suche im App-Store nach **Double Clap**.

4. Installiere die App.

5. Öffne den Tab **Konfiguration**.

6. `device_match` kann zunächst auf `auto` bleiben.

7. Vergib eine eigene, zufällige `webhook_id`.

8. Starte die App und prüfe den Tab **Protokoll**.

## Mikrofon auswählen

Standardmäßig steht:

```text
device_match: auto
```

Double Clap versucht dann, die Standard-PulseAudio-Eingangsquelle automatisch zu verwenden.

Beim Start werden die verfügbaren Audioquellen im Protokoll aufgelistet.

Wenn du gezielt ein bestimmtes Mikrofon verwenden möchtest, trage bei `device_match` einen eindeutigen Teil des Namens ein.

Beispiel:

```text
Jabra Link 390
```

oder:

```text
USB Audio Device
```

## Webhook einrichten

Double Clap enthält keine feste Webhook-ID.

Jede Installation benötigt eine eigene, zufällige ID.

Beispiel:

`double_clap_DEINE_ZUFALLS_ID`

Behandle die Webhook-ID wie ein Passwort und veröffentliche sie nicht.

## Beispiel-Automation

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

Passe `light.schlafzimmer` an deine gewünschte Lampe, Lichtgruppe oder andere Automation an.

## Wie die Erkennung funktioniert

Double Clap reagiert nicht einfach auf jedes laute Geräusch.

Ein möglicher Klatscher wird anhand mehrerer Signalmerkmale bewertet:

- **Peak**: maximale Lautstärkespitze
- **RMS**: durchschnittliche Signalenergie
- **Rise Factor**: Anstieg gegenüber dem normalen Raumpegel
- **Crest Factor**: Verhältnis zwischen Peak und Durchschnittspegel
- **Sharpness**: wie kurz und scharf der Impuls ist
- **Impulsdauer**: ein Klatscher muss schnell wieder abfallen

Erst zwei passende Impulse innerhalb des eingestellten Zeitfensters lösen den Webhook aus.

## Datenschutz

Double Clap:

- speichert keine Audiodateien
- zeichnet keine Gespräche auf
- transkribiert keine Sprache
- sendet keine Audiodaten an externe Dienste
- analysiert ausschließlich laufende Signalwerte
- gibt die konfigurierte Webhook-ID nicht im Protokoll aus
- verwendet einen lokalen Home-Assistant-Webhook

## Status

Die App befindet sich aktuell im experimentellen Stadium.

Je nach Mikrofon, Raum, Abstand und Hintergrundgeräuschen kann Feintuning erforderlich sein.

## Dokumentation

Ausführliche Hinweise zu Einrichtung und Feintuning:

[`jabra_clap/DOCS.md`](jabra_clap/DOCS.md)

## Technischer Hinweis

Der interne App-Slug und der Ordnername bleiben vorerst `jabra_clap`, damit bestehende Installationen beim Update auf 1.1.0 nicht als neue App behandelt werden.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## Autor

**Filo Mahlich**

Home Assistant Projekt: **Double Clap**
