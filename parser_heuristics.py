import re

# Expresiones regulares
PRICE_RE = r'(?P<currency>\$|USD|COP|EUR)?\s*(?P<price>\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))'
QTY_RE = r'(?:Qty|Quantity|Cantidad)[:\s]*(?P<qty>\d+)'
TOTAL_RE = r'\bTotal\s*[:\-]?\s*' + PRICE_RE

import os

def _parse_price(s):
    if not s:
        return None
    s = s.replace('USD', '').replace('COP', '').replace('EUR', '')
    s = s.replace(' ', '').replace(',', '').replace('$', '')
    try:
        return float(s)
    except:
        return None

def extract_items_and_totals(body_text, attachments):
    text_sources = [body_text or ''] + [a.get('texto', '') or '' for a in (attachments or [])]
    text = "\n".join(text_sources)
    text = re.sub(r'\s+', ' ', text)

    productos = []
    totales = {"total": None, "moneda": "USD"}


    pattern = re.compile(
        r'(?P<item>[A-Z0-9\-]+),\s*(?P<name>Vinyl Floor Tiles|[A-Z][A-Za-z0-9 \-,]+?):\s*(?P<desc>[^$]{20,200}?)\s+'
        r'(?P<qty>\d{1,4})\s+(?:EA|UN|PCS)?\s*\$?(?P<unit>\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*\$?(?P<total>\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        re.IGNORECASE
    )

    for match in pattern.finditer(text):
        nombre = match.group('name').strip()
        descripcion = match.group('desc').strip()
        cantidad = int(match.group('qty'))
        precio_unitario = _parse_price(match.group('unit'))
        total = _parse_price(match.group('total'))

        productos.append({
            "nombre": nombre,
            "descripcion": descripcion,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "total": total
        })


    if productos:
        totales["total"] = round(sum(p["total"] or 0 for p in productos), 2)
    else:
        precios = [float(p.replace(',', '').replace('$', '')) for p in re.findall(r'\$?(\d+[.,]\d{2})', text)]
        if precios:
            total = max(precios)
            productos.append({
                "nombre": "Producto detectado",
                "descripcion": "",
                "cantidad": 1,
                "precio_unitario": total,
                "total": total
            })
            totales["total"] = total


    adjuntos_limpios = []
    for a in attachments or []:
        adjuntos_limpios.append({
            "nombre": os.path.basename(a.get("nombre", "")),
            "tipo": a.get("tipo", ""),
            "ruta": a.get("ruta", "").replace("\\", "/")
        })

        adjuntos_limpios = [{"nombre": a["nombre"], "tipo": a["tipo"], "ruta": a["ruta"]} for a in attachments]
    return productos, totales, adjuntos_limpios

