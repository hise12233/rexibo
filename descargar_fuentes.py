import urllib.request
import os

os.makedirs("fonts", exist_ok=True)

fuentes = {
    "fonts/Roboto-Regular.ttf": "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Regular.ttf",
}

for path, url in fuentes.items():
    print(f"Descargando {path}...")
    urllib.request.urlretrieve(url, path)
    print(f"  OK ({os.path.getsize(path)} bytes)")

print("\nFuentes descargadas correctamente.")
