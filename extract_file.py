from pypdf import PdfReader
from paddleocr import PaddleOCR
from pdf2image import convert_from_path, pdfinfo_from_path
from extract_file import extraer_campos
from pathlib import Path

import numpy as np
import pandas as pd
import os
import re
import paddle
import time
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"
os.environ["PADDLEOCR_WARNINGS"] = "0"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


pdf_path = "files/Ceci by iScanner.pdf"
# pdf_path = "files/NAEL LAMAN LUZURIAGA 230.89.pdf"
# pdf_path = "files/JACQUELINE JOHNSON 2_compressed.pdf"
# pdf_path = "files/KAREN CASTRO 466.99.pdf"
# pdf_path = "files/Edison Molina_demo.pdf"

resultados = []
start_time = time.time()
    # 1. Solo leer número de páginas (rápido)
reader = PdfReader(pdf_path)
num_pages = len(reader.pages)
print('TOTAL PDFs', num_pages)

# OCR
ocr = PaddleOCR(
    lang='es'
)


# 2. Convertir a imágenes (Cada pagina)
info = pdfinfo_from_path(pdf_path)
num_pages = info["Pages"]
print("Convirtiendo PDF a imágenes...")
images = convert_from_path(
    pdf_path,
    dpi=300,                    # 250-300 es buen balance
    thread_count=4              # Acelera la conversión
)
for page_num, img in enumerate(images, start=1):
    print(f"Procesando página {page_num}/{num_pages}...")
    
    # OCR con PaddleOCR
    result = ocr.ocr(img)   # cls=True usa angle classification
    
    # result es una lista de listas: [[ [bbox, (text, confidence)], ... ]]
    page_text = ""
    detalles = []   # Para guardar bounding boxes y confianza si los necesitas
    
    for line in result[0] if result and len(result) > 0 else []:
        bbox = line[0]           # Coordenadas del cuadro
        text, confidence = line[1]
        page_text += text + "\n"
        detalles.append({
            "texto": text,
            "confianza": float(confidence),
            "bbox": bbox
        })
    
    # 5. Aquí va tu extracción de campos (la parte más importante)
    datos_extraidos = extraer_campos(page_text, detalles)   # ← Tu función
    
    resultados.append({
        "pdf_nombre": Path(pdf_path).name,
        "pagina": page_num,
        "texto_completo": page_text.strip(),
        "confianza_promedio": sum(d["confianza"] for d in detalles)/len(detalles) if detalles else 0,
        **datos_extraidos   # Desempaqueta los campos que extraigas (nombre, cedula, valor, fecha, etc.)
    })


total_time = time.time() - start_time
print(f"✅ PDF procesado en {total_time:.2f} segundos")

# 6. Guardar en DataFrame
df = pd.DataFrame(resultados)

# Guardar en formatos eficientes
# df.to_parquet(f"resultados_{Path(pdf_path).stem}.parquet", index=False)
df.to_csv(f"resultados_{Path(pdf_path).stem}.csv", index=False, encoding='utf-8-sig')
# df.to_csv(...) si prefieres
print(df.head())