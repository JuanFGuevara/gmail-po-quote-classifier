#!/usr/bin/env python3
import json
import sqlite3
import sys

def main(input_file, db_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Crear tablas si no existen
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_documento TEXT,
        correo TEXT,
        asunto TEXT,
        fecha TEXT,
        total_general REAL,
        moneda TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id INTEGER,
        nombre TEXT,
        descripcion TEXT,
        cantidad REAL,
        precio_unitario REAL,
        total REAL,
        FOREIGN KEY(doc_id) REFERENCES documentos(id)
    )
    """)

    for d in data:
        totales = d.get("totales", {})
        cur.execute("""
            INSERT INTO documentos (tipo_documento, correo, asunto, fecha, total_general, moneda)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            d.get("tipo_documento"),
            d.get("correo"),
            d.get("asunto"),
            d.get("fecha"),
            totales.get("total"),
            totales.get("moneda")
        ))
        doc_id = cur.lastrowid

        for p in d.get("productos", []):
            cur.execute("""
                INSERT INTO productos (doc_id, nombre, descripcion, cantidad, precio_unitario, total)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                doc_id,
                p.get("nombre"),
                p.get("descripcion", ""),
                p.get("cantidad"),
                p.get("precio_unitario"),
                p.get("total")
            ))

    conn.commit()
    conn.close()
    print(f"✅ Datos guardados en {db_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python export_sqlite.py <entrada.json> <base_datos.db>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
