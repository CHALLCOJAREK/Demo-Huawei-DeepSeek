import json
import os
import time

# Ruta del archivo JSON de entrada
json_input_path = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/consultaGeminiDatosP.json"
json_input_path = json_input_path.replace("\\", "/")  # Asegurar uso de slash normal

# Ruta del archivo JSON de salida
json_output_path = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/DatosFichaTecnica.json"
json_output_path = json_output_path.replace("\\", "/")  # Asegurar uso de slash normal

print(f"📂 Cargando JSON de entrada...")
with open(json_input_path, "r", encoding="utf-8") as f:
    data_input = json.load(f)
time.sleep(0.6)

respuesta_ia = data_input.get("respuestaIA")

if respuesta_ia:
    print("🧹 Limpiando contenido JSON de 'respuestaIA'...")
    cleaned_json_str = respuesta_ia.replace("```json\n", "").replace("\n```", "").strip()
    time.sleep(0.6)

    try:
        print("🔍 Procesando JSON limpio...")
        datos_ficha_tecnica = json.loads(cleaned_json_str)
        time.sleep(0.6)

        print(f"💾 Guardando datos en: {json_output_path}")
        with open(json_output_path, "w", encoding="utf-8") as f:
            json.dump(datos_ficha_tecnica, f, ensure_ascii=False, indent=4)
        time.sleep(0.6)

        print("✅ Datos movidos exitosamente.")
    except json.JSONDecodeError:
        print("❌ Error al procesar el JSON contenido en 'respuestaIA'. Asegúrate de que esté bien formado.")
else:
    print("❌ No se encontró el campo 'respuestaIA' en el archivo JSON de entrada.")
