import os
import subprocess
import sys
import platform

def install_pyinstaller():
    print("Checking for PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "show", "pyinstaller"])
        print("PyInstaller is already installed.")
    except subprocess.CalledProcessError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_linux():
    print("\n--- Building for Linux ---")
    # Clean previous build
    if os.path.exists("dist"):
        import shutil
        shutil.rmtree("dist", ignore_errors=True)
    if os.path.exists("build"):
        import shutil
        shutil.rmtree("build", ignore_errors=True)

    cmd = [
        "pyinstaller",
        "--name=FloodDetectionApp",
        "--onefile",
        "--windowed",
        "--add-data=logo_unpam.png:.",
        "--add-data=logoku.png:.",
        "--add-data=ui:ui",  # Include ui package if needed, though imports usually handle it
        "app.py"
    ]
    
    # On Linux, separator is :
    # On Windows, separator is ;
    
    print(f"Running command: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    print("Linux build complete. Executable is in dist/FloodDetectionApp")

def create_windows_spec():
    print("\n--- Creating Windows Spec File ---")
    spec_content = r"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('logo_unpam.png', '.'), ('logoku.png', '.'), ('ui', 'ui')],
    hiddenimports=[],
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
    name='FloodDetectionApp',
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
)
"""
    with open("FloodDetectionApp_Windows.spec", "w") as f:
        f.write(spec_content)
    
    print("Windows spec file created: FloodDetectionApp_Windows.spec")
    print("To build on Windows, run: pyinstaller FloodDetectionApp_Windows.spec")

if __name__ == "__main__":
    install_pyinstaller()
    
    if platform.system() == "Linux":
        build_linux()
        create_windows_spec()
    elif platform.system() == "Windows":
        print("Detected Windows. Please run: pyinstaller FloodDetectionApp_Windows.spec")
        create_windows_spec()
    else:
        print(f"Unsupported platform: {platform.system()}")
