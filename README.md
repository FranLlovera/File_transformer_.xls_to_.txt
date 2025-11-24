
# Transformador Excel → Iberlibros

Transformador de catálogo Excel a formato TXT para importar en Iberlibro.
Este repositorio contiene un script en Python que procesa un fichero Excel
con catálogo de libros y genera el archivo `output/catalogo_iberlibros.txt`
listo para importar en la plataforma.

---

## Quick summary
- Script principal: `transform_excel.py`
- Dependencias: listadas en `requirements.txt` (p. ej. `pandas`, `openpyxl`)
- Entrada: un archivo `.xls` o `.xlsx` colocado en `input/`
- Salida: `output/catalogo_iberlibros.txt` y (si procede) `output/filas_descartadas.xlsx`

## Features
- Detecta automáticamente el primer archivo Excel en `input/`.
- Filtra artículos por formato (13 dígitos o 13 dígitos + `U`).
- Permite excluir artículos manualmente mediante una blacklist en el código.
- Limpieza automática de texto (saltos de línea, comillas, espacios).
- Cálculo del precio final: (Precio base × 1.17) + 0.9 — redondeado a 2 decimales.
- Genera un TXT separado por tabuladores con los 29 campos requeridos.

## Project layout

```
├── input/                      # Archivos de entrada (.xls, .xlsx)
├── output/                     # Archivos generados
├── run_transform.bat           # Script para Windows (crea/activa venv y ejecuta)
├── transform_excel.py          # Script principal
├── requirements.txt            # Dependencias Python
├── INSTRUCCIONES.txt           # Instrucciones del autor
└── backups/                    # Backups locales (no tracked)
```

Notes:
- The repository previously contained an embedded Windows Python distribution
  that was moved to `backups/` and removed from tracking. See `.gitignore`.

## Requirements
- Python 3.9+ (recommended)
- `pip` available
- On Windows use the `py` launcher if available.

## Installation (macOS / Linux)

Open a terminal in the repository root and run:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Installation (Windows - recommended with PowerShell / cmd)

```powershell
# from repo root
py -3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Manual (inside an activated venv):

```bash
python transform_excel.py
```

Windows (double click):
- Use `run_transform.bat` (created to handle venv creation/activation and filenames with spaces).

Notes:
- Place exactly one `.xls` or `.xlsx` file in `input/`. If multiple files exist the script
  will process the first and log a warning.

## Configuration
- Blacklist: edit `is_blacklisted_article()` inside `transform_excel.py` to add/remove
  article codes that must be excluded even if they match the format.

## Troubleshooting
- ModuleNotFoundError (e.g. `pandas`): activate the `venv` and run `pip install -r requirements.txt`.
- No Excel file found: ensure an `.xls` or `.xlsx` file is inside `input/`.
- If Windows users encounter issues, check they have the `py` launcher or a compatible Python installed.

## Removing large/binary files from history
If you want to permanently remove large files that were previously committed (for example
DLLs or an embedded Python distribution) this requires rewriting git history (tools such as
`git filter-repo` or BFG). This is a destructive operation for the repository history and
must be coordinated with all collaborators.

## Contributing
- Open an issue or submit a PR. Keep changes minimal and document behavior changes.

## License & Contact
- See `LICENSE.txt` for license terms (if present). For support or questions, refer to
  the author contact details in `INSTRUCCIONES.txt`.

---

Version: 1.2 (documentation added)