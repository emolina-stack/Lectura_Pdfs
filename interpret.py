import http.client
import json
import base64
import re

#F:\Bots\Bot_Documentos\bot_establecimiento\captcha_img 

def response_captcha(captcha_bytes):
    try:
        encoded_string = base64.b64encode(captcha_bytes).decode('utf-8')

        base64_imagen = "data:image/png;base64," + encoded_string

        conn = http.client.HTTPSConnection("flowise-y3q2.onrender.com")
        payload = json.dumps({
                "question": """Eres un experto en facturas electrónicas de Ecuador. 
            Analiza la imagen y extrae los siguientes campos. 
            Responde **solo** en formato JSON válido:

            {
            "numero_autorizacion": "el número de 49 dígitos, NÚMERO DE AUTORIZACIÓN o CLAVE DE ACCESO",
            "fecha_hora_autorizacion": "Fecha y hora en formato dd/mm/yyyy hh:mm:ss",
            "ruc_receptor": "Identificación o CI",
            "razon_social": "Razón social del cliente/Nombres y Apellidos",
            "total": "VALOR TOTAL"
            }

            Si algún campo no se ve claramente, pon "No encontrado".No agregues texto extra.""",
                "uploads": [
                    {
                        "data": base64_imagen,
                        "type": "file",
                        "name": "factura.png",
                        "mime": "image/png"
                    }
                ]
            })
        headers = {
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/v1/prediction/1dfecf39-0693-4e4c-a540-0700bc5f5b3a", payload, headers)
        res = conn.getresponse()
        data = res.read()
        respuesta = data.decode("utf-8")

        try:
            json_resp = json.loads(respuesta)
            texto_final = json_resp.get("text", "").strip()
        except:
            texto_final = respuesta.strip()

        match = re.search(r'\{.*\}', texto_final, re.DOTALL)
        if match:
            try:
                resultado = json.loads(match.group(0))
                return resultado
            except:
                return {"numero_autorizacion": "", "fecha_hora": texto_final}
        else:
            return {"numero_autorizacion": "", "fecha_hora": texto_final}
    except Exception as e:
        print("Error al procesar el captcha:", str(e))
        return ""
        
