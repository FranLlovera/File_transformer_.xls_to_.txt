import pandas as pd
import os
import re
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def is_valid_article_format(article):
    """
    Verifica si el artículo tiene formato válido: 13 números o 13 números + U
    """
    if pd.isna(article):
        return False
    
    article_str = str(article).strip()
    
    # Patrón para 13 números exactos
    pattern_13_digits = r'^\d{13}$'
    # Patrón para 13 números seguidos de U
    pattern_13_digits_u = r'^\d{13}U$'
    check = bool(re.match(pattern_13_digits, article_str) or re.match(pattern_13_digits_u, article_str))
    return check

def is_blacklisted_article(article):
    """
    Verifica si el artículo está en una lista de exclusión manual.
    Estos artículos se eliminarán del catálogo incluso si el formato es válido.
    """
    # ⚙️ Lista de artículos que NO deben exportarse (ampliable)
    blacklist = {
        "2803202400001",  # ARTICULOS EN LOTE
        # Agrega más aquí, por ejemplo:
        # "00000011423",
        # "1011423",
    }

    if pd.isna(article):
        return False

    article_str = str(article).strip()
    return article_str in blacklist

def clean_description(description):
    """
    Elimina saltos de línea de la descripción
    """
    if pd.isna(description):
        return ""
    return str(description).replace('\n', ' ').replace('\r', ' ').strip()

def fix_author_separators(author):
    """
    Cambia '/' por ';' en los nombres de autores y limpia espacios
    """
    if pd.isna(author):
        return ""
    # Reemplazar espacios antes de '/' y luego cambiar '/' por '; '
    author_str = str(author).replace(' /', '/').replace('/', '; ')
    return author_str

def calculate_price_with_markup(price):
    """
    Calcula el precio según la nueva fórmula: Precio Base * 1.17 + 0.9
    Donde Precio Base es el 'price' de la columna 'Precio 1'.
    
    Equivale a: (Precio Librería + 17%) + 0.9€
    """
    # Verifica si el precio es nulo o cero
    if pd.isna(price) or price == 0:
        return 0
        
    try:
        price_float = float(price)
        
        # Fórmula solicitada: (Precio base * 0.17) + Precio base + 0.9
        # Precio base * 0.17 + Precio base es igual a Precio base * 1.17
        
        # 1. Aplicar el 17% de aumento sobre el precio base
        price_after_markup = price_float * 1.17
        
        # 2. Sumar el margen fijo de 0.9
        final_price = price_after_markup + 0.9
        
        return round(final_price, 2)
        
    except ValueError:
        # Manejar el caso si 'price' no se puede convertir a float
        logger.warning(f"Advertencia: El precio '{price}' no es numérico y se ignora.")
        return 0
        
