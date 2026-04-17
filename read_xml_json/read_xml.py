import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any

def leer_xml_factura(ruta_xml: str) -> Dict[str, Any]:
    """
    Lee un XML de factura electrónica del SRI y extrae los campos principales.
    """
    tree = ET.parse(ruta_xml)
    root = tree.getroot()

    # Namespace del SRI (muy importante)
    ns = {'sri': 'http://www.sri.gob.ec/factura'}

    def find(tag: str, default=None):
        """Busca un elemento dentro del namespace"""
        elem = root.find(f".//sri:{tag}", ns)
        return elem.text.strip() if elem is not None and elem.text else default

    datos = {
        "clave_acceso": Path(ruta_xml).stem,
        "tipo_comprobante": root.get("id", "FACTURA"),
        "version": root.get("version"),

        # Información del emisor
        "ruc_emisor": find("ruc"),
        "razon_social_emisor": find("razonSocial"),

        # Información del receptor
        "identificacion_receptor": find("identificacionComprador"),
        "razon_social_receptor": find("fechaAutorizacion"),

        # Datos de la factura
        "fecha_emision": find("fechaEmision"),
        "secuencial": find("secuencial"),
        "total_sin_impuestos": float(find("totalSinImpuestos") or 0),
        "total_descuento": float(find("totalDescuento") or 0),
        "importe_total": float(find("importeTotal") or 0),

        # Detalles de los productos
        "detalles": []
    }

    # Extraer todos los ítems
    for detalle in root.findall(".//sri:detalle", ns):
        datos["detalles"].append({
            "codigo": find("codigoPrincipal", parent=detalle),
            "descripcion": find("descripcion", parent=detalle),
            "cantidad": float(find("cantidad", parent=detalle) or 0),
            "precio_unitario": float(find("precioUnitario", parent=detalle) or 0),
            "precio_total": float(find("precioTotalSinImpuesto", parent=detalle) or 0),
        })

    return datos

if __name__ == "__main__":
    ruta = "../comprobantes_xml/1101202601099299798200120051020000487381234567812.xml"
    
    factura = leer_xml_factura(ruta)
    
    print("✅ XML leído correctamente")
    print(f"autorizacion: {factura['clave_acceso']}")
    print(f"Emisor: {factura['razon_social_emisor']} ({factura['ruc_emisor']})")
    print(f"Receptor: {factura['razon_social_receptor']}")
    print(f"Fecha: {factura['fecha_emision']}")
    print(f"Total: ${factura['importe_total']:.2f}")
    print(f"Items: {len(factura['detalles'])} productos")
    
    # Guardar en JSON (muy útil)
    import json
    with open("factura_procesada.json", "w", encoding="utf-8") as f:
        json.dump(factura, f, indent=2, ensure_ascii=False)