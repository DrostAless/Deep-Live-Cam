# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import shutil
from PyInstaller.utils.hooks import collect_submodules

project_root = Path.cwd()


def add_data(src: str, dest: str) -> tuple[str, str]:
    return (str(project_root / src), dest)


datas = [
    add_data('modules/ui.json', 'modules'),
    add_data('models/instructions.txt', 'models'),
]

for locale_file in sorted((project_root / 'locales').glob('*.json')):
    datas.append((str(locale_file), 'locales'))

binaries = []
for binary_name in ('ffmpeg', 'ffprobe'):
    binary_path = shutil.which(binary_name)
    if binary_path:
        binaries.append((binary_path, '.'))

hiddenimports = collect_submodules('modules.processors.frame')

a = Analysis(
    ['run.py'],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='deep-live-cam',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
