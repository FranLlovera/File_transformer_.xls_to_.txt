@echo off
echo ===============================================================================
echo                    TRANSFORMADOR DE CATALOGO EXCEL A IBERLIBROS
echo ===============================================================================
echo.

echo Verificando entorno virtual...
if not exist "venv\" (
    echo Creando entorno virtual Python...
    python -m venv venv
)

echo Activando entorno virtual...
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Verificando archivo de entrada...
if not exist "input\articulos con sus precios - cleps.xls" (
    echo ERROR: No se encontro el archivo de entrada
    echo Por favor, coloca tu archivo Excel en la carpeta 'input\'
    echo El archivo debe llamarse: "articulos con sus precios - cleps.xls"
    pause
    exit /b 1
)

echo.
echo ===============================================================================
echo                              INICIANDO PROCESAMIENTO
echo ===============================================================================
echo.

python transform_excel.py

echo.
echo ===============================================================================
echo                              PROCESAMIENTO COMPLETADO
echo ===============================================================================
echo.
echo Revisa los archivos de salida en la carpeta 'output\':
echo - catalogo_iberlibros.txt (archivo principal)
echo - filas_descartadas.xlsx (filas descartadas)
echo.

pause
