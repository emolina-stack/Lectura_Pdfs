from pathlib import Path
from api import PuntowAPI   # ← Asegúrate que tu archivo se llame api.py

import json
import time

# Importamos la clase que ya tienes

def procesar_json_y_enviar_a_api(ruta_json: str):
    """Lee el JSON y envía todas las autorizaciones a la API"""
    
    # 1. Cargar el JSON
    with open(ruta_json, encoding='utf-8') as f:
        datos = json.load(f)

    print(f"📋 Se encontraron {len(datos)} autorizaciones en el JSON\n")

    # 2. Conectar con la API
    api = PuntowAPI()           # usa las credenciales de tu .env
    api.obtener_token()


    for i, item in enumerate(datos, 1):
        clave = item.get("autorizacion_json")
        pdf_nombre = item.get("pdf_nombre", "Desconocido")
        
        # print(f"[{i}/{len(datos)}] Procesando → {clave[:20]}... (de {pdf_nombre})")

        try:
            # 3. Recuperar el comprobante
            resultado = api.recuperar_comprobante(
                clave_acceso=clave,
                async_mode=True          # recomendado (más estable)
            )

            # 4. Descargar el XML
            ruta_xml = api.descargar_xml(clave, carpeta_destino="comprobantes_xml")

            # Guardamos el resultado en el mismo diccionario
            item["estado"] = "descargado"
            item["ruta_xml"] = ruta_xml
            item["mensaje"] = "Éxito"

            print(f"   ✅ Descargado correctamente\n")

        except Exception as e:
            item["estado"] = "error"
            item["error"] = str(e)
            print(f"   ❌ Error: {e}\n")

    # 5. Guardar JSON actualizado con el estado
    

    
    print("="*70)
    print("✅ PROCESO FINALIZADO")
    print("="*70)


def main(json_path):
    # Cambia esta ruta por la de tu archivo JSON
    # json_path = "json_files/claves_Ceci by iScanner.json"     # ← pon aquí tu archivo
    
    procesar_json_y_enviar_a_api(json_path) 
# # ====================== USO ======================
# if __name__ == "__main__":
#     # Cambia esta ruta por la de tu archivo JSON
#     json_path = "json_files/claves_Ceci by iScanner.json"     # ← pon aquí tu archivo
    
#     procesar_json_y_enviar_a_api(json_path)