# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller 打包配置 - 药房进货比较系统"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(SPEC))

added_files = [
    (os.path.join(PROJECT_ROOT, 'static', 'index.html'), 'static'),
    (os.path.join(PROJECT_ROOT, 'static', 'vicrocode-sdk-v001.js'), 'static'),
    (os.path.join(PROJECT_ROOT, 'pharmacy.db'), '.'),
]

a = Analysis(
    [os.path.join(PROJECT_ROOT, 'launcher.py')],
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'flask_cors',
        'werkzeug.utils',
        'openpyxl.styles',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[os.path.join(PROJECT_ROOT, 'hook-runtime.py')],
    excludes=[
        'tkinter', 'matplotlib', 'scipy', 'IPython', 'jupyter', 'notebook',
        'pytest', 'sphinx', 'setuptools', 'pip', 'wheel', 'selenium',
        'webdriver_manager', 'retrying', 'tenacity', 'fake_useragent',
        'Pillow', 'PIL', 'gunicorn', 'unittest', 'distutils', 'pydoc',
        'xmlrpc', 'pydoc_data', 'email', 'antigravity',
    ],
    noarchive=False,
    optimize=0,
    cipher=None,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='药房进货比较系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(PROJECT_ROOT, 'static', 'images', 'icon.ico')
        if os.path.exists(os.path.join(PROJECT_ROOT, 'static', 'images', 'icon.ico'))
        else None,
)
