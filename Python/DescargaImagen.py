import requests
from PIL import Image
from io import BytesIO
import json
import os
import time

# Ruta al archivo JSON con la config (nombre + url)
JSON_CONFIG = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/nombreImagenLB.json"

# Carpeta donde se guardará la imagen descargada
CARPETA_SALIDA = "C:/Proyectos/Demo-Huawei-DeepSeek/DescargasImagenes"

# Cargar la configuración desde el archivo JSON
with open(JSON_CONFIG, "r", encoding="utf-8") as f:
    config = json.load(f)

url = config.get("url")
nombre_base = config.get("nombre_imagen", "imagen_predeterminada")

if not url:
    raise ValueError("El campo 'url' no está definido en el archivo JSON.")

os.makedirs(CARPETA_SALIDA, exist_ok=True)

# Nombre completo de la imagen de salida
nombre_archivo = f"{nombre_base}.jpg"
ruta_salida = os.path.join(CARPETA_SALIDA, nombre_archivo)

print("📥 Descargando imagen...")
time.sleep(0.6)

respuesta = requests.get(url)

if respuesta.status_code == 200:
    imagen = Image.open(BytesIO(respuesta.content)).convert("RGB")
    imagen.save(ruta_salida, "JPEG")
    print("💾 Imagen guardada correctamente")
    time.sleep(0.6)

    # Actualizar el JSON con el nombre del archivo guardado
    config["nombre_Archivo"] = nombre_archivo
    with open(JSON_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
else:
    print(f"Error al descargar la imagen: {respuesta.status_code}")
