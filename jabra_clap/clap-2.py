import array
import json
import math
import re
import subprocess
import time
import urllib.request

with open("/data/options.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

device_match = str(cfg.get("device_match", "Jabra Link 390"))
peak_threshold = float(cfg.get("peak_threshold", 0.55))
rms_threshold = float(cfg.get("rms_threshold", 0.08))
rise_factor = float(cfg.get("rise_factor", 3.5))
min_crest_factor = float(cfg.get("min_crest_factor", 3.4))
min_sharpness = float(cfg.get("min_sharpness", 0.55))
max_pulse_ms = int(cfg.get("max_pulse_ms", 120))
min_gap = int(cfg.get("min_gap_ms", 180)) / 1000.0
max_gap = int(cfg.get("max_gap_ms", 650)) / 1000.0
cooldown = int(cfg.get("cooldown_ms", 2500)) / 1000.0
webhook_id = str(cfg["webhook_id"])

def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

def find_source() -> str:
    output = subprocess.check_output(
        ["pactl", "list", "short", "sources"],
        text=True
    )

    print("Verfügbare Audioquellen:")
    print(output.rstrip())

    wanted = normalize(device_match)
    candidates = []

    for line in output.splitlines():
        if not line.strip():
            continue

        fields = line.split("\t")
        if len(fields) < 2:
            continue

        name = fields[1]
        if ".monitor" in name:
            continue

        candidates.append(name)

        if wanted in normalize(line):
            print(f"Passende Audioquelle gefunden: {name}")
            return name

    raise RuntimeError(
        f"Keine Audioquelle passend zu '{device_match}' gefunden. "
        f"Gefundene Eingänge: {', '.join(candidates) or 'keine'}"
    )

def trigger_webhook(peak: float, rms: float, crest: float, sharpness: float, gap_ms: int) -> None:
    url = f"http://homeassistant:8123/api/webhook/{webhook_id}"

    payload = json.dumps({
        "source": device_match,
        "peak": round(peak, 3),
        "rms": round(rms, 3),
        "crest_factor": round(crest, 2),
        "sharpness": round(sharpness, 2),
        "gap_ms": gap_ms,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=5) as response:
        response.read()

    print(
        f"DOPPELKLATSCH ERKANNT -> Webhook ausgelöst "
        f"(Abstand {gap_ms} ms)"
    )

source = find_source()

print(f"Benutze Mikrofon: {source}")
print(f"Peak Threshold: {peak_threshold}")
print(f"RMS Threshold: {rms_threshold}")
print(f"Rise Factor: {rise_factor}")
print(f"Min Crest Factor: {min_crest_factor}")
print(f"Min Sharpness: {min_sharpness}")
print(f"Max Pulsdauer: {max_pulse_ms} ms")
print(f"Doppelklatsch-Fenster: {int(min_gap*1000)}-{int(max_gap*1000)} ms")
print(f"Cooldown: {int(cooldown*1000)} ms")
print(f"Webhook-ID: {webhook_id}")

proc = subprocess.Popen([
    "parec",
    "--device=" + source,
    "--format=s16le",
    "--rate=16000",
    "--channels=1",
    "--raw"
], stdout=subprocess.PIPE)

chunk_samples = 320          # 20 ms bei 16 kHz
chunk_bytes = chunk_samples * 2
chunk_ms = 20

baseline = 0.01
last_event = 0.0
first_clap = None

pulse_active = False
pulse_start = 0.0
pulse_peak = 0.0
pulse_rms_max = 0.0
pulse_crest_max = 0.0
pulse_sharpness_max = 0.0

def classify_pulse(now: float):
    global pulse_active, pulse_start, pulse_peak, pulse_rms_max
    global pulse_crest_max, pulse_sharpness_max, first_clap, last_event

    if not pulse_active:
        return

    duration_ms = int((now - pulse_start) * 1000)

    is_clap = (
        duration_ms <= max_pulse_ms
        and pulse_peak >= peak_threshold
        and pulse_rms_max >= rms_threshold
        and pulse_crest_max >= min_crest_factor
        and pulse_sharpness_max >= min_sharpness
    )

    if is_clap:
        print(
            f"Klatsch-Kandidat: peak={pulse_peak:.3f}, "
            f"rms={pulse_rms_max:.3f}, "
            f"crest={pulse_crest_max:.2f}, "
            f"sharpness={pulse_sharpness_max:.2f}, "
            f"dauer={duration_ms}ms"
        )

        if now - last_event >= cooldown:
            if first_clap is None:
                first_clap = now
                print("1. Klatscher akzeptiert")
            else:
                gap = now - first_clap
                gap_ms = round(gap * 1000)

                if min_gap <= gap <= max_gap:
                    print(f"2. Klatscher akzeptiert, Abstand={gap_ms}ms")
                    try:
                        trigger_webhook(
                            pulse_peak,
                            pulse_rms_max,
                            pulse_crest_max,
                            pulse_sharpness_max,
                            gap_ms,
                        )
                        last_event = now
                    except Exception as err:
                        print(f"Fehler beim Auslösen des Webhooks: {err}")

                    first_clap = None

                elif gap > max_gap:
                    first_clap = now
                    print("Zu großer Abstand -> dieser Klatscher wird neuer erster Klatscher")

    pulse_active = False
    pulse_start = 0.0
    pulse_peak = 0.0
    pulse_rms_max = 0.0
    pulse_crest_max = 0.0
    pulse_sharpness_max = 0.0

try:
    while True:
        raw = proc.stdout.read(chunk_bytes)

        if not raw or len(raw) < chunk_bytes:
            if proc.poll() is not None:
                raise RuntimeError(
                    f"parec wurde beendet (Exit-Code {proc.returncode})"
                )
            time.sleep(0.02)
            continue

        samples = array.array("h")
        samples.frombytes(raw)

        if not samples:
            continue

        # Grundwerte
        abs_samples = [abs(sample) for sample in samples]
        peak = max(abs_samples) / 32768.0
        rms = math.sqrt(
            sum(sample * sample for sample in samples) / len(samples)
        ) / 32768.0

        # Crest Factor: Klatschen hat typischerweise einen deutlich höheren
        # Spitzenwert als Durchschnittspegel.
        crest = peak / max(rms, 0.0001)

        # "Sharpness": mittlere schnelle Sample-Änderung relativ zum Pegel.
        # Breitbandige, scharfe Transienten (Klatschen) liegen höher als Sprache.
        if len(samples) > 1:
            diff_mean = sum(
                abs(samples[i] - samples[i - 1])
                for i in range(1, len(samples))
            ) / (len(samples) - 1)
            mean_abs = sum(abs_samples) / len(abs_samples)
            sharpness = diff_mean / max(mean_abs, 1.0)
        else:
            sharpness = 0.0

        now = time.monotonic()

        # Baseline nur bei normalem Raumpegel langsam nachführen.
        if not pulse_active and rms < max(rms_threshold * 0.75, baseline * 2.0):
            baseline = baseline * 0.99 + rms * 0.01

        # Kandidat startet nur bei deutlichem, plötzlichem Anstieg.
        start_candidate = (
            peak >= peak_threshold
            and rms >= rms_threshold
            and rms >= max(0.003, baseline * rise_factor)
            and crest >= min_crest_factor
            and sharpness >= min_sharpness
        )

        if not pulse_active and start_candidate:
            pulse_active = True
            pulse_start = now
            pulse_peak = peak
            pulse_rms_max = rms
            pulse_crest_max = crest
            pulse_sharpness_max = sharpness
            continue

        if pulse_active:
            pulse_peak = max(pulse_peak, peak)
            pulse_rms_max = max(pulse_rms_max, rms)
            pulse_crest_max = max(pulse_crest_max, crest)
            pulse_sharpness_max = max(pulse_sharpness_max, sharpness)

            duration_ms = int((now - pulse_start) * 1000)

            # Ein echter Klatscher fällt schnell wieder ab.
            if rms < rms_threshold * 0.45:
                classify_pulse(now)
            elif duration_ms > max_pulse_ms:
                # Zu lang = eher Sprache/Musik/anhaltendes Geräusch.
                pulse_active = False
                pulse_start = 0.0
                pulse_peak = 0.0
                pulse_rms_max = 0.0
                pulse_crest_max = 0.0
                pulse_sharpness_max = 0.0

        if first_clap is not None and now - first_clap > max_gap:
            first_clap = None

finally:
    proc.terminate()
