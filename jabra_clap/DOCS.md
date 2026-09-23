# Jabra Double Clap – Dokumentation

## Übersicht

Jabra Double Clap ist eine Home-Assistant-App zur Erkennung eines Doppelklatschens über ein angeschlossenes Jabra-Audiogerät.

Entwickelt und getestet wurde sie mit einem **Jabra Speak2 75 über Jabra Link 390** unter Home Assistant OS.

Die App speichert keine Audiodateien. Sie verarbeitet den Audiostream ausschließlich in kleinen Zeitfenstern und wertet Signalmerkmale aus.

## Funktionsweise

Ein Klatscher wird nicht nur anhand seiner Lautstärke erkannt.

Die App bewertet mehrere Eigenschaften gleichzeitig:

- **Peak**  
  Maximale Lautstärkespitze eines Impulses.

- **RMS**  
  Durchschnittliche Signalenergie während des Impulses.

- **Rise Factor**  
  Verhältnis zwischen aktuellem Pegel und normalem Raumpegel.

- **Crest Factor**  
  Verhältnis zwischen Peak und RMS.

- **Sharpness**  
  Bewertet, wie schnell und scharf sich das Audiosignal verändert.

- **Pulsdauer**  
  Ein echter Klatscher sollte nur sehr kurz anhalten.

- **Gap**  
  Zeitlicher Abstand zwischen erstem und zweitem Klatscher.

Erst wenn zwei passende Klatschimpulse innerhalb des erlaubten Zeitfensters erkannt werden, wird der konfigurierte Home-Assistant-Webhook ausgelöst.

## Standardkonfiguration

| Option | Standard | Bedeutung |
|---|---:|---|
| `device_match` | `Jabra Link 390` | Text, nach dem im Namen der Audioquelle gesucht wird |
| `peak_threshold` | `0.55` | Mindest-Peak |
| `rms_threshold` | `0.08` | Mindest-RMS |
| `rise_factor` | `3.5` | Mindestanstieg gegenüber dem normalen Raumpegel |
| `min_crest_factor` | `3.4` | Mindest-Crest-Factor |
| `min_sharpness` | `0.55` | Mindest-Schärfe des Impulses |
| `max_pulse_ms` | `120` | Maximale Dauer eines Klatschimpulses |
| `min_gap_ms` | `180` | Minimaler Abstand zwischen beiden Klatschern |
| `max_gap_ms` | `650` | Maximaler Abstand zwischen beiden Klatschern |
| `cooldown_ms` | `2500` | Sperrzeit nach erfolgreicher Erkennung |
| `webhook_id` | individuell | Eigene geheime Webhook-ID |

## Webhook-Sicherheit

Ab Version 1.0.8 enthält das öffentliche Repository absichtlich keine feste Webhook-ID mehr.

Die `webhook_id` muss pro Installation selbst vergeben werden.

Verwende am besten eine lange, zufällige Zeichenfolge, zum Beispiel:

```text
jabra_double_clap_DEINE_ZUFALLS_ID
```

Behandle diese ID wie ein Passwort.

Sie sollte nicht öffentlich in GitHub, Foren oder Screenshots veröffentlicht werden.

In der Home-Assistant-Automation sollte zusätzlich `local_only: true` verwendet werden.

## Home-Assistant-Automation

Die Automation muss exakt dieselbe `webhook_id` verwenden wie die App.

Beispiel für eine Schlafzimmerlampe:

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

## Testen

Öffne:

**Jabra Double Clap → Protokoll**

und klatsche zweimal.

Bei erfolgreicher Erkennung sollte ungefähr Folgendes erscheinen:

```text
Klatsch-Kandidat: peak=..., rms=..., crest=..., sharpness=..., dauer=...
1. Klatscher akzeptiert
Klatsch-Kandidat: peak=..., rms=..., crest=..., sharpness=..., dauer=...
2. Klatscher akzeptiert, Abstand=...ms
DOPPELKLATSCH ERKANNT -> Webhook ausgelöst
```

## Feintuning

### Die App reagiert auf zu viele Geräusche

Erhöhe schrittweise einen oder mehrere dieser Werte:

```text
peak_threshold
rms_threshold
rise_factor
min_crest_factor
min_sharpness
```

Alternativ kannst du `max_pulse_ms` verkleinern.

Dadurch werden nur noch kürzere und schärfere Impulse akzeptiert.

### Echte Klatscher werden erkannt, aber es wird kein Doppelklatschen ausgelöst

Wenn im Protokoll immer wieder nur folgendes erscheint:

```text
1. Klatscher akzeptiert
```

ist meist das Zeitfenster zwischen beiden Klatschern zu klein.

Versuche beispielsweise:

```text
min_gap_ms: 150
max_gap_ms: 1000
```

### Es wird gar kein Klatscher erkannt

Senke zunächst vorsichtig:

```text
peak_threshold
rms_threshold
```

Prüfe anschließend im Protokoll, ob wieder `Klatsch-Kandidat` erscheint.

### Sprache wird als Klatschen erkannt

Erhöhe bevorzugt:

```text
min_crest_factor
min_sharpness
rise_factor
```

Sprache ist normalerweise länger und weniger impulsartig als ein echter Klatscher.

## Audioquelle

Beim Start listet die App die verfügbaren PulseAudio-Quellen auf.

Anschließend wird nach dem Text aus `device_match` gesucht.

Für einen Jabra Link 390 kann der Mikrofoneingang beispielsweise so aussehen:

```text
alsa_input.usb-_Jabra_Link_390_...mono-fallback
```

Im Protokoll sollte anschließend etwa Folgendes stehen:

```text
Passende Audioquelle gefunden: ...
Benutze Mikrofon: ...
```

## Nutzung zusammen mit Assist Satellite

Jabra Double Clap kann parallel zu Home Assistant Assist Satellite betrieben werden.

Assist Satellite verarbeitet weiterhin Wakewords und Sprachbefehle, während Jabra Double Clap denselben Audio-Stack zur Erkennung kurzer Klatschimpulse nutzt.

Je nach Hardware und Auslastung kann das Verhalten variieren.

## Datenschutz

Die App:

- speichert keine Audiodateien
- erstellt keine Sprachaufzeichnungen
- transkribiert keine Sprache
- sendet keine Audiodaten an externe Dienste
- berechnet lediglich Signalmerkmale des laufenden Mikrofonstreams

## Automatischer Start

In Home Assistant kann **Beim Systemstart starten** aktiviert werden.

Zusätzlich empfiehlt sich **Watchdog**, damit die App bei einem unerwarteten Absturz automatisch neu gestartet wird.

## Status

Jabra Double Clap ist derzeit als **experimentell** gekennzeichnet.

Unterschiedliche Räume, Mikrofonpositionen und Hintergrundgeräusche können Feintuning notwendig machen.

## Autor

**Entwickelt von Filo**
