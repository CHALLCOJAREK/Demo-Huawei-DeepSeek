import json
import datetime
import os
import re
import requests
import pdfplumber
from io import BytesIO
import google.generativeai as genai
import time

# === CONFIGURACIÓN DE RUTAS ===
PDF_JSON_INPUT = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/urlPDF.json"
PROMPT_JSON_INPUT = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/consultaGeminiDatosP.json"
JSON_OUTPUT_LIMPIO = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/DatosFichaTecnica.json"

# === CONFIGURACIÓN DE GEMINI ===
API_KEY = "AIzaSyCvKbqbTGBRmom8AkY8V8c8bSOXIU6XtgE"
genai.configure(api_key=API_KEY)


# === FUNCIONES AUXILIARES ===

def consultar_gemini(prompt_ia, datos):
    print("⚙️ Generando contenido con Gemini")
    time.sleep(0.6)

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(f"{prompt_ia}\n\nAquí están los datos:\n{datos}")
        return response.text
    except Exception as e:
        print(f"Error al consultar Gemini: {str(e)}")
        return None


def es_json_valido(texto):
    try:
        json.loads(texto)
        return True
    except json.JSONDecodeError:
        return False


def convertir_texto_a_json(texto):
    diccionario = {}
    pares = re.split(r',\s*\n?', texto.strip())
    for par in pares:
        if ':' in par:
            clave, valor = par.split(':', 1)
            diccionario[clave.strip()] = valor.strip()
    return diccionario


def extraer_texto_pdf(url):
    print("📥 Descargando PDF...")
    time.sleep(0.6)

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"No se pudo descargar el PDF. Código de estado: {response.status_code}")

    texto_completo = ""
    with pdfplumber.open(BytesIO(response.content)) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            if texto:
                texto = re.sub(r"https?://\S+|www\.\S+", '', texto)
                texto = re.sub(r"\byoutube\b", '', texto, flags=re.IGNORECASE)
                texto = texto.replace("\n", " - ")
                texto = re.sub(r"[\"']", '', texto)
                texto_completo += texto
    return texto_completo.strip()


# === SCRIPT PRINCIPAL ===

def main():
    # Leer URL del PDF
    with open(PDF_JSON_INPUT, "r", encoding="utf-8") as f:
        data_url = json.load(f)
        url_pdf = data_url.get("urlPDF")

    if not url_pdf:
        print("No se encontró 'urlPDF' en el JSON.")
        return

    # Extraer texto del PDF
    texto_extraido = extraer_texto_pdf(url_pdf)

    # Leer prompt y preparar datos
    if not os.path.exists(PROMPT_JSON_INPUT):
        print("Archivo con promptIA no encontrado.")
        return

    with open(PROMPT_JSON_INPUT, "r", encoding="utf-8") as f:
        contenido = json.load(f)

    prompt_ia = contenido.get("promptIA", "").strip()
    if not prompt_ia:
        print("No se encontró 'promptIA' en el JSON.")
        return

    # Consultar Gemini
    respuesta = consultar_gemini(prompt_ia, texto_extraido)
    if respuesta:
        contenido["datos"] = texto_extraido
        contenido["respuestaIA"] = respuesta
    else:
        print("No se recibió respuesta de Gemini.")
        return

    # Guardar resultado en archivo original
    with open(PROMPT_JSON_INPUT, "w", encoding="utf-8") as f:
        json.dump(contenido, f, ensure_ascii=False, indent=4)
    print("📝 Archivo actualizado con respuesta de Gemini")
    time.sleep(0.6)


    # Intentar guardar la respuesta como JSON limpio
    texto_respuesta = contenido.get("respuestaIA", "")
    if es_json_valido(texto_respuesta):
        resultado = json.loads(texto_respuesta)
    else:
        resultado = convertir_texto_a_json(texto_respuesta)

    with open(JSON_OUTPUT_LIMPIO, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)
    print("🧹 JSON limpio guardado correctamente")
    time.sleep(0.6)



# === EJECUCIÓN ===
if __name__ == "__main__":
    main()
