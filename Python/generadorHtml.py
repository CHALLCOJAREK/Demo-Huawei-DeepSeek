import json
import os
from pathlib import Path
import time

base_path = Path("C:/Proyectos/Demo-Huawei-DeepSeek/Json")
json_paths = {
    "ficha_tecnica": base_path / "DatosFichaTecnica.json",
    "gemini": base_path / "consulta_gemini.json",
    "beneficios": base_path / "consultaBeneficiosGIA.json"
}

# Directorio base para el HTML
base_dir = Path("C:/Proyectos/Demo-Huawei-DeepSeek/Plantillas")

# Leer los JSONs
data = {}
imagen_src = None

for key, path in json_paths.items():
    try:
        with open(path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        print("✅ JSON cargado exitosamente")
        time.sleep(0.6)

        if key == "ficha_tecnica":
            data.update(json_data)
            ruta_absoluta = json_data.get("rutaImagenProducto", "")
            if ruta_absoluta:
                ruta_absoluta = os.path.normpath(ruta_absoluta)
                if "ImagenesSinFondo" in ruta_absoluta:
                    relative_path = os.path.relpath(ruta_absoluta, base_dir).replace('\\', '/')
                    if os.path.exists(os.path.join(base_dir, relative_path)):
                        imagen_src = relative_path
                        print("🖼️ Imagen encontrada")
                        time.sleep(0.6)

                    else:
                        print(f"Error: La imagen {ruta_absoluta} no existe en {base_dir}")
                else:
                    print("Advertencia: Ruta de imagen no contiene 'ImagenesSinFondo', usando imagen por defecto")
            else:
                print("Advertencia: rutaImagenProducto vacía, usando imagen por defecto")

        elif key == "gemini":
            data["DescripcionGeneralD"] = json_data.get("respuestaIA", "")

        elif key == "beneficios":
            data["BeneficiosProducto"] = json_data.get("respuestaIA", "")

    except FileNotFoundError:
        print(f"Error: No se encontró {path}")
        if key == "ficha_tecnica":
            data = {}
        elif key == "gemini":
            data["DescripcionGeneralD"] = ""
        elif key == "beneficios":
            data["BeneficiosProducto"] = ""

    except json.JSONDecodeError:
        print(f"Error: {path} no es un JSON válido")
        if key == "ficha_tecnica":
            data = {}
        elif key == "gemini":
            data["DescripcionGeneralD"] = ""
        elif key == "beneficios":
            data["BeneficiosProducto"] = ""

    except Exception as e:
        print(f"Error al leer {path}: {str(e)}")
        if key == "ficha_tecnica":
            data = {}
        elif key == "gemini":
            data["DescripcionGeneralD"] = ""
        elif key == "beneficios":
            data["BeneficiosProducto"] = ""

# Procesar recomendaciones
recomendaciones = [r.strip() for r in data.get('recomendacionesUsoProductoD', '').split('. ') if r.strip()]
if not recomendaciones:
    recomendaciones = ["Sin recomendaciones"]

# Procesar beneficios
beneficios = []
beneficios_raw = data.get("BeneficiosProducto")

if isinstance(beneficios_raw, list):
    beneficios = [b.strip() for b in beneficios_raw if b.strip()]
elif isinstance(beneficios_raw, str) and beneficios_raw:
    beneficios = [b.strip() for b in beneficios_raw.split('. ') if b.strip()]
else:
    beneficios = [
        "Alta compatibilidad con pinturas alquídicas y de secado rápido.",
        "Ideal para acabados finos en automóviles.",
        "Fácil aplicación y dilución uniforme.",
        "Rápido secado para mayor eficiencia.",
        "Versátil para múltiples tipos de pinturas y lacas."
    ]
print("🛠️ Generando plantilla HTML")
time.sleep(0.6)

# Plantilla HTML
template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Ficha Técnica - {nombre}</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="estilos.css" />
</head>
<body>
  <div class="ficha-tecnica">
    <header class="encabezado">
        <div class="logo">
            <img src="logo-menu-first-pro.png" alt="Logo" />
        </div>          
        <div class="empresa">
            <p>COMERCIO PERU FENIX EIRL<br>RUC 20606042150</p>
        </div>
    </header>

    <section class="imagen-producto">
      <img src="{imagen_src}" alt="{nombre}" />
    </section>

    <section class="titulo">
      <h2>{nombre}</h2>
    </section>

    <section class="contenido">
      <div class="columna izquierda">
        <p>{descripcion}</p>
        <h3>Beneficios:</h3>
        <ul>
{beneficios}
        </ul>
      </div>
      <div class="columna derecha">
        <ul class="detalles">
          <li><strong>Marca:</strong> {marca}</li>
          <li><strong>Tipo:</strong> {tipo}</li>
          <li><strong>Presentación:</strong> {presentacion}</li>
          <li><strong>Color:</strong> {color}</li>
          <li><strong>Composición:</strong> {composicion}</li>
          <li><strong>Dimensiones:</strong> {altura} x {ancho} x {profundidad}</li>
          <li><strong>Observación:</strong> {observacion}</li>
          <li><strong>Advertencia:</strong> {advertencia}</li>
        </ul>
        <h3>Recomendaciones de Uso y Cuidado:</h3>
        <ul class="recomendaciones">
{recomendaciones}
        </ul>
      </div>
    </section>

    <footer class="pie">
      <div class="contacto">
        <span><i class="fas fa-globe"></i> www.insumosfirstpro.com</span> 
        <span><i class="fas fa-envelope"></i> contacto@insumosfirstpro.com</span>
        <span><i class="fas fa-phone"></i> 942 129 598</span>
      </div>
    </footer>
  </div>
</body>
</html>"""

# Generar HTML para listas
recomendaciones_html = ''.join(f'          <li>{r}</li>\n' for r in recomendaciones)
beneficios_html = ''.join(f'          <li>{b}</li>\n' for b in beneficios)

# Rellenar plantilla
try:
    html_content = template.format(
        nombre=data.get('nombreProductoD', 'Sin nombre'),
        descripcion=data.get('DescripcionGeneralD', 'Sin descripción'),
        marca=data.get('marcaProductoD', 'No especificado'),
        tipo=data.get('tipoProductoD', 'No especificado'),
        presentacion=data.get('pesoProductoD', 'No especificado'),
        color=data.get('colorProductoD', 'No especificado'),
        composicion=data.get('materialProductoD', 'No especificado'),
        altura=data.get('alturaProductoD', 'No especificado'),
        ancho=data.get('anchoProductoD', 'No especificado'),
        profundidad=data.get('profundidadProductoD', 'No especificado'),
        observacion=data.get('observacionProductoD', 'No especificado'),
        advertencia=data.get('advertenciaProductoD', 'No especificado'),
        recomendaciones=recomendaciones_html,
        beneficios=beneficios_html,
        imagen_src=imagen_src or "imagen-defecto.png"
    )
except KeyError as e:
    print(f"Error: Llave no encontrada en la plantilla: {str(e)}")
    html_content = None
except Exception as e:
    print(f"Error al formatear la plantilla: {str(e)}")
    html_content = None

# Guardar el HTML
if html_content:
    try:
        output_path = base_dir / "PlantillaFichaTecnica.html"
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"index.html generado exitosamente en {output_path}")
    except Exception as e:
        print(f"Error al guardar el HTML: {str(e)}")
else:
    print("No se generó index.html debido a un error en la plantilla")

print("🎉 Proceso culminado con éxito")
time.sleep(0.6)