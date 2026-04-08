from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
import re
from PIL import Image, ImageEnhance


# pdf_path = "files/Ceci by iScanner.pdf"
# pdf_path = "files/NAEL LAMAN LUZURIAGA 230.89.pdf"
# pdf_path = "files/JACQUELINE JOHNSON 2_compressed.pdf"
pdf_path = "files/KAREN CASTRO 466.99.pdf"
# pdf_path = "files/Edison Molina_demo.pdf"

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Regex muy robusto para Número de Autorización
patron = re.compile(r'(\d{49})', re.IGNORECASE)   # Busca directamente 49 dígitos seguidos


reader = PdfReader(pdf_path)

for i, page in enumerate(reader.pages, start=1):
    print(f"{'='*35} PAGINA {i} {'='*35}")
    
    texto = (page.extract_text() or "").strip()
    numero = None

    # Primer intento: texto nativo
    if texto:
        match = patron.search(texto)
        if match:
            numero = match.group(1)

    # Segundo intento: OCR con preprocesamiento
    if not numero:
        print("   Aplicando OCR mejorado...")
        try:
            images = convert_from_path(pdf_path, first_page=i, last_page=i, dpi=450)
            if images:
                img = images[0]
                
                # Preprocesamiento para mejorar OCR
                img = img.convert('L')                    # Escala de grises
                img = ImageEnhance.Contrast(img).enhance(2.0)   # Aumentar contraste
                img = ImageEnhance.Sharpness(img).enhance(1.5)  # Aumentar nitidez
                
                texto_ocr = pytesseract.image_to_string(img, config='--oem 3 --psm 6 -l spa')
                
                match = patron.search(texto_ocr)
                if match:
                    numero = match.group(1)
        except Exception as e:
            print(f"   Error OCR: {e}")

    if numero:
        print(f"✅ Número de Autorización encontrado: {numero}")
    else:
        print("❌ No se encontró Número de Autorización")

    print("\n")