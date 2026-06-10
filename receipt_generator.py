from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
import os
import io

FONDO_PATH = "img/fondo.jpeg"

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}


def fecha_actual() -> str:
    now = datetime.now()
    hora = now.strftime("%I:%M %p").lstrip("0")
    hora = hora.replace("AM", "a. m.").replace("PM", "p. m.")
    return f"{now.day} de {MESES[now.month]} de {now.year} a las {hora}"


def referencia_aleatoria() -> str:
    return "M" + str(random.randint(10000000, 99999999))


def formatear_monto(monto: str) -> tuple:
    """Devuelve (simbolo, numero) por separado para control de espaciado."""
    try:
        valor = float(monto.replace(",", "."))
        entero = int(valor)
        decimales = round((valor - entero) * 100)
        entero_fmt = f"{entero:,}".replace(",", ".")
        return ("$", f"{entero_fmt},{decimales:02d}")
    except Exception:
        return ("$", monto)


def cargar_fuente(nombre: str, size: int) -> ImageFont.FreeTypeFont:
    rutas = [
        # Fuente empaquetada en el proyecto (funciona en Render/Linux)
        os.path.join(os.path.dirname(__file__), "fonts", "Roboto-Regular.ttf"),
        # Fallback Windows
        f"C:/Windows/Fonts/arial.ttf",
        f"C:/Windows/Fonts/arialbd.ttf",
        # Fallback Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for ruta in rutas:
        if os.path.exists(ruta):
            return ImageFont.truetype(ruta, size)
    return ImageFont.load_default()


def generar_comprobante(nombre: str, monto: str) -> io.BytesIO:
    # Cargar la plantilla SIN redimensionar (574 x 1156 px)
    img = Image.open(FONDO_PATH).convert("RGB")
    W, H = img.size  # 574 x 1156

    draw = ImageDraw.Draw(img)

    # ── Fuentes (tamaño proporcional a 574px de ancho) ────────────────────────
    f_nombre = cargar_fuente("arial.ttf", 22)   # normal, igual que fecha
    f_valor  = cargar_fuente("arial.ttf", 22)   # normal, igual que fecha
    f_fecha  = cargar_fuente("arial.ttf", 20)
    f_ref    = cargar_fuente("arial.ttf", 20)   # referencia más pequeña

    NEGRO = (25, 25, 25)

    # ── Coordenadas calculadas para 574 x 1156 ───────────────────────────────
    X = 44  # margen izquierdo

    simbolo, numero = formatear_monto(monto)
    y_monto = int(H * 0.518)

    datos = [
        (nombre,                 f_nombre, X,      int(H * 0.454)),
        (fecha_actual(),         f_fecha,  41,     int(H * 0.582)),
        (referencia_aleatoria(), f_ref,    X,      int(H * 0.648)),
    ]

    for texto, fuente, x, y in datos:
        draw.text((x, y), texto, font=fuente, fill=NEGRO)

    # Monto: $ y número separados con 5px de espacio exacto
    draw.text((X, y_monto), simbolo, font=f_valor, fill=NEGRO)
    ancho_simbolo = f_valor.getlength(simbolo)
    draw.text((X + ancho_simbolo + 2, y_monto), numero, font=f_valor, fill=NEGRO)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
