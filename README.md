# Ethical hacking playground

A simple local web application built with Python Flask and SQLite for learning web security safely.

## Fitur
- Login sederhana
- Halaman profil pengguna
- Form komentar
- Halaman pencarian komentar
- Upload file dasar

## Tujuan Pembelajaran
Aplikasi ini dibuat untuk membantu pemula memahami konsep keamanan web di lingkungan lokal:
- Autentikasi dan sesi pengguna
- Validasi input form
- Upload file yang terbatas
- SQL sederhana dengan SQLite
- Struktur aplikasi web yang bersih dan mudah dipahami

## Persiapan
Pastikan Anda memiliki:
- Python 3.12+
- Docker (opsional)

## Instalasi Lokal
1. Buka terminal di folder `ethical-hacking-playground`
2. Buat virtual environment (opsional):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi:
   ```bash
   python app.py
   ```
5. Buka browser ke `http://127.0.0.1:5000`

## Akun Default
- Username: `student`
- Password: `learn123`

## Menjalankan dengan Docker
1. Build image:
   ```bash
   docker build -t ethical-hacking-playground .
   ```
2. Jalankan container:
   ```bash
   docker run -p 5000:5000 ethical-hacking-playground
   ```
3. Buka `http://127.0.0.1:5000`

## Struktur Folder
- `app.py`: logika utama aplikasi
- `database.db`: database SQLite
- `templates/`: halaman HTML
- `static/`: file CSS dan upload
- `docs/`: dokumentasi tambahan
- `requirements.txt`: daftar pustaka Python
- `Dockerfile`: image Docker untuk menjalankan aplikasi

## Penjelasan Struktur Folder
- `templates/`: menyimpan semua template HTML Jinja2
- `static/`: menyimpan assets, seperti CSS dan file upload
- `docs/`: mendokumentasikan tujuan keamanan dan cara menggunakan aplikasi

## Catatan Keamanan
Aplikasi ini sengaja sederhana untuk tujuan pembelajaran. Jangan gunakan pola autentikasi atau penyimpanan password ini di lingkungan produksi.
