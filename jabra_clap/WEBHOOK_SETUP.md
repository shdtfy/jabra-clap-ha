# Webhook-Sicherheit

Ab Version 1.0.8 enthält das öffentliche Repository **keine feste Webhook-ID mehr**.

Die `webhook_id` ist eine Pflichtangabe in der App-Konfiguration und wird in Home Assistant als Passwortfeld behandelt.

Für deine eigene Installation kannst du zum Beispiel diese zufällig erzeugte ID verwenden:

`jabra_double_clap_DEINE_ZUFALLS_ID`

Verwende exakt dieselbe ID in deiner Home-Assistant-Automation:

```yaml
triggers:
  - trigger: webhook
    webhook_id: DEINE_WEBHOOK_ID
    allowed_methods:
      - POST
    local_only: true
```

Behandle die Webhook-ID wie ein Passwort und veröffentliche sie nicht im Repository.
