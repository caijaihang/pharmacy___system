# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件 - 药房进货比较系统
生成单个 EXE 文件，内含 Flask 后端 + PyQt5 WebEngine 前端
兼容 Windows 7
"""

import os
import sys

block_cipher = None

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(SPEC))

# 需要打包的数据文件（格式：('源路径', '打包内目标目录')）
added_files = [
    # 静态资源文件（HTML、JS）
    (os.path.join(PROJECT_ROOT, 'static', 'index.html'), 'static'),
    (os.path.join(PROJECT_ROOT, 'static', 'vicrocode-sdk-v001.js'), 'static'),
    # 初始数据库（首次运行时复制到 EXE 同级目录）
    (os.path.join(PROJECT_ROOT, 'pharmacy.db'), '.'),
]

# 隐式导入（PyInstaller 可能无法自动检测到的模块）
hiddenimports = [
    # Flask 相关
    'flask',
    'flask_cors',
    'werkzeug',
    'werkzeug.utils',
    'jinja2',
    'markupsafe',
    'itsdangerous',
    'click',
    # 爬虫相关
    'requests',
    'urllib3',
    'certifi',
    'charset_normalizer',
    'idna',
    'bs4',
    'lxml',
    'lxml.etree',
    # 数据处理
    'pandas',
    'pandas._libs',
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.np_datetime',
    'pandas._libs.tslibs.nattype',
    'pandas.core.arrays.masked',
    'pandas.core.arrays.arrow',
    'numpy',
    'openpyxl',
    'openpyxl.styles',
    'xlrd',
    # PyQt5 WebEngine（核心依赖）
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtWebChannel',
    'PyQt5.QtNetwork',
    'PyQt5.QtWebEngineCore',
    # 其他
    'sqlite3',
    'hashlib',
    'json',
    're',
    'threading',
    'datetime',
    'logging',
]

# 排除不需要的模块（减小体积）
excludes = [
    'tkinter',
    'matplotlib',
    'scipy',
    'IPython',
    'jupyter',
    'notebook',
    'pytest',
    'sphinx',
    'setuptools',
    'pip',
    'wheel',
    'selenium',
    'webdriver_manager',
    'retrying',
    'tenacity',
    'fake_useragent',
    'Pillow',
    'PIL',
    'gunicorn',
    'unittest',
    'distutils',
    'pydoc',
    'xmlrpc',
    'pydoc_data',
    'email',
    'html.parser',
    'antigravity',
]

a = Analysis(
    [os.path.join(PROJECT_ROOT, 'launcher.py')],
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=added_files,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[
        os.path.join(PROJECT_ROOT, 'hook-runtime.py'),  # 运行时钩子：初始化数据库
    ],
    excludes=excludes,
    noarchive=False,
    optimize=0,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='药房进货比较系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # 不显示命令行窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(PROJECT_ROOT, 'static', 'images', 'icon.ico') if os.path.exists(
        os.path.join(PROJECT_ROOT, 'static', 'images', 'icon.ico')) else None,
)
