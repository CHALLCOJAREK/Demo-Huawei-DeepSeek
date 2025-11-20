import os
import json
import pdfkit

# Ruta base del proyecto
#BASE_DIR = os.path.dirname(os.path.abspath(_file_)).replace("\\", "/")

# Ruta del archivo JSON de datos
json_path = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/DatosFichaTecnica.json"

# Leer el JSON para obtener el nombre del producto
try:
    with open(json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        nombre_producto = data.get("nombreProductoD", "FichaTecnica").replace("/", "").replace("\\", "")
except Exception as e:
    print(f"❌ Error al leer el JSON: {e}")
    nombre_producto = "FichaTecnica"

# Rutas del HTML y del PDF
input_html = "C:/Proyectos/Demo-Huawei-DeepSeek/Plantillas/PlantillaFichaTecnica.html"
output_dir = "C:/Proyectos/Demo-Huawei-DeepSeek/PDF"
output_pdf = f"{output_dir}/{nombre_producto}.pdf"

# Asegurar que el directorio de salida existe
os.makedirs(output_dir, exist_ok=True)

# Verificar si el HTML existe
if not os.path.exists(input_html.replace("/", "\\")):
    print(f"❌ Archivo HTML no encontrado: {input_html}")
    exit(1)

# Opciones para PDF
options = {
    'page-size': 'Letter',
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
    'encoding': 'UTF-8',
    'zoom': '1.15',
    'no-outline': None,
    'enable-local-file-access': ''
}

try:
    config = pdfkit.configuration(wkhtmltopdf="C:/Proyectos/Demo-Huawei-DeepSeek/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdfkit.from_file(input_html, output_pdf, options=options, configuration=config)
    print(f"✅ PDF generado exitosamente")

    # Guardar ruta del PDF en un JSON
    ruta_pdf_json = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/RutaPDF.json"
    with open(ruta_pdf_json, 'w', encoding='utf-8') as ruta_file:
        json.dump({"rutaPDF": output_pdf}, ruta_file, indent=4, ensure_ascii=False)
    print(f"📁 Ruta del PDF guardada")

except Exception as e:
    print("❌ Error al generar PDF:")
    print(str(e))