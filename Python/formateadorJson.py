import json
import re

# Rutas ajustadas con '/' en lugar de '\'
ruta_input = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/consultaGeminiDatosP.json"
ruta_output = "C:/Proyectos/Demo-Huawei-DeepSeek/Json/DatosFichaTecnica.json"

def es_json_valido(texto):
    #Verifica si el string es un JSON válido."""
    try:
        json.loads(texto)
        return True
    except json.JSONDecodeError:
        return False

def convertir_texto_a_json(texto):
    #Convierte texto plano tipo 'clave: valor,' a diccionario.
    diccionario = {}
    # Divide por comas, elimina espacios o saltos de línea
    pares = re.split(r',\s*\n?', texto.strip())
    for par in pares:
        if ':' in par:
            clave, valor = par.split(':', 1)
            diccionario[clave.strip()] = valor.strip()
    return diccionario

def formatear_respuesta_ia(ruta_entrada, ruta_salida):
    #Procesa archivo de entrada y genera JSON formateado en salida."""
    with open(ruta_entrada, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    texto_respuesta = datos.get("respuestaIA", "")

    if es_json_valido(texto_respuesta):
        resultado = json.loads(texto_respuesta)
    else:
        resultado = convertir_texto_a_json(texto_respuesta)

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"JSON generado en: {ruta_salida}")
    return resultado

# Ejecutar si se desea probar directamente
if __name__ == "__main__":
    formatear_respuesta_ia(ruta_input, ruta_output)
