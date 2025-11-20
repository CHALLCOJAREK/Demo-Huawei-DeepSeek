import os
import re

ruta_carpeta = r"C:\Proyectos\Demo-Huawei-DeepSeek\Python"

# Regex para encoding en open(), json.load(), json.dump()
patron_open = re.compile(r"open\(([^)]*?)encoding\s*=\s*['\"]([a-zA-Z0-9_\-]+)['\"]")
patron_encode = re.compile(r"\.encode\(['\"]([a-zA-Z0-9_\-]+)['\"]\)")
patron_decode = re.compile(r"\.decode\(['\"]([a-zA-Z0-9_\-]+)['\"]\)")

archivos_py = []
for root, _, files in os.walk(ruta_carpeta):
    for archivo in files:
        if archivo.endswith(".py"):
            archivos_py.append(os.path.join(root, archivo))

print(f"\n📂 Archivos Python encontrados: {len(archivos_py)}\n")

total = 0

for archivo in archivos_py:
    with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()
        codificaciones = []

        for i, linea in enumerate(lineas, 1):
            match_open = patron_open.search(linea)
            match_enc = patron_encode.search(linea)
            match_dec = patron_decode.search(linea)

            if match_open:
                codificaciones.append((i, "open", match_open.group(2)))
            if match_enc:
                codificaciones.append((i, "encode", match_enc.group(1)))
            if match_dec:
                codificaciones.append((i, "decode", match_dec.group(1)))

        if codificaciones:
            print(f"📄 Archivo: {os.path.relpath(archivo, ruta_carpeta)}")
            for lin, tipo, cod in codificaciones:
                icono = "🔐" if tipo in ["open", "encode"] else "🔓"
                print(f"   {icono} {tipo} en línea {lin}: '{cod}'")
            print("-" * 50)
            total += len(codificaciones)

if total == 0:
    print("⚠️ No se detectó ninguna codificación ni decodificación con tipo explícito.")
else:
    print(f"\n✅ Se detectaron {total} usos de codificación/decodificación.\n")
