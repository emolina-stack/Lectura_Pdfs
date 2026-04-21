import os
import sys
from proccess_easy_ocr import ProcesadorEasyOCR     # ← la más probable
from read_xml_json.compare_xml_json import enriquecer_json_con_xml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main
import time


# ================== CONFIGURACIÓN ==================
# pdf_path = "files/Ceci by iScanner.pdf"   # ← Cambia si es necesario
# pdf_path = "files/NAEL LAMAN LUZURIAGA 230.89.pdf"
# pdf_path = "files/JACQUELINE JOHNSON 2_compressed.pdf"
# pdf_path = "files/KAREN CASTRO 466.99.pdf"
# pdf_path = "files/Edison Molina_demo.pdf"
pdf_path = "files/25281-ALCANCE LIQ1412923-CALLE GARCIA JORGE.pdf"

if __name__ == "__main__":
    inicio = time.time()

    ruta_json = "json_files/claves_25281-ALCANCE LIQ1412923-CALLE GARCIA JORGE.json"     # ← tu JSON del OCR
    ruta_xml = "comprobantes_xml/2503202601091442909700120011000000000365930867118.xml"  # ← el XML que descargaste
    procesador = ProcesadorEasyOCR()
    
    # Prueba con uno de tus PDFs
    lista_claves = procesador.procesar_pdf(pdf_path)
    fin = time.time()
    
    print(f"\nSe encontraron {len(lista_claves)} claves de acceso")
    print(lista_claves)
    main(ruta_json)
    print('*'*10)
    enriquecer_json_con_xml(ruta_json, ruta_xml)
    minutos = int((fin - inicio) // 60)
    segundos = int((fin - inicio) % 60)
    print(f"\n⏱️ Tiempo total: {minutos} minutos y {segundos} segundos")