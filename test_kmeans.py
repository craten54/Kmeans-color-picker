import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage import color

# === CSS Custom untuk mempercantik tampilan ===
st.markdown("""
    <style>
    body {
        background-color: #1e1e2f; /* Warna background gelap */
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    h1, h2, h3 {
        color: #f7f7f7;
        text-align: center;
        padding-top: 20px;
        /* Hapus background semi-transparan jika tidak diperlukan di sini */
    }

    /* Mengatur warna latar belakang untuk elemen utama Streamlit */
    .stApp {
        background-color: #1e1e2f; /* Pastikan background aplikasi tetap gelap */
    }

    /* Mengatur gaya untuk kontainer utama konten */
    /* Ini adalah div yang membungkus sebagian besar konten Streamlit */
    .css-1aumxhk { /* Ini mungkin berubah tergantung versi Streamlit, periksa dengan inspector */
        background-color: #2b2b3c !important; /* Latar belakang untuk blok konten */
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* Gaya untuk gambar yang diunggah di dalam kolom */
    .stImage {
        border-radius: 10px;
        box-shadow: 0px 0px 10px #000000aa;
    }

    /* Gaya untuk tombol */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
    }

    .stButton > button:hover {
        background-color: #45a049;
    }

    /* Gaya untuk kotak warna dalam palet */
    .palette-color {
        display: inline-block;
        width: 100%; /* Agar memenuhi kolom Streamlit */
        height: 80px;
        margin: 0; /* Sesuaikan margin jika diperlukan */
        border-radius: 10px;
        border: 2px solid #fff;
        box-shadow: 0 0 5px #ccc;
        cursor: pointer;
    }

    /* Gaya untuk st.color_picker yang tampil di bawah kotak warna */
    .stColorPicker > div > div > div:first-child {
        display: none; /* Sembunyikan label 'Warna X' bawaan color_picker */
    }
    .stColorPicker label {
        display: none; /* Sembunyikan label 'Warna X' bawaan color_picker */
    }
    .stColorPicker {
        margin-top: 5px; /* Sedikit spasi antara kotak warna dan color picker */
    }

    /* Mengatur lebar kolom agar gambar dan color picker bisa berdampingan */
    .st-emotion-cache-1kyxreqf { /* Ini adalah class untuk kolom utama Streamlit, mungkin berbeda */
        padding: 20px; /* Tambahkan padding di sini jika ingin ada ruang antar kolom */
    }
    </style>
""", unsafe_allow_html=True)

# === Fungsi untuk mengambil warna dominan menggunakan K-Means (ruang RGB) ===
def get_dominant_colors_rgb(image, num_colors=5):
    """
    Mengambil warna dominan dari gambar menggunakan K-Means pada ruang warna RGB.
    """
    image_array = np.array(image)
    reshaped_image = image_array.reshape(-1, 3) 
    
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(reshaped_image)
    
    dominant_colors = kmeans.cluster_centers_.astype(int)
    return dominant_colors

# === Fungsi untuk mengambil warna dominan menggunakan K-Means (ruang Lab) ===
def get_dominant_colors_lab(image, num_colors=5):
    """
    Mengambil warna dominan dari gambar menggunakan K-Means pada ruang warna Lab.
    Ini sering memberikan hasil yang lebih intuitif secara visual.
    """
    image_array = np.array(image)
    lab_image = color.rgb2lab(image_array) 
    reshaped_lab_image = lab_image.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(reshaped_lab_image)
    
    dominant_lab_colors = kmeans.cluster_centers_
    dominant_rgb_colors = (color.lab2rgb(dominant_lab_colors) * 255).astype(int)
    
    return dominant_rgb_colors

# === Judul dan uploader ===
st.title("🎨 Image Color Picker")
st.write("Unggah gambar untuk mendapatkan **5 warna paling dominan**.")

uploaded_file = st.file_uploader("📁 Pilih sebuah gambar...", type=["jpg", "png", "jpeg"])

# === Opsi pemilihan ruang warna ===
color_space_choice = st.radio(
    "Pilih ruang warna untuk analisis:",
    ('RGB', 'Lab (Disarankan untuk hasil yang lebih intuitif)'),
    horizontal=True
)

# === Jika gambar diunggah ===
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Buat dua kolom: satu untuk gambar, satu untuk palet warna
    col_image, col_palette = st.columns([0.6, 0.4]) # Rasio 60% untuk gambar, 40% untuk palet

    with col_image:
        st.subheader("📷 Gambar yang Diunggah")
        st.image(image, caption='Gambar Asli', use_container_width=True)
        st.write("---") # Garis pemisah visual
        st.write("🔍 Menganalisis warna dominan...") # Pindahkan ke bawah gambar

    with col_palette:
        st.subheader("🎯 Palet Warna Dominan")
        
        dominant_colors = []
        if color_space_choice == 'RGB':
            dominant_colors = get_dominant_colors_rgb(image, num_colors=5)
        else: # Lab
            dominant_colors = get_dominant_colors_lab(image, num_colors=5)

        # Buat kolom untuk setiap warna dalam palet (di dalam col_palette)
        # Menggunakan 1 kolom per warna agar tampilan vertikal lebih rapi di sidebar
        for i, color in enumerate(dominant_colors):
            hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])
            
            st.markdown(
                f'<div class="palette-color" style="background-color: {hex_color};"></div>',
                unsafe_allow_html=True
            )
            st.color_picker(f"Warna {i+1}", hex_color, label_visibility="collapsed", key=f"cp{i}")
            st.markdown(f"<p style='text-align: center; font-size: 0.9em; margin-bottom: 0;'>RGB: ({color[0]}, {color[1]}, {color[2]})</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 0.9em; margin-top: 0;'>Hex: {hex_color}</p>", unsafe_allow_html=True)
            st.write("---") # Garis pemisah antar warna untuk kejelasan
else:
    # Teks instruksi jika belum ada gambar yang diunggah
    st.info("Silakan unggah gambar untuk melihat palet warna dominannya.")