# PCA-Image-Compression
Penerapan Principal Component Analysis pada Kompresi Citra Digital
Aplikasi web interaktif untuk melakukan kompresi citra digital berwarna (RGB) berbasis metode Aljabar Linear **Principal Component Analysis (PCA)**. Proyek ini dibangun menggunakan **Python** dan **Streamlit** sebagai pemenuhan Tugas Project 2 Mata Kuliah Aljabar Linear.

---

## 🌟 Fitur Utama

* **Kompresi Citra RGB Interaktif**: Mampu memproses gambar berwarna secara modular dengan memisahkan channel Red, Green, dan Blue untuk mempertahankan warna asli objek.
* **Pengaturan Komponen Dinamis**: Pengguna dapat menentukan jumlah komponen utama ($n\_components$) secara presisi menggunakan input angka.
* **Metrik Evaluasi Real-Time**: Menampilkan kalkulasi performa kompresi secara langsung berupa nilai **MSE (Mean Squared Error)**, **PSNR (Peak Signal-to-Noise Ratio)**, waktu proses (*runtime*), serta persentase kesamaan informasi.
* **Sistem Pengaman Citra**: Fitur otomatis untuk melakukan *downscaling* citra beresolusi ekstrem tinggi agar menghindari *freeze* atau *crash* komputasi akibat kompleksitas $\mathcal{O}(N^3)$ dekomposisi matriks kovariansi.
* **Desain UI Premium Dark Mode**: Antarmuka responsif dengan perpaduan tema *Matte Black*, *Dark Blue*, dan aksen *Dark Red* mewah menggunakan tipografi Serif yang elegan.

---

## 🛠️ Spesifikasi Teknologi

Aplikasi ini menggunakan beberapa pustaka Python utama sebagai berikut:
* **Python** (Bahasa Pemrograman Utama)
* **Streamlit** (Framework Antarmuka Web Interaktif)
* **NumPy** (Komputasi Numerik Aljabar Linear di Backend)
* **Pillow (PIL)** (Pengolahan dan Manipulasi Berkas Citra)

---

## 🚀 Cara Menjalankan Aplikasi di Lokal

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di komputer lokal kamu:

### 1. Kloning Repositori
```bash
git clone [https://github.com/lutfianniar/PCA-Image-Compression.git](https://github.com/lutfianniar/PCA-Image-Compression.git)
cd PCA-Image-Compression
```
### 2. Instalasi Pustaka
```bash
pip install streamlit numpy pillow
```
### 3. Jalankan Server Streamlit
```bash
streamlit run src/app.py
```

---

## 📁 Struktur Direktori

```text
.
├── src/
│   ├── app.py             # File Utama Frontend (Streamlit & CSS Custom)
│   └── backend.py         # File Logika Murni PCA & Hitungan Metrik (NumPy)
│
└── README.md              # Dokumentasi Proyek GitHub
```

---

## 👥 Anggota Kelompok (Kelompok 4)
### 1. Annisa Salma Tabina (L0125004)
### 2. Lutfiannisa Tri Yuniarti (L0125020)
### 3. Gita Florensia Adi (L0125101)
