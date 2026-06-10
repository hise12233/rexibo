"""
Genera una imagen de prueba con datos ficticios para verificar posiciones.
Abre img/preview.png para ver el resultado.
"""
from receipt_generator import generar_comprobante

with open("img/preview.png", "wb") as f:
    f.write(generar_comprobante("Didier Gomez", "100000").read())

print("Vista previa guardada en img/preview.png — ábrela para verificar.")
