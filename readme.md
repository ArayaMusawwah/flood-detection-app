# Fuzzy Flood Detector - Desktop (PyQt5)

Files:

- fuzzy_engine.py : core fuzzy functions (MF, rules, inference, defuzz)
- app.py : PyQt5 GUI application
- requirements.txt : pip install -r requirements.txt

Cara menjalankan (Linux / Windows / macOS):

1. Pastikan Python 3.8+ terinstall.
2. Buat virtualenv opsional:
   python -m venv venv
   source venv/bin/activate (Linux/macOS) or venv\\Scripts\\activate (Windows)
3. Install requirements:
   pip install -r requirements.txt
4. Jalankan aplikasi:
   python app.py

Packaging (opsional):

- Untuk membuat single executable di Windows/Linux:
  pip install pyinstaller
  pyinstaller --onefile --windowed app.py
  Jika ada masalah dengan resource matplotlib, lihat dokumentasi PyInstaller.

Catatan:

- Aplikasi ini adalah prototype untuk tugas kampus; MF dan rule disederhanakan.
- Kamu bisa mengubah parameter MF di fuzzy_engine.py
- Untuk menyimpan konfigurasi MF, tambahkan fungsionalitas save/load JSON (sudah mudah ditambahkan).
