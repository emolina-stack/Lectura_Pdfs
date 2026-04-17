from proccess_easy_ocr import ProcesadorEasyOCR     # ← la más probable

from main import main
import time

# ================== CONFIGURACIÓN ==================
pdf_path = "files/Ceci by iScanner.pdf"   # ← Cambia si es necesario
# pdf_path = "files/NAEL LAMAN LUZURIAGA 230.89.pdf"
# pdf_path = "files/JACQUELINE JOHNSON 2_compressed.pdf"
# pdf_path = "files/KAREN CASTRO 466.99.pdf"
# pdf_path = "files/Edison Molina_demo.pdf"

if __name__ == "__main__":
    inicio = time.time()
    procesador = ProcesadorEasyOCR()
    
    # Prueba con uno de tus PDFs
    lista_claves = procesador.procesar_pdf(pdf_path)
    fin = time.time()
    minutos = int((fin - inicio) // 60)
    segundos = int((fin - inicio) % 60)
    print(f"\nSe encontraron {len(lista_claves)} claves de acceso")
    print(lista_claves)
    main()
    print(f"\n⏱️ Tiempo total: {minutos} minutos y {segundos} segundos")