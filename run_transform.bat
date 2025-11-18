@echo off
echo ===============================================================================
echo                    TRANSFORMADOR DE CATALOGO EXCEL A IBERLIBROS
echo ===============================================================================
echo.

REM Ir a la carpeta del script .bat
cd /d "%~dp0"

echo Verificando entorno virtual...
if not exist "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
)

echo Activando entorno virtual...
call venv\Scripts\activate

echo Entorno activado.
echo.

REM ------------------------------------------------------
REM  🔥 IMPORTANTE: NO REINSTALAR DEPENDENCIAS AQUÍ
REM  (esto causaba el error con numpy/pandas)
REM ------------------------------------------------------

echo Buscando archivo Excel en la carpeta 'input'...
set "excelFile="

for %%f in (input\*.xls input\*.xlsx) do (
    set "excelFile=%%f"
    goto foundExcel
)

:foundExcel

if "%excelFile%"=="" (
    echo ERROR: No se encontró ningún archivo Excel en la carpeta input\
    echo Inserta un archivo .xls o .xlsx antes de continuar.
    pause
    exit /b 1
)

echo Archivo encontrado: %excelFile%
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
echo Revisa los archivos en la carpeta 'output\': 
echo - catalogo_iberlibros.txt
echo - filas_descartadas.xlsx
echo.

pause
