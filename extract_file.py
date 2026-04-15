from pypdf import PdfReader
from pdf2image import convert_from_path
from ia_moondream import extraer_datos_factura_llamaindex
import re

pdf_path = "files/Ceci by iScanner.pdf"
# pdf_path = "files/NAEL LAMAN LUZURIAGA 230.89.pdf"
# pdf_path = "files/JACQUELINE JOHNSON 2_compressed.pdf"
# pdf_path = "files/KAREN CASTRO 466.99.pdf"
# pdf_path = "files/Edison Molina_demo.pdf"


# Parsear el PDF
# documentos = parser.load_data("files/KAREN CASTRO 466.99.pdf")

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
    resultado = extraer_datos_factura_llamaindex(img_bytes)

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