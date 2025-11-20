import json
from bs4 import BeautifulSoup
import os

def extract_ficha_cnt_href(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extraer URL del PDF
    pdf_element = soup.find(class_="ficha-cnt-pdf")
    pdf_href = pdf_element.get('href') if pdf_element and pdf_element.get('href') else ""

    # Extraer URL de la imagen
    image_element = soup.find(class_="image-zoom")
    image_href = image_element.get('href') if image_element and image_element.get('href') else ""

    return pdf_href, image_href

def save_to_json(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    html_file_path = 'C:/Proyectos/Demo-Huawei-DeepSeek/html/htmlPagina.html'

    # Rutas JSON de salida
    output_json_pdf = 'C:/Proyectos/Demo-Huawei-DeepSeek/Json/ficha_cnt_output.json'
    output_json_img = 'C:/Proyectos/Demo-Huawei-DeepSeek/Json/nombreImagenLB.json'

    # Extraer URLs
    url_pdf, url_imagen = extract_ficha_cnt_href(html_file_path)

    # Guardar cada URL en su respectivo JSON
    save_to_json({"urlPDF": url_pdf}, output_json_pdf)
    save_to_json({"url": url_imagen}, output_json_img)

    print(f"✅ URL PDF guardada en: {output_json_pdf}")
    print(f"✅ URL de imagen guardada en: {output_json_img}")
