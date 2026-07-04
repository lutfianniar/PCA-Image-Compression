import numpy as np

def compress_channel_pca(channel_matrix, n_components):
    """
    Melakukan PCA pada satu channel matriks 2D (R, G, atau B).
    Sesuai langkah-langkah di Bab 2 dokumen tugas.
    """
    # 1. Menghitung mean dari data pada tiap dimensi (fitur/kolom)
    # Persamaan (1): Mean = 1/n * sum(Xi)
    mean = np.mean(channel_matrix, axis=0)
    data_centered = channel_matrix - mean
    
    # 2. Menghitung Matriks Kovariansi
    # Persamaan (2): Cx = 1/(n-1) * sum((Xi-Mean)(Xi-Mean)^T)
    # Kita gunakan np.cov (menggunakan flag rowvar=False agar kolom sebagai variabel)
    cov_matrix = np.cov(data_centered, rowvar=False)
    
    # 3. Menghitung eigenvalue dan eigenvector
    # Persamaan (3): Cx * vm = lambda_m * vm
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    
    # 4. Urutkan nilai eigenvalue secara descending (dari besar ke kecil)
    sorted_idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_idx]
    eigenvectors = eigenvectors[:, sorted_idx]
    
    # Pilih sejumlah n_components teratas (Principal Components)
    components = eigenvectors[:, :n_components]
    
    # 5. Transformasi data ke dimensi baru (Proyeksi)
    score_matrix = np.dot(data_centered, components)
    
    # Reconstruction: Kembalikan ke dimensi asal menggunakan komponen terpilih
    recon_matrix = np.dot(score_matrix, components.T) + mean
    
    # Batasi nilai piksel agar tetap di rentang valid 0-255
    return np.clip(recon_matrix, 0, 255)

def compress_image_pca(image_array, n_components):
    """
    Memecah gambar menjadi 3 channel (RGB) untuk mempertahankan warna asli,
    melakukan PCA pada tiap channel, lalu menggabungkannya kembali.
    """
    # Pastikan jumlah komponen tidak melebihi dimensi minimum gambar
    height, width, channels = image_array.shape
    max_possible = min(height, width)
    if n_components > max_possible:
        n_components = max_possible

    # Array kontainer untuk menyimpan hasil rekonstruksi tiap channel
    compressed_channels = []
    
    # Loop untuk channel R, G, dan B (Mempertahankan warna asli sesuai spesifikasi)
    for i in range(channels):
        channel_data = image_array[:, :, i].astype(float)
        recon_channel = compress_channel_pca(channel_data, n_components)
        compressed_channels.append(recon_channel)
        
    # Gabungkan kembali 3 channel (RGB) menjadi satu kesatuan gambar 3D
    compressed_image = np.dstack(compressed_channels)
    
    return compressed_image.astype(np.uint8)

def calculate_metrics(img_asli_array, img_hasil_array):
    """
    Menghitung nilai Mean Squared Error (MSE) dan Peak Signal-to-Noise Ratio (PSNR)
    antara gambar asli dan gambar hasil kompresi PCA.
    """
    # Pastikan tipe data berupa float untuk kalkulasi presisi
    asli = img_asli_array.astype(float)
    hasil = img_hasil_array.astype(float)
    
    # 1. Rumus MSE: Rata-rata dari (Gambar Asli - Gambar Hasil)^2
    mse = np.mean((asli - hasil) ** 2)
    
    # 2. Rumus PSNR
    if mse == 0:
        # Jika MSE = 0 artinya gambar identik sempurna (tidak ada noise)
        psnr = float('inf') 
    else:
        max_pixel = 255.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
        
    return round(mse, 4), round(psnr, 2)