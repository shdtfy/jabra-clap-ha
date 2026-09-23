# Double Clap – Dokumentation

## Übersicht

Double Clap ist eine Home-Assistant-App zur lokalen Erkennung eines Doppelklatschens über einen kompatiblen Mikrofoneingang.

Die App wurde ursprünglich mit einem **Jabra Speak2 75 über Jabra Link 390** entwickelt, ist aber nicht an Jabra-Hardware gebunden.

Andere USB-Mikrofone, Konferenzlautsprecher und PulseAudio-kompatible Audioeingänge können ebenfalls funktionieren.

Die App speichert keine Audiodateien. Sie verarbeitet den Audiostream in kleinen Zeitfenstern und wertet ausschließlich Signalmerkmale aus.

## Mikrofon auswählen

Standardmäßig steht:

```text
device_match: auto
```

Double Clap versucht damit, die Standard-PulseAudio-Eingangsquelle automatisch auszuwählen.

Beim Start werden alle nutzbaren Audioeingänge im Protokoll angezeigt.

Wenn du ein bestimmtes Mikrofon verwenden möchtest, kannst du `device_match` auf einen eindeutigen Teil des Gerätenamens setzen.

Beispiele:

```text
Jabra Link 390
```

```text
USB Audio Device
```

Wenn `auto` keine eindeutige Audioquelle bestimmen kann, zeigt das Protokoll die gefundenen Eingänge an.

## Funktionsweise

Ein Klatscher wird nicht nur anhand seiner Lautstärke erkannt.

Double Clap bewertet mehrere Eigenschaften gleichzeitig:

- **Peak**: maximale Lautstärkespitze eines Impulses
- **RMS**: durchschnittliche Signalenergie
- **Rise Factor**: Verhältnis zwischen aktuellem Pegel und normalem Raumpegel
- **Crest Factor**: Verhältnis zwischen Peak und RMS
- **Sharpness**: wie schnell und scharf sich das Signal verändert
- **Pulsdauer**: ein Klatscher sollte nur sehr kurz anhalten
- **Gap**: zeitlicher Abstand zwischen erstem und zweitem Klatscher

Erst wenn zwei passende Impulse innerhalb des erlaubten Zeitfensters erkannt werden, wird der konfigurierte Home-Assistant-Webhook ausgelöst.

## Standardkonfiguration

| Option | Standard | Bedeutung |
|---|---:|---|
| `device_match` | `auto` | Standard-Audioquelle automatisch wählen oder Gerätenamen angeben |
| `peak_threshold` | `0.55` | Mindest-Peak |
| `rms_threshold` | `0.08` | Mindest-RMS |
| `rise_factor` | `3.5` | Mindestanstieg gegenüber dem normalen Raumpegel |
| `min_crest_factor` | `3.4` | Mindest-Crest-Factor |
| `min_sharpness` | `0.55` | Mindest-Schärfe des Impulses |
| `max_pulse_ms` | `120` | Maximale Dauer eines Klatschimpulses |
| `min_gap_ms` | `180` | Minimaler Abstand zwischen beiden Klatschern |
| `max_gap_ms` | `650` | Maximaler Abstand zwischen beiden Klatschern |
| `cooldown_ms` | `2500` | Sperrzeit nach erfolgreicher Erkennung |
| `webhook_id` | erforderlich | Eigene geheime Webhook-ID |

## Webhook-Sicherheit

Double Clap enthält keine feste Webhook-ID.

Jede Installation sollte eine eigene lange und zufällige ID verwenden.

Beispiel:

```text
double_clap_DEINE_ZUFALLS_ID
```

Behandle die ID wie ein Passwort.

In der Home-Assistant-Automation sollte zusätzlich `local_only: true` verwendet werden.

Die konfigurierte Webhook-ID wird von Double Clap nicht im Protokoll ausgegeben.

## Home-Assistant-Automation

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

Passe `light.schlafzimmer` an die gewünschte Entity an.

## Testen

Öffne:

**Double Clap → Protokoll**

Beim Start sollten die verfügbaren Audioquellen und die ausgewählte Quelle erscheinen.

Bei einem erkannten Doppelklatschen erscheint ungefähr:

```text
Klatsch-Kandidat: peak=..., rms=..., crest=..., sharpness=..., dauer=...
1. Klatscher akzeptiert
Klatsch-Kandidat: peak=..., rms=..., crest=..., sharpness=..., dauer=...
2. Klatscher akzeptiert, Abstand=...ms
DOPPELKLATSCH ERKANNT -> Webhook ausgelöst
```

## Feintuning

### Zu viele Fehl-Auslösungen

Erhöhe schrittweise:

```text
peak_threshold
rms_threshold
rise_factor
min_crest_factor
min_sharpness
```

Oder verkleinere:

```text
max_pulse_ms
```

### Beide Klatscher werden einzeln erkannt

Wenn wiederholt nur `1. Klatscher akzeptiert` erscheint, vergrößere das Zeitfenster.

Beispiel:

```text
min_gap_ms: 150
max_gap_ms: 1000
```

### Es wird kein Klatscher erkannt

Senke zunächst vorsichtig:

```text
peak_threshold
rms_threshold
```

### Sprache wird als Klatschen erkannt

Erhöhe bevorzugt:

```text
min_crest_factor
min_sharpness
rise_factor
```

## Nutzung mit Assist Satellite

Double Clap kann parallel zu Home Assistant Assist Satellite laufen.

Assist Satellite verarbeitet weiterhin Wakewords und Sprachbefehle, während Double Clap denselben Audio-Stack für die Erkennung kurzer Klatschimpulse nutzt.

## Datenschutz

- Keine Audiodateien werden gespeichert.
- Gespräche werden nicht aufgezeichnet.
- Sprache wird nicht transkribiert.
- Audiodaten werden nicht an externe Dienste gesendet.
- Es werden ausschließlich Signalmerkmale des laufenden Mikrofonstreams berechnet.
- Die konfigurierte Webhook-ID wird nicht im Log ausgegeben.

## Kompatibilität

Getestet:

- Jabra Speak2 75
- Jabra Link 390
- Home Assistant OS
- Assist Satellite

Weitere PulseAudio-kompatible Mikrofone können funktionieren, sind aber nicht alle einzeln getestet.

## Status

Double Clap ist derzeit **experimentell**.

## Autor

**Entwickelt von Filo Mahlich**
