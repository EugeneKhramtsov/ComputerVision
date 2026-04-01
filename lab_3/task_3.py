from PIL import Image
import numpy as np
import math
from types import MappingProxyType

classic_sepia_coef = MappingProxyType(
    {
        "rr": 0.393, "rg": 0.769, "rb": 0.189,
        "gr": 0.349, "gg": 0.686, "gb": 0.168,
        "br": 0.272, "bg": 0.534, "bb": 0.131
    }
)

def sepia_pixel(r, g, b, sepia_coef = classic_sepia_coef):
    r_new = sepia_coef["rr"] * r + sepia_coef["rg"] * g + sepia_coef["rb"] * b
    g_new = sepia_coef["gr"] * r + sepia_coef["gg"] * g + sepia_coef["gb"] * b
    b_new = sepia_coef["br"] * r + sepia_coef["bg"] * g + sepia_coef["bb"] * b

    return (
        min(255, int(r_new)),
        min(255, int(g_new)),
        min(255, int(b_new))
    )

def white_fade_effect(c, d):
    return min(255, int(c + (c * (d ** 3)))) # не лінійне вицвітання від центру

image = Image.open("origin.jpg")
width = image.size[0]
height = image.size[1]
pixels = np.array(image)

center_x = width // 2
center_y = height // 2

for i in range(height):
    for j in range(width):
        r, g, b = map(int, pixels[i, j])

        r, g, b = sepia_pixel(r, g, b)

        d = math.sqrt((i - center_y) ** 2 + (j - center_x) ** 2)
        d = d / math.sqrt(center_x ** 2 + center_y ** 2)

        r = white_fade_effect(r, d)
        g = white_fade_effect(g, d)
        b = white_fade_effect(b, d)

        pixels[i, j] = [r, g, b]

result = Image.fromarray(pixels)
result.show()
result.save("processed.jpg")