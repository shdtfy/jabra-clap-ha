# Webhook-Sicherheit

Double Clap enthält keine feste öffentliche Webhook-ID.

Die `webhook_id` ist eine Pflichtangabe in der App-Konfiguration und wird in Home Assistant als Passwortfeld behandelt.

Erstelle für deine Installation eine eigene lange und zufällige ID.

Beispiel:

`double_clap_DEINE_ZUFALLS_ID`

Verwende exakt dieselbe ID in deiner Home-Assistant-Automation:

```yaml
triggers:
  - trigger: webhook
    webhook_id: DEINE_WEBHOOK_ID
    allowed_methods:
      - POST
    local_only: true
```

Behandle die Webhook-ID wie ein Passwort und veröffentliche sie nicht.

Double Clap gibt die konfigurierte Webhook-ID nicht im App-Protokoll aus.
