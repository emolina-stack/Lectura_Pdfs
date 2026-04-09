from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
import re
from interpret import response_captcha
from PIL import Image, ImageEnhance

# ================== CONFIGURACIÓN ==================
# pdf_path = "files/Ceci by iScanner.pdf"   # ← Cambia si es necesario
# pdf_path = "files/NAEL LAMAN LUZURIAGA 230.89.pdf"
# pdf_path = "files/JACQUELINE JOHNSON 2_compressed.pdf"
pdf_path = "files/KAREN CASTRO 466.99.pdf"
# pdf_path = "files/Edison Molina_demo.pdf"

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# custom_config = r'--oem 3 --psm 6 -l spa'

# ================== PATRONES REGEX ==================
# patron_numero = re.compile(
#     r'(\d{49})',
#     re.IGNORECASE
# )

# patron_fecha_hora = re.compile(
#     r'(?:Fecha y Hora de Autorización|FECHA Y HORA DE AUTORIZACIÓN|Fecha y hora de Autorización|FECHA Y HORA AUTORIZACIÓN)[:\s]*(\d{1,2}[/\.-]\d{1,2}[/\.-]\d{2,4}\s+\d{1,2}:\d{2}(?::\d{2})?)',
#     re.IGNORECASE
# )

reader = PdfReader(pdf_path)

print(f"📄 Procesando PDF con {len(reader.pages)} páginas...\n")

for i, page in enumerate(reader.pages, start=1):
    print(f"{'='*40} PAGINA {i} {'='*40}")
    
    images = convert_from_path(pdf_path, first_page=i, last_page=i, dpi=400)
    img = images[0]

    import io
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    #   CONECTANDO CON API FLOWISE
    resultado = response_captcha(img_bytes)

    numero = resultado.get("numero_autorizacion", "")
    fecha_hora = resultado.get("fecha_hora_autorizacion", "")
    valor_total = resultado.get("total", "")
    identificacion = resultado.get("ruc_receptor", "")
    razon_social = resultado.get("razon_social","")

    print(f"✅ Número de Autorización   : {numero if numero else 'No encontrado'}")
    print(f"✅ Fecha y Hora de Autorización : {fecha_hora if fecha_hora else 'No encontrado'}")
    print(f"✅ Razon Social: {razon_social if razon_social else 'No encontrado'}")
    print(f"✅ Identificacion: {identificacion if identificacion else 'No encontrado'}")
    print(f"✅ Valor Total : {valor_total if valor_total else 'No encontrado'}")
