from llama_index.multi_modal_llms.ollama import OllamaMultiModal
from llama_index.core.schema import ImageDocument
import io
import json
import base64

# ================== CONFIGURACIÓN ==================
multi_modal_llm = OllamaMultiModal(
    model="moondream",      # o "moondream"
    request_timeout=120.0
)

def extraer_datos_factura_llamaindex(imagen_bytes):
    try:
        # ← CORRECCIÓN PRINCIPAL: Pasar los bytes directamente
        # image_doc = ImageDocument(image_bytes=imagen_bytes)
        image_doc = base64.b64encode(imagen_bytes).decode('utf-8')
        base64_imagen = "data:image/png;base64," + image_doc


        prompt = """Dame el texto visible"""

        response = multi_modal_llm.complete(
            prompt=prompt,
            image_documents=[base64_imagen]
        )

        texto_respuesta = response.text.strip()
        print('TEXTOOO', texto_respuesta)

        match = re.search(r'\{.*\}', texto_respuesta, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass

        return {
            "numero_autorizacion": "No encontrado"
            
        }

    except Exception as e:
        print("Error con LlamaIndex:", str(e))
        return {
            "numero_autorizacion": "Error"
        }