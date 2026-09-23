import array
import json
import math
import os
import re
import subprocess
import time
import urllib.request

with open("/data/options.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

device_match = str(cfg.get("device_match", "Jabra Link 390"))
peak_threshold = float(cfg.get("peak_threshold", 0.30))
rms_threshold = float(cfg.get("rms_threshold", 0.035))
rise_factor = float(cfg.get("rise_factor", 2.5))
min_gap = int(cfg.get("min_gap_ms", 180)) / 1000.0
max_gap = int(cfg.get("max_gap_ms", 850)) / 1000.0
cooldown = int(cfg.get("cooldown_ms", 1800)) / 1000.0
token = os.environ["SUPERVISOR_TOKEN"]

def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

def find_source() -> str:
    output = subprocess.check_output(["pactl", "list", "short", "sources"], text=True)
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

def fire_event(peak: float, rms: float, gap_ms: int) -> None:
    payload = json.dumps({
        "source": device_match,
        "peak": round(peak, 3),
        "rms": round(rms, 3),
        "gap_ms": gap_ms,
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://supervisor/core/api/events/jabra_double_clap",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        response.read()

    print(f"DOPPELKLATSCH ERKANNT -> HA Event gesendet (Abstand {gap_ms} ms)")

source = find_source()

print(f"Benutze Mikrofon: {source}")
print(f"Peak Threshold: {peak_threshold}")
print(f"RMS Threshold: {rms_threshold}")
print(f"Rise Factor: {rise_factor}")
print(f"Doppelklatsch-Fenster: {int(min_gap * 1000)}-{int(max_gap * 1000)} ms")
print(f"Cooldown: {int(cooldown * 1000)} ms")

proc = subprocess.Popen([
    "parec",
    "--device=" + source,
    "--format=s16le",
    "--rate=16000",
    "--channels=1",
    "--raw",
], stdout=subprocess.PIPE)

chunk_samples = 320
chunk_bytes = chunk_samples * 2
baseline = 0.01
last_impulse = 0.0
first_clap = None
last_event = 0.0

try:
    while True:
        raw = proc.stdout.read(chunk_bytes)

        if not raw or len(raw) < chunk_bytes:
            if proc.poll() is not None:
                raise RuntimeError(f"parec wurde beendet (Exit-Code {proc.returncode})")
            time.sleep(0.02)
            continue

        samples = array.array("h")
        samples.frombytes(raw)
        if not samples:
            continue

        absolute = [abs(sample) for sample in samples]
        peak = max(absolute) / 32768.0
        rms = math.sqrt(sum(sample * sample for sample in samples) / len(samples)) / 32768.0
        now = time.monotonic()

        if rms < max(rms_threshold * 1.5, baseline * 2.0):
            baseline = baseline * 0.985 + rms * 0.015

        impulse = (
            peak >= peak_threshold
            and rms >= rms_threshold
            and rms >= max(0.001, baseline * rise_factor)
            and now - last_impulse > 0.10
        )

        if impulse:
            last_impulse = now

            if now - last_event < cooldown:
                continue

            if first_clap is None:
                first_clap = now
                print(f"1. Impuls: peak={peak:.3f}, rms={rms:.3f}, baseline={baseline:.3f}")
                continue

            gap = now - first_clap
            gap_ms = round(gap * 1000)
            print(
                f"2. Impuls: peak={peak:.3f}, rms={rms:.3f}, "
                f"baseline={baseline:.3f}, Abstand={gap_ms}ms"
            )

            if min_gap <= gap <= max_gap:
                try:
                    fire_event(peak, rms, gap_ms)
                    last_event = now
                except Exception as err:
                    print(f"Fehler beim Senden des HA Events: {err}")
                first_clap = None
            elif gap > max_gap:
                first_clap = now

        if first_clap is not None and now - first_clap > max_gap:
            first_clap = None
finally:
    proc.terminate()
