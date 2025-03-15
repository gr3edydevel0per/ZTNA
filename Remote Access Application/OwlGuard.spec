# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

block_cipher = None

# Get the absolute path to your project directory
project_root = os.getcwd()  # Alternative to __file__, ensures correct path

# Define data files with absolute paths
datas = [
    (os.path.join(project_root, 'templates'), 'templates'),
    (os.path.join(project_root, 'static'), 'static'),
    (os.path.join(project_root, 'assets'), 'assets'),
    (os.path.join(project_root, 'utils'), 'utils')
]

# Clean and verify the data files
def clean_data_files(data_list):
    return [(src, dst) for src, dst in data_list if os.path.exists(src)]

datas = clean_data_files(datas)

hidden_imports = collect_submodules('flask') + [
    'PyQt6.QtWebEngineWidgets',
    'PyQt6.QtWebEngineCore',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets'
]

a = Analysis(
    ['gui.py'],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OwlGuard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, 'assets', 'images', 'owl.png'),  # Ensure this file exists
    version=os.path.join(project_root, 'version.txt') if os.path.exists(os.path.join(project_root, 'version.txt')) else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OwlGuard'
)
