import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage import color 

# --- Hapus bagian Base64 encoding untuk gummy.png di sini, karena tidak lagi menjadi background utama ---
# background_image_path = "gummy.png" 
# try:
#     encoded_image = get_base64_encoded_image(background_image_path)
#     background_image_url = f"data:image/png;base64,{encoded_image}" 
# except FileNotFoundError:
#     st.error(f"Error: Gambar background '{background_image_path}' tidak ditemukan. Pastikan berada di folder yang sama.")
#     background_image_url = ""

# === CSS Custom untuk mempercantik tampilan ===
st.markdown("""
    <style>
    body {
        background-color: #1e1e2f; /* Warna background gelap default */
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Mengatur warna latar belakang untuk elemen utama Streamlit */
    .stApp {
        background-color: #1e1e2f; /* Pastikan background aplikasi tetap gelap */
    }

    h1, h2, h3 {
        color: #f7f7f7;
        text-align: center;
        padding-top: 20px;
        /* Hapus background semi-transparan di h1, h2, h3 jika ingin lebih sederhana */
        /* background-color: rgba(0, 0, 0, 0.5); */ 
        /* border-radius: 10px; */
        /* padding: 10px; */
        /* margin-bottom: 20px; */
    }

    /* Mengatur gaya untuk kontainer utama konten agar terlihat di atas background */
    /* Ini adalah div yang membungkus sebagian besar konten Streamlit */
    /* st-emotion-cache-1c7y2vl adalah class umum untuk main content wrapper */
    .st-emotion-cache-1c7y2vl, .css-1aumxhk, .st-emotion-cache-z5fcl4 { 
        background-color: rgba(43, 43, 60, 0.8) !important; /* Latar belakang semi-transparan */
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

# --- Bagian untuk mengunggah gambar utama ---
uploaded_file = st.file_uploader("📁 Pilih sebuah gambar untuk dianalisis...", type=["jpg", "png", "jpeg"])

# --- Bagian untuk menampilkan gummy.png di sebelah kiri ---
# Coba muat gummy.png sebagai gambar biasa di sidebar atau di kolom khusus
try:
    gummy_image = Image.open("gummy.png")
    display_gummy = True
except FileNotFoundError:
    st.warning("File 'gummy.png' tidak ditemukan di direktori yang sama. Tidak dapat menampilkan gambar 'gummy'.")
    display_gummy = False
except Exception as e:
    st.warning(f"Error saat memuat 'gummy.png': {e}. Pastikan format file benar.")
    display_gummy = False

# === Opsi pemilihan ruang warna ===
color_space_choice = st.radio(
    "Pilih ruang warna untuk analisis:",
    ('RGB', 'Lab (Disarankan untuk hasil yang lebih intuitif)'),
    horizontal=True
)

# === Tata Letak Kolom Utama ===
# Membagi tata letak menjadi 2 kolom: kiri untuk gummy (jika ada), kanan untuk uploader & color picker
# Atau, jika gummy tidak ada, kiri untuk uploader & color picker, kanan kosong
if display_gummy:
    # Jika gummy.png ada, buat 3 kolom: gummy | uploader+input_options | palette
    # Tapi ini bisa jadi terlalu banyak kolom dan kecil, mari coba 2 kolom utama
    # Satu untuk gummy.png, satu lagi untuk seluruh proses color picker
    col_gummy, col_main_app = st.columns([0.4, 0.6]) # 40% untuk gummy, 60% untuk aplikasi utama

    with col_gummy:
        st.subheader("🖼️ Gambar Info (gummy.png)")
        st.image(gummy_image, caption='Gambar Gummy', use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True) # Spasi

    with col_main_app: # Seluruh logika aplikasi color picker akan di sini
        if uploaded_file is None:
            st.info("Silakan unggah gambar di sini untuk memulai analisis.")
        # Jika gambar diunggah di kolom utama
        else:
            image = Image.open(uploaded_file)
            st.subheader("📷 Gambar yang Diunggah")
            st.image(image, caption='Gambar Asli', use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True) # Spasi
            st.write("🔍 Menganalisis warna dominan...")

            dominant_colors = []
            if color_space_choice == 'RGB':
                dominant_colors = get_dominant_colors_rgb(image, num_colors=5)
            else: # Lab
                dominant_colors = get_dominant_colors_lab(image, num_colors=5)

            st.subheader("🎯 Palet Warna Dominan:")
            
            # Buat kolom untuk setiap warna (horizontal)
            cols_palette_display = st.columns(5) 

            for i, color in enumerate(dominant_colors):
                hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])
                
                with cols_palette_display[i]:
                    st.markdown(
                        f'<div class="palette-color" style="background-color: {hex_color};"></div>',
                        unsafe_allow_html=True
                    )
                    st.color_picker(f"Warna {i+1}", hex_color, label_visibility="collapsed", key=f"cp{i}")
                    st.markdown(f"<p style='text-align: center; font-size: 0.9em; margin-bottom: 0;'>RGB: ({color[0]}, {color[1]}, {color[2]})</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-size: 0.9em; margin-top: 0;'>Hex: {hex_color}</p>", unsafe_allow_html=True)

else: # Jika gummy.png tidak ditemukan, aplikasi berjalan normal tanpa gambar gummy di samping
    if uploaded_file is None:
        st.info("Silakan unggah gambar untuk melihat palet warna dominannya.")
    else:
        image = Image.open(uploaded_file)
        st.subheader("📷 Gambar yang Diunggah")
        st.image(image, caption='Gambar Asli', use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True) # Spasi
        st.write("🔍 Menganalisis warna dominan...")

        dominant_colors = []
        if color_space_choice == 'RGB':
            dominant_colors = get_dominant_colors_rgb(image, num_colors=5)
        else: # Lab
            dominant_colors = get_dominant_colors_lab(image, num_colors=5)

        st.subheader("🎯 Palet Warna Dominan:")
        
        cols_palette_display = st.columns(5) # Membuat 5 kolom untuk palet

        for i, color in enumerate(dominant_colors):
            hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])
            
            with cols_palette_display[i]:
                st.markdown(
                    f'<div class="palette-color" style="background-color: {hex_color};"></div>',
                    unsafe_allow_html=True
                )
                st.color_picker(f"Warna {i+1}", hex_color, label_visibility="collapsed", key=f"cp{i}")
                st.markdown(f"<p style='text-align: center; font-size: 0.9em; margin-bottom: 0;'>RGB: ({color[0]}, {color[1]}, {color[2]})</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-size: 0.9em; margin-top: 0;'>Hex: {hex_color}</p>", unsafe_allow_html=True)