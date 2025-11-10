import re

def classify_document(data):
    subject = (data.get("subject") or "").upper()
    body = (data.get("body_text") or "").upper()
    attachments = data.get("adjuntos", [])
    from_addr = (data.get("from") or "").lower().strip()

    match = re.search(r"<([^>]+)>", from_addr)
    if match:
        from_addr = match.group(1)

    # --- Ignorar remitentes de marketing / plataformas ---
    ignore_domains = [
        "coursera.org",
        "m.learn.coursera.org",
        "shein.com",
        "marketing",
        "newsletter",
        "noreply",
        "monday.com",
        "amazon",
        "facebook",
        "instagram",
        "linkedin",
        "twitter",
        "meta.com"
    ]
    if any(bad in from_addr for bad in ignore_domains):
        return "OTRO"

    # Ignorar asuntos de promociones
    if any(word in subject for word in [
        "SALE", "DISCOUNT", "DESCUENTO", "PROMO", "OFFER", "NEWSLETTER",
        "WELCOME", "NO CONTESTAR", "ADQUIERE", "REGÍSTRATE", "SUBSCRIBE", "INSCRÍBETE"
    ]):
        return "OTRO"

    #Reglas por ASUNTO 
    if re.search(r"\bPO[-_ ]?\d+\b", subject):
        return "PO"
    if any(kw in subject for kw in ["PURCHASE ORDER", "ORDEN DE COMPRA", "ORDEN #"]):
        return "PO"
    if any(kw in subject for kw in ["QUOTE", "QUOTATION", "COTIZACIÓN", "QUOTE REQUEST"]):
        return "QUOTE"

    #Reglas por CUERPO 
    # Evitar falsos positivos de marketing
    if any(phrase in body for phrase in [
        "SEND ME A QUOTE", "PLEASE QUOTE", "NEED A QUOTE", "COTIZACIÓN", "QUOTE REQUEST"
    ]) and not re.search(r"\bPO[-_ ]?\d+\b", body):
        return "QUOTE"

    if re.search(r"\bPO[-_ ]?\d+\b", body) or "PURCHASE ORDER" in body:
        return "PO"

    # Reglas por ADJUNTOS
    for att in attachments:
        text = att.get("texto", "")
        if text:
            text_upper = text.upper()
            if any(x in text_upper for x in ["PURCHASE ORDER", "PO NUMBER"]):
                return "PO"

    #  Regla de desempate
    # Si aparecen ambas menciones, gana PO si hay número de orden explícito
    if ("PURCHASE ORDER" in body and "QUOTE" in body) or ("ORDEN" in body and "COTIZACIÓN" in body):
        if re.search(r"\bPO[-_ ]?\d+\b", body):
            return "PO"
        else:
            return "QUOTE"

    #  Valor por defecto 

    return "OTRO"
