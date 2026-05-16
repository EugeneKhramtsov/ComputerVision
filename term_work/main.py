import numpy as np
from types import MappingProxyType
import cv2
import matplotlib.pyplot as plt

classic_sepia_coef = MappingProxyType(
    {
        "rr": 0.393, "rg": 0.769, "rb": 0.189,
        "gr": 0.349, "gg": 0.686, "gb": 0.168,
        "br": 0.272, "bg": 0.534, "bb": 0.131
    }
)

custom_sepia_coef = MappingProxyType(
    {
        "rr": 0.2, "rg": 0.2, "rb": 0.2,
        "gr": 0.1, "gg": 0.1, "gb": 0.1,
        "br": 0.6, "bg": 0.4, "bb": 1
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

image = cv2.imread("fields_1.jpg").astype(np.float32)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

height, width, _ = image_rgb.shape
pixels_rgb = np.array(image_rgb)

center_x = width // 2
center_y = height // 2

for i in range(height):
    for j in range(width):
        r, g, b = map(int, pixels_rgb[i, j])

        r, g, b = sepia_pixel(r, g, b, custom_sepia_coef)

        pixels_rgb[i, j] = [r, g, b]

image_sepia = pixels_rgb

pixels_bgr = cv2.cvtColor(pixels_rgb, cv2.COLOR_RGB2BGR)

Ix = cv2.Sobel(pixels_bgr, cv2.CV_32F, 1, 0, ksize=3)
Iy = cv2.Sobel(pixels_bgr, cv2.CV_32F, 0, 1, ksize=3)

magnitude = np.sqrt(Ix**2 + Iy**2)

image_sobel = cv2.cvtColor(magnitude, cv2.COLOR_RGB2BGR)

# -------------------------
# Display all images
# -------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Original
axes[0].imshow(image_rgb.astype(np.uint8))
axes[0].set_title("Original")
axes[0].axis("off")

# Sepia
axes[1].imshow(image_sepia.astype(np.uint8))
axes[1].set_title("Sepia")
axes[1].axis("off")

# Sobel
axes[2].imshow(image_sobel.astype(np.uint8))
axes[2].set_title("Sobel")
axes[2].axis("off")

plt.tight_layout()
plt.show()