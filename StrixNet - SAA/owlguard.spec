# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('core/templates', 'core/templates'),  # Include templates directory
        ('core/static', 'core/static'),        # Include static files
        ('core/utils', 'core/utils'),          # Include utils directory
        ('ui/assets', 'ui/assets'),            # Include assets directory
        ('core', 'core'),                      # Include core module
        ('ui', 'ui'),                          # Include ui module
        ('ui/assets/images/owl.ico', '.'),    # Include icon file
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebChannel',
        'flask',
        'werkzeug',
        'jinja2',
        'requests',
        'win32con',
        'win32api',
        'win32process',
        'core.server',
        'core.utils.api_helper',
        'core.utils.device_posture',
        'core.utils.device_data',
        'core.utils.vpn_manager',
        'core.utils.api_server',
        'core.utils.essentials',
        'ui.app'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PySide2', 'PySide6', 'PyQt5', 'PyQt4', '__pycache__'], 
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
    icon='ui/assets/images/owl.ico',  # Make sure this path is correct
    optimize=1,
    uac_admin=True,  # <-- This is the magic flag
)

