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
        "question": "contestame sin ningun comentario el dato de la imagen",
        "uploads": [
            {
                "data": base64_imagen,
                "type": "file",
                "name": "Flowise.png",
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

        texto_completo = texto_final
        match = re.search(r'"([^"]*)"', texto_completo)

        if match:
            captcha = match.group(1)
            print(captcha)          
        else:
            # print("No se encontraron comillas")
            captcha=texto_completo
        return captcha
    except Exception as e:
        print("Error al procesar el captcha:", str(e))
        return ""
        
