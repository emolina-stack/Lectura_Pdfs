import xmltodict
import json
from pathlib import Path
import xmltodict
import json
from pathlib import Path

def leer_xml_con_xmltodict(ruta_xml: str):
    """Versión corregida - maneja correctamente el CDATA"""
    with open(ruta_xml, encoding='utf-8') as f:
        xml_str = f.read()

    # Parsear el XML exterior
    data = xmltodict.parse(xml_str)

    # Extraer datos del envoltorio <autorizacion>
    autorizacion = data.get('autorizacion', {})

    # Extraer y parsear el CDATA (la factura real)
    comprobante_str = autorizacion.get('comprobante', '')
    if isinstance(comprobante_str, str):
        factura_dict = xmltodict.parse(comprobante_str)
    else:
        factura_dict = comprobante_str  # por si ya viene como dict

    factura = factura_dict.get('factura', {})

    info_tributaria = factura.get('infoTributaria', {})
    info_factura = factura.get('infoFactura', {})

    # Datos principales
    info = {
        "numero_autorizacion": autorizacion.get('numeroAutorizacion'),
        # "fecha_autorizacion": autorizacion.get('fechaAutorizacion'),
        
        # # "clave_acceso": info_tributaria.get('claveAcceso'),
        "ruc_emisor": info_tributaria.get('ruc'),
        # "razon_social_emisor": info_tributaria.get('razonSocial'),
        
        # "razon_social_receptor": info_factura.get('razonSocialComprador'),
        # "identificacion_receptor": info_factura.get('identificacionComprador'),
        # "importe_total": float(info_factura.get('importeTotal', 0)),
        
    }

    # Extraer detalles de productos
    detalles = info_factura.get('detalles', {}).get('detalle', [])
    if not isinstance(detalles, list):
        detalles = [detalles]

    for det in detalles:
        info["detalles"].append({
            "codigo": det.get('codigoPrincipal'),
            "descripcion": det.get('descripcion'),
            "cantidad": float(det.get('cantidad', 0)),
            "precio_unitario": float(det.get('precioUnitario', 0)),
            "precio_total": float(det.get('precioTotalSinImpuesto', 0)),
        })

    return info


