# -*- mode: python ; coding: utf-8 -*-
import pandas

block_cipher = None

a = Analysis(
    ['login.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('../backend', 'backend'),  # Adjusted path to point to the backend directory
        ('*', 'frontend'),            # Include all files in frontend
        ('images/*', 'frontend/images'),  # Include images in frontend/images
        ('assist/*', 'assist')  # بدل ../assist
    # Adjusted path to point to the assist directory
    ],
    hiddenimports=['PyQt6', 'bcrypt', 'pandas', 'sqlalchemy'],
    hookspath=[],
    hooksconfig={},
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
    [],
    exclude_binaries=True,
    name='login',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='login'
)