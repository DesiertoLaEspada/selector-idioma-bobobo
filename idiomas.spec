import os
import sys

block_cipher = None

# Obtener el directorio actual del script en ejecución
if getattr(sys, 'frozen', False):
    current_dir = sys._MEIPASS
else:
    current_dir = os.getcwd()  # Usamos el directorio de trabajo actual

a = Analysis(
    ['idiomas.py'],
    pathex=[current_dir],  # Directorio actual
    binaries=[
        ('C:/Program Files/MKVToolNix/mkvmerge.exe', '.'), 
        ('C:/Program Files/MKVToolNix/mkvpropedit.exe', '.')
    ],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Selector de idioma',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    # Ruta relativa al icono (directorio actual + /icons/icono.ico)
    icon=os.path.join(current_dir, 'icons', 'icono.ico')  
)
