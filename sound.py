# video_to_sound.py
from PIL import Image
import numpy as np
import wave, glob, os
from os import system
FRAME_DIR = "cartoon_frames3"
OUT = "soundtrack.wav"

FPS = 20
SR = 44100

files = sorted(glob.glob(os.path.join(FRAME_DIR, "*.png")))
duration = len(files) / FPS
samples = int(duration * SR)

brightness = []
change = []

prev = None

for f in files:
    img = Image.open(f).convert("L").resize((64, 64))
    arr = np.asarray(img, dtype=np.float32) / 255.0

    brightness.append(arr.mean())

    if prev is None:
        change.append(0)
    else:
        change.append(np.abs(arr - prev).mean())

    prev = arr

brightness = np.array(brightness)
change = np.array(change)

brightness = (brightness - brightness.min()) / (np.ptp(brightness) + 1e-9)
change = (change - change.min()) / (np.ptp(change) + 1e-9)

t_frames = np.linspace(0, duration, len(files))
t_audio = np.linspace(0, duration, samples)

b = np.interp(t_audio, t_frames, brightness)
c = np.interp(t_audio, t_frames, change)

t = np.arange(samples) / SR

# slow organic drone
drone = np.sin(2 * np.pi * (55 + 25*b) * t)

# higher shimmer responding to visual change
shimmer = np.sin(2 * np.pi * (330 + 500*c) * t)

# pulse from frame-to-frame change
pulse = np.sin(2 * np.pi * (2 + 10*c) * t)
pulse = np.maximum(pulse, 0)

audio = (
    0.45 * drone * (0.4 + 0.6*b) +
    0.18 * shimmer * c +
    0.25 * pulse * c
)

### soft fade in/out
##fade = int(SR * 3)
##audio[:fade] *= np.linspace(0, 1, fade)
##audio[-fade:] *= np.linspace(1, 0, fade)

audio /= np.max(np.abs(audio)) + 1e-9
audio = (audio * 32767).astype(np.int16)

with wave.open(OUT, "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(audio.tobytes())

print(f"wrote {OUT}")

system('ffmpeg -i soundtrack.wav -codec:a libmp3lame -q:a 2 soundtrack.mp3')
system('ffmpeg -i blobs06.mp4 -i soundtrack.mp3 -shortest -c:v copy -c:a aac blobs06_sound.mp4')

