import streamlit as st
import numpy as np
import time
import io
from PIL import Image

# Mengambil modul logika PCA dan metrik yang dibuat secara modular
from backend import compress_image_pca, calculate_metrics

# --- 1. KONFIGURASI HALAMAN WEBSITE ---
st.set_page_config(
    page_title="PCA Image Compression - Kelompok 4", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. STYLE TAMBAHAN ---
st.markdown("""
    <style>
    /* 1. Background Utama */
    .stApp {
        background: linear-gradient(135deg, #0A0908 0%, #151012 100%);
    }
    
    /* 2. Header Box */
    .title-container {
        background: rgba(73, 17, 28, 0.45);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 30px 20px;
        border-radius: 20px;
        margin-bottom: 35px;
        text-align: center;
        border: 1px solid rgba(242, 244, 243, 0.15);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37), 
                    0 0 20px rgba(73, 17, 28, 0.4);
    }
    
    .main-title { 
        font-size: 3rem; 
        font-weight: 900; 
        color: #F2F4F3; 
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(242, 244, 243, 0.3);
    }
    
    .sub-title { 
        color: rgba(242, 244, 243, 0.75); 
        font-size: 1.15rem; 
        font-weight: 400;
        margin-top: 10px;
        letter-spacing: 1px;
    }
    
    /* 3. Panel Kontrol Kanan */
    .right-panel {
        background: rgba(73, 17, 28, 0.3);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: 28px;
        border-radius: 20px;
        border: 1px solid rgba(73, 17, 28, 0.5);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    }
    
    /* 4. Mempercantik Teks & Judul Kolom */
    .column-label {
        color: #F2F4F3;
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
        border-left: 4px solid #49111C;
        padding-left: 10px;
    }
    
    h3, h4, label { 
        color: #F2F4F3 !important; 
        font-weight: 700 !important;
    }
    
    .stMarkdown p { 
        color: rgba(242, 244, 243, 0.9) !important; 
        font-size: 1.05rem;
    }
    
    /* 5. Mengubah File Uploader bawaan Streamlit */
    section[data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 2px dashed rgba(242, 244, 243, 0.2) !important;
        border-radius: 15px !important;
        padding: 10px;
    }
    
    /* 6. Tombol Download Premium */
    div.stDownloadButton > button {
        background: linear-gradient(45deg, #F2F4F3 0%, #E2E4E3 100%) !important;
        color: #0A0908 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
    }
    
    div.stDownloadButton > button:hover {
        background: linear-gradient(45deg, #49111C 0%, #6C1A29 100%) !important;
        color: #F2F4F3 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(73, 17, 28, 0.6) !important;
    }
    
    /* 7. Merapikan garis pembatas */
    hr {
        border-color: rgba(242, 244, 243, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Judul
st.markdown("""
    <div class="title-container">
        <div class="main-title">Image Compression</div>
        <div class="sub-title">Fakultas Teknologi Informasi dan Sains Data - Informatika UNS</div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. PROSES LOGIKA BACKEND ---
if uploaded_file := st.file_uploader("Choose File", type=["jpg", "jpeg", "png", "webp", "bmp"], key="file_picker"):
    try:
        img_asli = Image.open(uploaded_file)
        
        # Untuk mengecilkan scale dimensi piksel gambar asli agar mudah diolah
        MAX_RESOLUTION = 1000
        if img_asli.width > MAX_RESOLUTION or img_asli.height > MAX_RESOLUTION:
            img_asli.thumbnail((MAX_RESOLUTION, MAX_RESOLUTION), Image.Resampling.LANCZOS)
            st.warning("⚠️ Gambar telah di-downscale secara otomatis agar proses hitung PCA lebih cepat.")
        
        img_array = np.array(img_asli)
        
        if len(img_array.shape) != 3:
            st.error("Silakan unggah gambar berwarna.")
            has_image = False
        else:
            height, width, _ = img_array.shape
            max_components = min(height, width)
            has_image = True
            
            # Membaca nilai slider secara aman
            comp_val = st.session_state.slider_components if 'slider_components' in st.session_state else min(50, max_components)
            
            # Eksekusi kompresi PCA & Catat Runtime
            start_time = time.time()
            img_kompresi_array = compress_image_pca(img_array, comp_val)
            runtime = time.time() - start_time
            
            img_hasil = Image.fromarray(img_kompresi_array)
            
            # Hitung metrik MSE & PSNR
            mse_val, psnr_val = calculate_metrics(img_array, img_kompresi_array)
            
            # Hitung ukuran file fisik (KB)
            ukuran_asli_kb = round(uploaded_file.size / 1024, 2)
            
            buffer = io.BytesIO()
            img_hasil.save(buffer, format="JPEG")
            byte_im = buffer.getvalue()
            ukuran_kompresi_kb = round(buffer.getbuffer().nbytes / 1024, 2)
            
    except Exception as e:
        st.error(f"Terjadi kesalahan pembacaan file: {str(e)}")
        has_image = False
else:
    has_image = False

# --- 4. TAMPILAN 2 KOLOM UTAMA (60% Kiri, 40% Kanan) ---
main_col1, main_col2 = st.columns([6, 4], gap="large")

# --- TAMPILAN KOLOM KIRI (WORKSPACE AREA) ---
with main_col1:
    st.subheader("📸 Workspace Area")
    st.markdown("---")
    
    preview_col1, preview_col2 = st.columns(2)
    
    if has_image:
        with preview_col1:
            st.markdown('<p class="column-label">Before</p>', unsafe_allow_html=True)
            st.image(img_asli, width=340)
            st.markdown(f"📦 **Ukuran Asli:** `{ukuran_asli_kb} KB`", unsafe_allow_html=True)
        
        with preview_col2:
            st.markdown('<p class="column-label">After</p>', unsafe_allow_html=True)
            st.image(img_hasil, width=340)
            st.markdown(f"📦 **Ukuran Kompresi:** `{ukuran_kompresi_kb} KB`", unsafe_allow_html=True)
    else:
        with preview_col1:
            st.info("Belum ada gambar asli.")
        with preview_col2:
            st.info("Belum ada hasil kompresi.")

# --- TAMPILAN KOLOM KANAN (PANEL INFORMASI METRIK) ---
with main_col2:
    
    st.subheader("⚙️ Control & Info Panel")
    
    if has_image:
        st.info(f"💡 **Petunjuk Batas:** Untuk gambar ini, kamu bisa memasukkan jumlah komponen dari **1** hingga **{int(max_components)}**.")
        
        n_components = st.number_input(
            "Masukkan Jumlah PCA (Tingkat Kompresi):",
            min_value=1, max_value=int(max_components), value=min(50, max_components), step=1,
            key="slider_components"
        )
        
        if n_components == max_components:
            st.caption("ℹ️ *Skala maksimal tercapai. Kualitas gambar kembali penuh sesuai aslinya.*")
            
        st.markdown("#### 📊 Statistik Citra")
        pixel_diff_percentage = round((n_components / max_components) * 100, 2)
        st.write(f"🔹 **Persentaase Kesamaan:** {pixel_diff_percentage} %")
        st.write(f"🔹 **Compression Time:** {round(runtime, 4)} seconds")
        st.write(f"🔹 **Mean Squared Error (MSE):** `{mse_val}`")
        st.write(f"🔹 **Peak Signal-to-Noise Ratio (PSNR):** `{psnr_val} dB`")
        
        st.markdown("---")
        st.markdown("#### 📥 Action")
        
        st.download_button(
            label="Download Gambar Hasil PCA ↓",
            data=byte_im,
            file_name=f"compressed_pca_{n_components}.jpg",
            mime="image/jpeg"
        )
    else:
        st.warning("Silakan unggah gambar di area Workspace terlebih dahulu.")

# Footer Identitas Kelompok 4
st.markdown("<br><hr><center style='color: #555; font-size: 1.0rem;'>© 2026 Kelompok 4 - Tugas Project 2 Aljabar Linear</center>", unsafe_allow_html=True)