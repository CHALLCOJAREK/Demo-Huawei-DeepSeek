import json
import datetime
import os
import google.generativeai as genai
import time

# Inicializa la API Key de Gemini
API_KEY = "AIzaSyCvKbqbTGBRmom8AkY8V8c8bSOXIU6XtgE"
genai.configure(api_key=API_KEY)

# Función para consultar Gemini usando la biblioteca oficial de Google
def consultar_gemini(prompt_ia, datos):
    print("🧠 Generando contenido con inteligencia artificial...")
    print(f"✍️ Prompt utilizado: {prompt_ia}")
    time.sleep(0.6)
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(f"{prompt_ia}\n\nAquí están los datos:\n{datos}")
        return response.text
    except Exception as e:
        print(f"Error al consultar Gemini: {str(e)}")
        return None

# Cargar archivo JSON
def procesar_json(ruta_archivo):
    print(f"📂 Cargando archivo JSON...")
    time.sleep(0.6)
    
    if not os.path.exists(ruta_archivo) or os.path.getsize(ruta_archivo) == 0:
        print(f"El archivo no existe o está vacío: {ruta_archivo}")
        return

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = json.load(f)
            print("✅ Archivo JSON cargado exitosamente")
            time.sleep(0.6)

    except json.decoder.JSONDecodeError as e:
        print(f"Error al leer el JSON: {str(e)}")
        return

    prompt_ia = contenido.get("promptIA", "").strip()
    datos = contenido.get("datos", "").strip()
    print(f"💭 Pensando en base al prompt...")
    time.sleep(0.6)

    print(f"📊 Datos: {datos}")
    time.sleep(0.6)

    if not prompt_ia or not datos:
        print(f"Faltan datos en el JSON")
        return

    respuesta = consultar_gemini(prompt_ia, datos)
    if respuesta:
        respuesta_limpia = respuesta.replace("\n", "")
        contenido["respuestaIA"] = respuesta_limpia
        print("🧹 Respuesta de Gemini obtenida y limpiada con éxito")
        time.sleep(0.6)


    else:
        print(f"No se obtuvo respuesta de Gemini.")
        return

    try:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(contenido, f, ensure_ascii=False, indent=4)
        print("💾 Archivo JSON actualizado exitosamente")
        time.sleep(0.6)

    except Exception as e:
        print(f"[{datetime.datetime.now()} - ERROR - Error al guardar el archivo JSON: {str(e)}]")

# Ruta del archivo JSON
ruta = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/consulta_gemini.json"
procesar_json(ruta)
