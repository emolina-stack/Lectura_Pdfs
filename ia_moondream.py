import base64
import json
import re
import ollama

def extraer_datos_factura_llamaindex(imagen_bytes):
    try:
        base64_image = base64.b64encode(imagen_bytes).decode('utf-8')
        
        response = ollama.chat(
            model='glm-ocr',
            messages=[{
                'role': 'user',
                'content': '''Eres un experto en facturas electrónicas del SRI de Ecuador.
                Analiza la imagen y extrae SOLO los siguientes campos. 
                Responde únicamente con un JSON válido y nada más:

                {
                "numero_autorizacion": "",
                "fecha_hora_autorizacion": "",
                "ruc_receptor": "",
                "razon_social": "",
                "total": ""
                }

                Si no encuentras un campo, pon "No encontrado".''',
                                'images': [base64_image],
                            }],
                            options={
                                'temperature': 0.0,
                                'num_ctx': 16384,          # ← ESTO SOLUCIONA EL ERROR
                                'num_predict': 1024
                            }
        )

        # CORRECCIÓN: Acceder directamente al contenido de la respuesta
        texto_respuesta = response['message']['content']

        print("🔍 Respuesta cruda del modelo:\n", texto_respuesta)

        # Extraer JSON
        match = re.search(r'\{.*\}', texto_respuesta, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

        return {
            'numero_autorizacion': 'No encontrado',
            'fecha_hora_autorizacion': 'No encontrado',
            'ruc_receptor': 'No encontrado',
            'razon_social': 'No encontrado',
            'total': 'No encontrado'
        }

    except Exception as e:
        print('Error:', str(e))
        return {
            'numero_autorizacion': 'Error',
            'fecha_hora_autorizacion': str(e),
            'ruc_receptor': '',
            'razon_social': '',
            'total': ''
        }
