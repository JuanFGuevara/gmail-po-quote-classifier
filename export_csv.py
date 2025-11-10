
import json
import pandas as pd
import sys

def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rows = []
    for d in data:
        productos = d.get("productos", [])
        if not productos:
            rows.append({
                "tipo_documento": d.get("tipo_documento"),
                "correo": d.get("correo"),
                "asunto": d.get("asunto"),
                "fecha": d.get("fecha"),
                "producto_nombre": "",
                "producto_descripcion": "",
                "cantidad": "",
                "precio_unitario": "",
                "total_producto": "",
                "total_general": d.get("totales", {}).get("total"),
                "moneda": d.get("totales", {}).get("moneda"),
            })
        else:
            for p in productos:
                rows.append({
                    "tipo_documento": d.get("tipo_documento"),
                    "correo": d.get("correo"),
                    "asunto": d.get("asunto"),
                    "fecha": d.get("fecha"),
                    "producto_nombre": p.get("nombre"),
                    "producto_descripcion": p.get("descripcion", ""),
                    "cantidad": p.get("cantidad"),
                    "precio_unitario": p.get("precio_unitario"),
                    "total_producto": p.get("total"),
                    "total_general": d.get("totales", {}).get("total"),
                    "moneda": d.get("totales", {}).get("moneda"),
                })

    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Exportado a {output_file} ({len(df)} filas)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python export_csv.py <entrada.json> <salida.csv>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
