#  Gmail Purchase Order / Quote Classifier

Este proyecto permite conectarse a una cuenta de Gmail mediante la API de Google, descargar correos con adjuntos PDF, clasificarlos como **Purchase Orders (PO)** o **Quotes (Cotizaciones)**, y generar una salida estructurada en **JSON** con los datos principales.

---

# Características

- Lectura automática de correos vía **Gmail API (OAuth 2.0)**
- Extracción de texto desde el cuerpo y adjuntos PDF
- Clasificación inteligente según reglas lingüísticas:
  - `PO`, `Purchase Order`, `Orden de Compra`, `PO-1234` → **PO**
  - `Quote`, `Cotización`, `Quotation Request`, etc. → **QUOTE**
- Limpieza de correos de spam o marketing
- Exportación a JSON (y opcionalmente CSV o SQLite)
- Evita correos duplicados automáticamente

---

#  ConfiguraciónS

## 1 Crear un proyecto en Google Cloud Console

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear un **nuevo proyecto**.
3. Activra la **Gmail API** desde “APIs y servicios”.
4. En Credenciales → Crear credenciales → ID de cliente OAuth:
   - Tipo de aplicación: Escritorio
   - Descarga el archivo `credentials.json` y guárdalo en el directorio del proyecto.

### 2 Instalar dependencias

   En una terminal ejecutar, dentro del directorio del proyecto:

      python -m venv venv
      .\venv\Scripts\activate     # (en Windows)
      # o en Linux/Mac: source venv/bin/activate
      pip install -r requirements.txt
   

#### 3️ Autenticación inicial 

   La primera vez que ejecutes el script, se abrirá una ventana de navegador para que inicies sesión en tu cuenta de Gmail y autorices los permisos.
   Una vez hecho, se generará automáticamente un archivo token.json con el acceso autorizado.



# EJECUCION  

   Para ejecutar el script principal y clasificar los correos, ejecuta en la terminal:

   python main.py --query "newer_than:7d" --max 10 --output salida.json


   ## Parámetros disponibles:


      | Parámetro  | Descripción                                                                 |
      | ---------- | --------------------------------------------------------------------------- |
      | `--query`  | Filtro de Gmail (ejemplo: `"subject:'Purchase Order'"` o `"newer_than:1d"`) |
      | `--max`    | Número máximo de correos a procesar                                         |
      | `--output` | Nombre del archivo JSON donde se guardará la salida                         |

   *Ejemplo para leer solo correos de hoy*:

       python main.py --query "newer_than:1d" --max 20 --output salida_hoy.json


# Exportar a CSV o SQLite:

   Una vez generado tu salida.json, puedes exportarlo fácilmente:

      python export_csv.py salida.json salida.csv
      python export_sqlite.py salida.json ordenes.db

# ESTRUCTURA DEL PROYECTO

gmail_classifier/
│
├── main.py
├── gmail_client.py
├── parser.py
├── parser_heuristics.py
├── classifier.py
├── pdf_utils.py
├── export_csv.py
├── export_sqlite.py
├── requirements.txt
├── README.md
├── credentials.json
├── token.json
└── adjuntos/

#  SUPUESTOS

-Todos los correos relevantes contienen asunto identificable o PDF con texto legible.

-Los adjuntos PDF permiten extracción de texto.

-Solo se procesan correos recientes (definidos por el parámetro --query).

# EJEMPLO DE SALIDA

## PO:
  {
    "tipo_documento": "PO",
    "correo": "Juan Felipe Guevara Davila <est.juanf.guevara@unimilitar.edu.co>",
    "asunto": "PURCHASE ORDER NUMBER: SW-0000005988",
    "fecha": "Sat, 8 Nov 2025 08:24:10 -0500",
    "productos": [
      {
        "nombre": "Vinyl Floor Tiles",
        "descripcion": "Teal, Std Excelon Imperial Texture, 12 in Tile Wd, Smooth ARMSTRONG FLOORING, 51906031, Country of Origin USA",
        "cantidad": 50,
        "precio_unitario": 101.47,
        "total": 5073.5
      }
    ],
    "totales": {
      "total": 5073.5,
      "moneda": "USD"
    },
    "adjuntos": [
      {
        "nombre": "Ejemplo_de_PO.pdf",
        "tipo": "application/pdf",
        "ruta": "adjuntos/Ejemplo_de_PO.pdf"
      }
    ]
  }

# QUOTE:

 {
    "tipo_documento": "QUOTE",
    "correo": "Juan Felipe Guevara Davila <est.juanf.guevara@unimilitar.edu.co>",
    "asunto": "QUOTE",
    "fecha": "Sat, 8 Nov 2025 08:20:00 -0500",
    "productos": [
      {
        "nombre": "Producto detectado",
        "descripcion": "",
        "cantidad": 1,
        "precio_unitario": 442.58,
        "total": 442.58
      }
    ],
    "totales": {
      "total": 442.58,
      "moneda": "USD"
    },
    "adjuntos": []
  }




# AUTOR

Juan Felipe Guevara Dávila

Proyecto de clasificación de correos Gmail (PO vs QUOTE)
Universidad Militar Nueva Granada
Bogotá, Colombia 