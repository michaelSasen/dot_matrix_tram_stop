import time
from PIL import ImageFont
from luma.core.render import canvas
from luma.emulator.device import pygame as pygame_emulator
from entur_departures import get_departures

device = pygame_emulator(width=64, height=16, rotate=0, mode="1", transform="scale2x")
font = ImageFont.truetype("DejaVuSans.ttf", 12)

REFRESH_INTERVAL = 10  # seconds

def build_text():
    return "   ".join(get_departures())

text = build_text()
with canvas(device) as draw:
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

y = max(0, (device.height - text_height) // 2)
x = device.width
last_fetch = time.time()
refresh_due = False

try:
    while True:
        if time.time() - last_fetch > REFRESH_INTERVAL:
            refresh_due = True

        with canvas(device) as draw:
            draw.text((x, y), text, font=font, fill="white")

        x -= 2
        if x < -text_width:
            if refresh_due:
                text = build_text()
                with canvas(device) as draw:
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                last_fetch = time.time()
                refresh_due = False
            x = device.width

        time.sleep(0.014)
except KeyboardInterrupt:
    pass