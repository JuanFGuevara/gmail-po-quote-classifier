import os
import base64
from pdf_utils import extract_text_from_pdf

def parse_email_and_attachments(message, gmail_client):
    headers = {h['name']: h['value'] for h in message.get('payload', {}).get('headers', [])}
    subject = headers.get('Subject', '')
    from_addr = headers.get('From', '')
    date = headers.get('Date', '')
    body = ''


    def extract_text_from_part(part):
        data = part.get('body', {}).get('data')
        if data:
            txt = base64.urlsafe_b64decode(data.encode('UTF-8')).decode('utf-8', errors='ignore')
            return txt
        return ''

    payload = message.get('payload', {})
    def walk_parts(p):
        texts = []
        if p.get('mimeType', '').startswith('text/'):
            texts.append(extract_text_from_part(p))
        for sub in p.get('parts', []) or []:
            texts += walk_parts(sub)
        return texts

    texts = walk_parts(payload)
    body = "\n".join(texts).strip()


    import re
    from html import unescape

    body_clean = re.sub(r'<[^>]+>', ' ', body)          
    body_clean = unescape(body_clean)                    
    body_clean = re.sub(r'\s+', ' ', body_clean).strip() 
    body = body_clean


    lines = list(dict.fromkeys(body.splitlines()))
    body = "\n".join(lines)


    adjuntos = []
    for part in payload.get('parts', []) or []:
        if part.get('filename'):
            fname = part['filename']
            mime = part.get('mimeType')
            body_info = part.get('body', {})
            if 'attachmentId' in body_info:
                att_id = body_info['attachmentId']


                clean_name = fname.replace(" ", "_")
                save_name = os.path.join('adjuntos', clean_name)
                save_name = save_name.replace("\\", "/")
                os.makedirs('adjuntos', exist_ok=True)

                gmail_client.download_attachment(message['id'], att_id, save_name)

                text = None
                if mime == 'application/pdf' or fname.lower().endswith('.pdf'):
                    text = extract_text_from_pdf(save_name)

                adjuntos.append({
                    "nombre": clean_name,
                    "tipo": mime,
                    "ruta": save_name,
                    "texto": text
                })


    from parser_heuristics import extract_items_and_totals
    productos, totales, adjuntos_limpios = extract_items_and_totals(body, adjuntos)



    adjuntos_limpios = [{"nombre": a["nombre"], "tipo": a["tipo"], "ruta": a["ruta"]} for a in adjuntos]

    parsed = {
        "from": from_addr,
        "subject": subject,
        "date": date,
        "body_text": body,
        "productos": productos,
        "totales": totales,
        "adjuntos": adjuntos_limpios  
    }
    return parsed
