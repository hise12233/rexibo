"""
Ejecuta este script para ver las dimensiones reales de tu fondo.jpeg
y generar una imagen de prueba con puntos de referencia numerados.
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONDO_PATH = "img/fondo.jpeg"

img = Image.open(FONDO_PATH).convert("RGB")
W, H = img.size
print(f"Tamaño real de fondo.jpeg: {W} x {H} px")

draw = ImageDraw.Draw(img)

# Dibujar una cuadrícula cada 50px para calibrar coordenadas
for x in range(0, W, 50):
    draw.line([(x, 0), (x, H)], fill=(200, 0, 0, 100), width=1)
    draw.text((x + 2, 2), str(x), fill=(200, 0, 0))

for y in range(0, H, 50):
    draw.line([(0, y), (W, y)], fill=(0, 0, 200, 100), width=1)
    draw.text((2, y + 2), str(y), fill=(0, 0, 200))

img.save("img/calibracion.png")
print("Imagen guardada en img/calibracion.png")
print("Abre esa imagen y fíjate en las coordenadas X,Y donde van los textos.")
