# Jabra Double Clap – Dokumentation

## Übersicht

Jabra Double Clap ist eine Home-Assistant-App zur Erkennung eines Doppelklatschens über ein angeschlossenes Jabra-Audiogerät. Entwickelt wurde sie für einen **Jabra Speak2 75 über Jabra Link 390**, kann aber auch mit anderen PulseAudio-kompatiblen Mikrofoneingängen funktionieren.

Die App speichert keine Audiodateien. Sie verarbeitet den Audiostream in kleinen Zeitfenstern und bewertet nur Signalmerkmale.

## Funktionsweise

Ein Klatscher wird nicht nur als „lautes Geräusch“ gewertet. Die App prüft mehrere Merkmale:

- **Peak**: maximale Lautstärkespitze
- **RMS**: mittlere Signalenergie
- **Rise Factor**: wie stark sich der Impuls vom normalen Raumpegel abhebt
- **Crest Factor**: Verhältnis von Peak zu RMS
- **Sharpness**: wie schnell und scharf sich das Signal verändert
- **Pulsdauer**: ein Klatscher muss kurz sein
- **Gap**: Abstand zwischen erstem und zweitem Klatscher

Erst wenn zwei passende Impulse innerhalb des erlaubten Zeitfensters erkannt werden, wird der Webhook ausgelöst.

## Standardkonfiguration

| Option | Standard | Bedeutung |
|---|---:|---|
| `device_match` | `Jabra Link 390` | Text, nach dem im Namen der Audioquelle gesucht wird |
| `peak_threshold` | `0.55` | Mindest-Peak |
| `rms_threshold` | `0.08` | Mindest-RMS |
| `rise_factor` | `3.5` | Mindestanstieg gegenüber dem Raumpegel |
| `min_crest_factor` | `3.4` | Mindest-Crest-Factor |
| `min_sharpness` | `0.55` | Mindest-Schärfe des Impulses |
| `max_pulse_ms` | `120` | Maximale Dauer eines Klatschimpulses |
| `min_gap_ms` | `180` | Minimaler Abstand zwischen zwei Klatschern |
| `max_gap_ms` | `650` | Maximaler Abstand zwischen zwei Klatschern |
| `cooldown_ms` | `2500` | Sperrzeit nach erfolgreicher Erkennung |
| `webhook_id` | individuell | ID des lokalen Home-Assistant-Webhooks |

## Home-Assistant-Automation

Lege eine Automation mit demselben `webhook_id` an, das in der App-Konfiguration steht.

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

`switch.pv_anlage` ist hier nur ein Beispiel für eine vorhandene zweite Schalt-Entität. Passe die Entity-IDs an dein System an.

## Testen

Öffne **Jabra Double Clap → Protokoll** und klatsche zweimal.

Bei einer erfolgreichen Erkennung sollte ungefähr Folgendes erscheinen:

```text
Klatsch-Kandidat: peak=..., rms=..., crest=..., sharpness=..., dauer=...
1. Klatscher akzeptiert
Klatsch-Kandidat: peak=..., rms=..., crest=..., sharpness=..., dauer=...
2. Klatscher akzeptiert, Abstand=...ms
DOPPELKLATSCH ERKANNT -> Webhook ausgelöst
```

## Feintuning

### Reagiert auf zu viele Geräusche

Erhöhe schrittweise:

- `peak_threshold`
- `rms_threshold`
- `rise_factor`
- `min_crest_factor`
- `min_sharpness`

Oder verkleinere `max_pulse_ms`.

### Erkennt echte Klatscher, löst aber nicht aus

Wenn im Log immer wieder nur **„1. Klatscher akzeptiert“** erscheint, passt meist das Zeitfenster nicht.

Dann kannst du beispielsweise versuchen:

```text
min_gap_ms: 150
max_gap_ms: 1000
```

### Erkennt gar nichts

Senke zuerst vorsichtig:

```text
peak_threshold
rms_threshold
```

Danach im Log prüfen, ob wieder `Klatsch-Kandidat` erscheint.

## Audioquelle

Beim Start listet die App die verfügbaren PulseAudio-Quellen auf und sucht nach `device_match`.

Für den Jabra Link 390 sieht der Eingang beispielsweise so aus:

```text
alsa_input.usb-_Jabra_Link_390_...mono-fallback
```

## Assist Satellite

Die App kann parallel zu Home Assistant Assist Satellite laufen. Assist Satellite kann weiterhin Wakewords und Sprachbefehle verarbeiten, während Jabra Double Clap denselben Audio-Stack für die Klatscherkennung nutzt.

## Datenschutz

- Keine Audiodateien werden gespeichert.
- Keine Sprache wird transkribiert.
- Es werden nur laufend Signalwerte berechnet.
- Der Webhook sollte mit `local_only: true` verwendet werden.

## Hinweise

Die App ist derzeit **experimentell**. Unterschiedliche Räume, Mikrofonpositionen, Fernseher, Musik und andere impulsartige Geräusche können das Ergebnis beeinflussen.

**Entwickelt von Filo**
