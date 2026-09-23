# Double Clap

![Double Clap](logo.png)

**Lokale Doppelklatsch-Erkennung für Home Assistant · entwickelt von Filo**

Double Clap überwacht einen PulseAudio-kompatiblen Mikrofoneingang und erkennt zwei kurze, scharfe Klatschimpulse. Bei erfolgreicher Erkennung wird ein lokaler Home-Assistant-Webhook ausgelöst.

### Merkmale

- Automatische Auswahl der Standard-Audioquelle
- Manuelle Mikrofonwahl über `device_match`
- Doppelklatschen statt einfacher Lautstärkeschwelle
- Peak-, RMS-, Rise-Factor-, Crest-Factor- und Sharpness-Auswertung
- Einstellbares Zeitfenster zwischen beiden Klatschern
- Lokaler Webhook
- Keine Audioaufzeichnung
- Geeignet zur parallelen Nutzung mit Assist Satellite

### Getestet mit

- Jabra Speak2 75
- Jabra Link 390

Andere PulseAudio-kompatible Mikrofone können ebenfalls funktionieren.

Weitere Hinweise findest du im Tab **Dokumentation**.
