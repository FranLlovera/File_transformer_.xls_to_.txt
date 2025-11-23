@echo off
setlocal

echo ===============================================================================
echo                    TRANSFORMADOR DE CATALOGO EXCEL A IBERLIBROS
echo ===============================================================================
echo.

REM Change to script directory (works across drives)
cd /d "%~dp0"

REM Prefer 'py -3' to create venv if available
echo Verificando entorno virtual...
if not exist "venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    py -3 -m venv venv 2>nul || python -m venv venv
)

REM Activate the virtualenv (explicit .bat)
if exist "venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call "venv\Scripts\activate.bat"
    echo Entorno activado.
) else (
    echo ADVERTENCIA: No se encontró 'venv\Scripts\activate.bat'. Asegúrate de crear el venv previamente.
)

echo.

REM ------------------------------------------------------
REM  🔥 IMPORTANTE: NO REINSTALAR DEPENDENCIAS AQUÍ
REM  (esto causaba el error con numpy/pandas)
REM ------------------------------------------------------

echo Buscando archivo Excel en la carpeta 'input'...
set "excelFile="

REM Use dir to find files (handles spaces); takes first match
for /f "delims=" %%F in ('dir /b /a-d "input\*.xls" "input\*.xlsx" 2^>nul') do (
    set "excelFile=%%~fF"
    goto foundExcel
)

:foundExcel

if "%excelFile%"=="" (
    echo ERROR: No se encontró ningún archivo Excel en la carpeta input\
    echo Inserta un archivo .xls o .xlsx antes de continuar.
    pause
    exit /b 1
)

echo Archivo encontrado: "%excelFile%"
echo.

echo ===============================================================================
echo                              INICIANDO PROCESAMIENTO
echo ===============================================================================
echo.

REM Run the Python script; venv activation should make the correct python available
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
endlocal
