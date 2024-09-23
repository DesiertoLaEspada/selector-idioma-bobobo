import os
import sys

block_cipher = None

# Obtener el directorio actual del script en ejecución
if getattr(sys, 'frozen', False):
    current_dir = sys._MEIPASS
else:
    current_dir = os.getcwd()  # Usamos el directorio de trabajo actual

# Ajustar rutas de los binarios (usa las rutas relativas para empaquetar)
binaries = [
    ('C:/Program Files/MKVToolNix/mkvmerge.exe', '.'), 
    ('C:/Program Files/MKVToolNix/mkvpropedit.exe', '.')
]

# Añadir iconos y otros recursos al bundle
datas = [
    ('icons/twitter_icon.png', 'icons'),
    ('icons/instagram_icon.png', 'icons'),
    ('icons/youtube_icon.png', 'icons'),
    ('icons/tiktok_icon.png', 'icons')
]

a = Analysis(
    ['idiomas.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
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
    icon='icons/icono.ico'
)