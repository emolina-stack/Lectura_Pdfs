from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse

llama_parse_api_key = "llx-xCB7aGdifgYEzVlfPe3UMt1mpEbY4dTbJeh85kEarnAX1GJX"
print("🔑 Usando API Key:", llama_parse_api_key[:10] + "..." if llama_parse_api_key else "❌ SIN CLAVE")

parser = LlamaParse(
    api_key=llama_parse_api_key,
    result_type="text",      # Mejor para formularios y facturas
    premium_mode=True,   # Usa el modelo más potente (recomendado para escaneados)
    verbose=True        
    # language="es",             # fuerza español (opcional)
    # num_workers=2,             # más velocidad si tienes muchos PDFs
)

file_extractor = {"application/pdf": parser}

# Ruta de tu PDF
pdf_path = "files/Ceci by iScanner.pdf"

documents = SimpleDirectoryReader(
    input_files=[pdf_path],
    file_extractor=file_extractor
).load_data()
print("datooos", len(documents))

# Mostrar el texto extraído
print("✅ PDF escaneado leído correctamente con OCR + IA\n")
for i, doc in enumerate(documents):
    print(f"── Página {i+1} ──")
    texto=doc.text.strip()
    print(f"algoo: {texto}")
    if texto:
        print(texto[:800] + "..." if len(texto) > 800 else texto)  # primeros 800 caracteres
    else:
        print("❌ TEXTO VACÍO en esta página")
    print("\n" + "="*90 + "\n")

