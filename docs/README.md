# Dokumentasi ethical hacking playground

Aplikasi ini dibuat sebagai tempat aman untuk belajar konsep dasar keamanan web secara lokal.

## Tujuan Pembelajaran
- Memahami alur login dan session
- Menulis data ke database dengan SQLite
- Menampilkan komentar dan hasil pencarian
- Memproses upload file dengan validasi sederhana
- Melihat bagaimana struktur aplikasi Flask disusun

## Bagian Utama Aplikasi
- `app.py`: titik masuk aplikasi dan rute web
- `templates/`: halaman HTML untuk setiap fitur
- `static/`: styling CSS dan direktori upload
- `database.db`: menyimpan data pengguna, komentar, dan upload

## Fitur Keamanan yang Ditunjukkan
- Validasi file upload berdasarkan ekstensi
- Penggunaan `secure_filename` untuk nama file upload
- Pemisahan logika antara route dan template
- Pesan dan peringatan sederhana untuk input yang tidak valid

## Cara Menjalankan
Ikuti instruksi pada `README.md` di root project.
