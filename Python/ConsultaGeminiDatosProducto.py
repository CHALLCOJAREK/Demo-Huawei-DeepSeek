import json
import datetime
import os
import re
import google.generativeai as genai
import time

# Inicializa la API Key de Gemini
API_KEY = "AIzaSyCvKbqbTGBRmom8AkY8V8c8bSOXIU6XtgE"
genai.configure(api_key=API_KEY)

# === Función para consultar Gemini ===
def consultar_gemini(prompt_ia, datos):
    print("🧠 Generando contenido con base en el análisis solicitado")
    time.sleep(0.6)

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(f"{prompt_ia}\n\nAquí están los datos:\n{datos}")
        return response.text
    except Exception as e:
        print(f"Error al consultar Gemini: {str(e)}")
        return None

# === Detecta si un string es JSON válido ===
def es_json_valido(texto):
    try:
        json.loads(texto)
        return True
    except json.JSONDecodeError:
        return False

# === Convierte texto tipo clave: valor, a JSON dict ===
def convertir_texto_a_json(texto):
    diccionario = {}
    pares = re.split(r',\s*\n?', texto.strip())
    for par in pares:
        if ':' in par:
            clave, valor = par.split(':', 1)
            diccionario[clave.strip()] = valor.strip()
    return diccionario

# === Procesa JSON de entrada, consulta Gemini y limpia respuesta ===
def procesar_json(ruta_archivo):
    print("📂 Iniciando carga del archivo JSON")
    time.sleep(0.6)

    if not os.path.exists(ruta_archivo) or os.path.getsize(ruta_archivo) == 0:
        print(f"[{datetime.datetime.now()} - ERROR - El archivo no existe o está vacío: {ruta_archivo}")
        return

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = json.load(f)
            print("✅ Archivo JSON cargado correctamente")
            time.sleep(0.6)

    except json.decoder.JSONDecodeError as e:
        print(f"Error al leer el JSON: {str(e)}")
        return

    prompt_ia = contenido.get("promptIA", "").strip()
    datos = contenido.get("datos", "").strip()
    print("💡 Prompt IA recibido y registrado")
    time.sleep(0.6)

    print("📊 Datos cargados y listos para procesar")
    time.sleep(0.6)

    if not prompt_ia or not datos:
        print(f"Faltan datos en el JSON.")
        return

    respuesta = consultar_gemini(prompt_ia, datos)
    if respuesta:
        contenido["respuestaIA"] = respuesta
        print("📩 Respuesta de Gemini recibida con éxito")
        time.sleep(0.6)

    else:
        print(f"No se obtuvo respuesta de Gemini.")
        return

    try:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(contenido, f, ensure_ascii=False, indent=4)
        print("🔄 Archivo JSON actualizado correctamente")
        time.sleep(0.6)
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {str(e)}")

    # Formatear respuestaIA como JSON limpio
    texto_respuesta = contenido.get("respuestaIA", "")
    if es_json_valido(texto_respuesta):
        resultado = json.loads(texto_respuesta)
    else:
        resultado = convertir_texto_a_json(texto_respuesta)

    ruta_salida = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/DatosFichaTecnica.json"
    try:
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
        print("🧹 JSON limpio guardado exitosamente")
        time.sleep(0.6)

    except Exception as e:
        print(f"Error al guardar archivo limpio: {str(e)}")

# === Ejecutar ===
ruta = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/consultaGeminiDatosP.json"
procesar_json(ruta)
