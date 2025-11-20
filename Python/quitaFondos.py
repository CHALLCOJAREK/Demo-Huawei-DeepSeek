from rembg import remove
from PIL import Image
import json
import os
import time

# Rutas
JSON_ORIGEN = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/nombreImagenLB.json"
JSON_SALIDA = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/imagenSinFondo.json"
CARPETA_INPUT = "C:/Proyectos/Demo-Huawei-DeepSeek/DescargasImagenes"
CARPETA_OUTPUT = "C:/Proyectos/Demo-Huawei-DeepSeek/ImagenesSinFondo"

print("📁 Verificando y creando carpeta de salida si es necesario...")
os.makedirs(CARPETA_OUTPUT, exist_ok=True)
time.sleep(0.6)

print(f"📂 Leyendo JSON de entrada: {JSON_ORIGEN}")
with open(JSON_ORIGEN, "r", encoding="utf-8") as f:
    datos = json.load(f)
time.sleep(0.6)

nombre_archivo_entrada = datos.get("nombre_Archivo")  # ejemplo: hola.jpg
if not nombre_archivo_entrada:
    raise ValueError("❌ No se encontró 'nombre_Archivo' en el JSON.")
print(f"📝 Nombre del archivo a procesar: {nombre_archivo_entrada}")
time.sleep(0.6)

input_path = os.path.join(CARPETA_INPUT, nombre_archivo_entrada)
nombre_sin_extension = os.path.splitext(nombre_archivo_entrada)[0]
output_filename = f"{nombre_sin_extension}.png"
output_path = os.path.join(CARPETA_OUTPUT, output_filename)
output_path_normalized = output_path.replace("\\", "/")

print(f"🖼️ Abriendo imagen: {input_path}")
input_image = Image.open(input_path)
time.sleep(0.6)

print("⚙️ Eliminando fondo de la imagen...")
output_image = remove(input_image)
time.sleep(0.6)

print(f"💾 Guardando imagen procesada en: {output_path}")
output_image.save(output_path)
time.sleep(0.6)

print(f"📄 Guardando ruta de imagen procesada en JSON: {JSON_SALIDA}")
with open(JSON_SALIDA, "w", encoding="utf-8") as f:
    json.dump({"ruta_Imagen_Procesada": output_path_normalized}, f, indent=4, ensure_ascii=False)
time.sleep(0.6)

print("✅ Proceso completado con éxito")