def transform_excel_to_txt(input_file, output_file, discarded_file):
    """
    Transforma el archivo Excel de entrada a formato TXT separado por tabs
    """
    try:
        logger.info(f"Iniciando procesamiento del archivo: {input_file}")
        
        # Leer el archivo Excel
        logger.info("Leyendo archivo Excel...")
        df = pd.read_excel(input_file)
        logger.info(f"Archivo leído exitosamente. Total de filas: {len(df)}")
        
        # === NUEVA LIMPIEZA INICIAL ===
        # Elimina saltos de línea (\n, \r) de todas las celdas del archivo Excel
        df = df.astype(str).replace({r'[\r\n]+': ' '}, regex=True)

        # Mostrar las columnas disponibles
        logger.info(f"Columnas encontradas: {list(df.columns)}")
        
        # Crear DataFrame para filas descartadas
        discarded_rows = []
        
       # Filtrar filas con artículos válidos y no incluidos en la lista negra
        logger.info("Filtrando artículos con formato válido y no listados en la blacklist...")

        logger.info("⚙️ Lista negra activa: se excluirán artículos definidos manualmente en 'is_blacklisted_article()'")cd 

        valid_mask = df['Artículo'].apply(is_valid_article_format)
        blacklist_mask = df['Artículo'].apply(is_blacklisted_article)

        # Filas válidas = formato correcto Y NO están en blacklist
        valid_df = df[valid_mask & ~blacklist_mask].copy()
        invalid_df = df[~valid_mask | blacklist_mask].copy()

        # Marcar las descartadas por blacklist con su motivo
        if len(invalid_df) > 0:
            # Motivo para artículos en blacklist
            invalid_df.loc[blacklist_mask, 'Motivo_Descarte'] = 'Artículo en blacklist (exclusión manual)'

            # Motivo para artículos con formato incorrecto
            invalid_df.loc[~valid_mask, 'Motivo_Descarte'] = 'Formato de artículo inválido (no es 13 dígitos o 13 dígitos+U)'

            discarded_rows.append(invalid_df)

        logger.info(f"Filas válidas: {len(valid_df)}")
        logger.info(f"Filas descartadas: {len(invalid_df)}")
        
        # Crear DataFrame de salida con las columnas requeridas
        logger.info("Creando estructura de datos de salida...")
        output_columns = [
            'listingid', 'title', 'author', 'illustrator', 'price', 'quantity', 
            'producttype', 'description', 'bindingtext', 'bookcondition', 
            'publishername', 'placepublished', 'yearpublished', 'isbn', 
            'sellercatalog1', 'sellercatalog2', 'sellercatalog3', 'abecategory', 
            'keywords', 'jacketcondition', 'editiontext', 'printingtext', 
            'signedtext', 'volume', 'size', 'imgurl', 'weight', 'weightunit', 
            'shippingtemplateid', 'language'
        ]
        
        output_df = pd.DataFrame(columns=output_columns)
        
        # Realizar transformaciones
        logger.info("Aplicando transformaciones...")
        
        output_df['listingid'] = valid_df['Artículo']
        output_df['title'] = valid_df['Descripción'].apply(clean_description)
        output_df['author'] = valid_df['Autor'].apply(fix_author_separators)
        output_df['illustrator'] = ''  # Vacío
        output_df['price'] = valid_df['Precio 1'].apply(calculate_price_with_markup)
        output_df['quantity'] = 1  # Siempre 1
        output_df['producttype'] = 'libro'  # Asumiendo que son libros
        output_df['description'] = ''  # Vacío
        output_df['bindingtext'] = ''  # Vacío
        output_df['bookcondition'] = 'bueno'  # Siempre 'bueno'
        output_df['publishername'] = valid_df['Editorial']
        output_df['placepublished'] = ''  # Vacío
        output_df['yearpublished'] = ''  # Vacío
        output_df['isbn'] = valid_df['Artículo']  # Usar el artículo como ISBN
        output_df['sellercatalog1'] = ''  # Vacío
        output_df['sellercatalog2'] = ''  # Vacío
        output_df['sellercatalog3'] = ''  # Vacío
        output_df['abecategory'] = ''  # Vacío
        output_df['keywords'] = ''  # Vacío
        output_df['jacketcondition'] = ''  # Vacío
        output_df['editiontext'] = ''  # Vacío
        output_df['printingtext'] = ''  # Vacío
        output_df['signedtext'] = ''  # Vacío
        output_df['volume'] = ''  # Vacío
        output_df['size'] = ''  # Vacío
        output_df['imgurl'] = ''  # Vacío
        output_df['weight'] = ''  # Vacío
        output_df['weightunit'] = ''  # Vacío
        output_df['shippingtemplateid'] = ''  # Vacío
        output_df['language'] = ''  # Vacío
        
        # === LIMPIEZA GLOBAL DE CAMPOS ===
        logger.info("Limpiando saltos de línea, comillas y espacios en todos los campos...")

        for col in output_df.columns:
            output_df[col] = (
                output_df[col]
                .astype(str)
                .replace({r'[\r\n]+': ' '}, regex=True)  # elimina saltos de línea
                .str.replace('"', '', regex=False)       # elimina comillas dobles
                .str.strip()                             # elimina espacios extremos
            )

        # Limpieza y normalización del campo precio
        output_df['price'] = (
            output_df['price']
            .astype(str)
            .str.replace(',', '.')
            .str.strip()
        )

        # === GUARDAR ARCHIVO FINAL ===
        logger.info(f"Guardando archivo de salida: {output_file}")
        output_df.reset_index(drop=True).to_csv(
            output_file,
            sep='\t',
            index=False,
            encoding='utf-8',
            quoting=3  # evita comillas automáticas
        )
        logger.info(f"Archivo de salida guardado exitosamente con {len(output_df)} filas")

        
        # Guardar archivo de filas descartadas
        if discarded_rows:
            logger.info(f"Guardando archivo de filas descartadas: {discarded_file}")
            discarded_df = pd.concat(discarded_rows, ignore_index=True)
            discarded_df.to_excel(discarded_file, index=False)
            logger.info(f"Archivo de descartadas guardado con {len(discarded_df)} filas")
        else:
            logger.info("No hay filas descartadas")
        
        # Resumen final
        logger.info("=== RESUMEN DEL PROCESAMIENTO ===")
        logger.info(f"Total de filas procesadas: {len(df)}")
        logger.info(f"Filas válidas exportadas: {len(output_df)}")
        logger.info(f"Filas descartadas: {len(df) - len(output_df)}")
        logger.info(f"Archivo de salida: {output_file}")
        if discarded_rows:
            logger.info(f"Archivo de descartadas: {discarded_file}")
        logger.info("Procesamiento completado exitosamente")
        
    except Exception as e:
        logger.error(f"Error durante el procesamiento: {str(e)}")
        raise

if __name__ == "__main__":
    # Configuración de directorios y archivos
    input_dir = "input"
    output_dir = "output"
    output_file = os.path.join(output_dir, "catalogo_iberlibros.txt")
    discarded_file = os.path.join(output_dir, "filas_descartadas.xlsx")

    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Buscar automáticamente un archivo Excel en la carpeta 'input'
    excel_files = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith((".xls", ".xlsx"))
    ]

    if not excel_files:
        logger.error("Error: No se encontró ningún archivo Excel en la carpeta 'input/'.")
        logger.error("Por favor, coloca un archivo .xls o .xlsx dentro de la carpeta 'input/'.")
    else:
        # Si hay más de un archivo, advertir y usar solo el primero
        if len(excel_files) > 1:
            logger.warning(f"Advertencia: Se encontraron varios archivos Excel. Se procesará solo el primero: {excel_files[0]}")

        input_file = os.path.join(input_dir, excel_files[0])
        logger.info(f"Archivo Excel detectado automáticamente: {input_file}")

        transform_excel_to_txt(input_file, output_file, discarded_file)
