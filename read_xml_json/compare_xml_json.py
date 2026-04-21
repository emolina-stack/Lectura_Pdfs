import json
import os
import sys
from pathlib import Path
from .read_xml import leer_xml_con_xmltodict   # ← importa la función que ya tienes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

carpeta_salida = Path("files_comparativo")  # o la ruta que quieras
carpeta_salida.mkdir(parents=True, exist_ok=True)

def enriquecer_json_con_xml(ruta_json_ocr: str, ruta_xml: str = None):
    """
    Compara y enriquece el JSON del OCR con los datos reales del XML.
    """
    # 1. Cargar JSON del OCR
    with open(ruta_json_ocr, encoding='utf-8') as f:
        datos_ocr = json.load(f)

    # 2. Cargar XML
    if ruta_xml is None:
        # Si no pasas ruta_xml, intenta buscarlo por nombre de clave
        clave = datos_ocr[0]["autorizacion"] if datos_ocr else ""
        ruta_xml = f"../comprobantes_xml/{clave}.xml"

    xml_data = leer_xml_con_xmltodict(ruta_xml)

    # 3. Comparar y enriquecer
    for item in datos_ocr:
        clave_ocr = item.get("autorizacion")
        
        if clave_ocr == xml_data.get("clave_acceso") or clave_ocr == xml_data.get("numero_autorizacion"):
            # === COINCIDE ===
            item["autorizacion_xml"] = xml_data.get("numero_autorizacion")
            item["estado"] = "coincide"
            # item["total_xml"] = xml_data["importe_total"]
            # item["total_ocr"] = item.get("total")
            
            # Enriquecer con datos del XML
            item.update({
                "ruc_emisor": xml_data["ruc_emisor"],
                "razon_social_emisor": xml_data["razon_social_emisor"],
                "identificacion_receptor": xml_data["identificacion_receptor"],
                # "razon_social_receptor": xml_data["razon_social_receptor"],
                # "fecha_emision": xml_data["fecha_emision"],
                # "fecha_autorizacion": xml_data["fecha_autorizacion"],
                # "detalles_xml": xml_data["detalles"],
            })
                            
        else:
            item["estado"] = "no_coincide"

    # 4. Guardar JSON enriquecido
    nombre_archivo = Path(ruta_json_ocr).stem + "_comparativo.json"
    ruta_salida = carpeta_salida / nombre_archivo
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(datos_ocr, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON enriquecido guardado en: {ruta_salida}")
    
    return datos_ocr

