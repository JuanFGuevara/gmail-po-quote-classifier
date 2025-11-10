#!/usr/bin/env python3
import json
import click
from gmail_client import GmailClient
from parser import parse_email_and_attachments
from classifier import classify_document

@click.command()
@click.option('--query', default='newer_than:7d', help='Gmail query, eg: "newer_than:7d"')
@click.option('--max', 'max_results', default=10, help='Max messages to process')
@click.option('--output', default='output.json', help='Output JSON file')
def main(query, max_results, output):
    client = GmailClient() 
    msgs = client.list_messages(query=query, max_results=max_results)
    results = []

    for m in msgs:
        print(f"Procesando mensaje id={m['id']}")
        message = client.get_message(m['id'])
        data = parse_email_and_attachments(message, gmail_client=client)
        tipo = classify_document(data)

 
        if tipo in ("PO", "QUOTE"):
            result = {
                "tipo_documento": tipo,
                "correo": data.get("from"),
                "asunto": data.get("subject"),
                "fecha": data.get("date"),
                "productos": data.get("productos", []),
                "totales": data.get("totales", {}),
                "adjuntos": data.get("adjuntos", [])
            }
            results.append(result)
        else:
            print(f"→ Ignorado ({tipo}): {data.get('subject')}")


    unique = []
    seen = set()
    for r in results:
        key = (r["asunto"], r["fecha"], r["correo"])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    results = unique


    with open(output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nProcesados {len(results)} mensajes únicos — salida en {output}")

if __name__ == '__main__':
    main()
