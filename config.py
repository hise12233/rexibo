import os

# Token leído desde variable de entorno (para Render y producción)
# En local puedes crear un archivo .env o setearla manualmente
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8656134175:AAG_6bbKytWW1CWACTQvtvAOWPWUSiGt96k")

# Información de la empresa/negocio
EMPRESA = "Mi Negocio"
DIRECCION = "Calle Ejemplo 123"
TELEFONO = "+1 234 567 890"
EMAIL = "contacto@minegocio.com"

# Ruta de la imagen de fondo
FONDO_PATH = "img/fondo.jpeg"
