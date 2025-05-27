import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage import color
import base64

# --- Fungsi untuk mengonversi gambar lokal ke Base64 ---
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# --- Path ke gambar background Anda ---
background_image_path = "gummy.png"

# --- Konversi gambar background ke Base64 ---
encoded_image = ""
try:
    encoded_image = get_base64_encoded_image(background_image_path)
    background_image_url = f"data:image/png;base64,{encoded_image}"
except FileNotFoundError:
    st.error(f"Error: Gambar background '{background_image_path}' tidak ditemukan. Pastikan berada di folder yang sama.")
    background_image_url = "" # Fallback to no image
except Exception as e:
    st.error(f"Error saat memproses 'gummy.png' sebagai background: {e}")
    background_image_url = ""


# === CSS Custom untuk mempercantik tampilan ===
st.markdown(f"""
    <style>
    /* Menghilangkan celah di atas dan mengatur background dasar untuk seluruh halaman */
    html, body {{
        margin: 0 !important;
        padding: 0 !important;
        height: 100%; /* Pastikan body mengambil tinggi penuh */
        background-color: #FEEAE8 !important; /* Fallback jika gambar tidak muncul */
        color: #51302D !important; /* Warna teks default */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* Mengatur gambar latar belakang untuk seluruh aplikasi Streamlit */
    .stApp {{
        background-image: url("{background_image_url}") !important;
        background-size: cover !important; /* Menutupi seluruh area */
        background-position: center !important; /* Memposisikan gambar di tengah */
        background-repeat: no-repeat !important; /* Jangan ulangi gambar */
        background-attachment: fixed !important; /* Membuat background tetap saat scroll */
        background-color: #FEEAE8 !important; /* Warna fallback jika gambar tidak muncul */
        min-height: 100vh; /* Pastikan tinggi minimal 100% viewport height */
        padding-top: 0 !important; /* Hapus padding default atas */
    }}

    /* Mengatur gaya untuk kontainer utama konten agar terlihat di atas background */
    /* Ini adalah div yang membungkus sebagian besar konten Streamlit (main content area) */
    /* Targetkan elemen yang paling relevan yang membungkus konten utama */
    .st-emotion-cache-z5fcl4 > div > div {{ /* Ini biasanya div pembungkus utama konten Streamlit */
        background-color: rgba(249, 202, 197, 0.9) !important; /* #F9CAC5 dengan transparansi */
        padding: 30px !important; /* Tambah padding */
        border-radius: 15px !important;
        box-shadow: 0px 8px 25px rgba(81, 48, 45, 0.5) !important; /* Bayangan lebih menonjol */
        margin: 50px auto !important; /* Jarak dari atas/bawah dan di tengah secara horizontal */
        max-width: 900px !important; /* Batasi lebar agar tidak terlalu melebar */
        width: 90% !important; /* Responsif: 90% dari lebar parent */
    }}
    /* Pastikan elemen Streamlit lainnya yang mungkin memiliki background juga transparan atau sesuai */
    .st-emotion-cache-1c7y2vl, .css-1aumxhk {{
        background-color: transparent !important;
    }}


    h1, h2, h3 {{
        color: #51302D !important; /* Warna gelap untuk judul */
        text-align: center;
        padding: 15px !important;
        background-color: #FDC5CB !important; /* #FDC5CB untuk judul */
        border-radius: 10px !important;
        margin-bottom: 30px !important;
        box-shadow: 0px 3px 8px rgba(81, 48, 45, 0.3) !important;
    }}

    /* Gaya untuk gambar yang diunggah */
    .stImage {{
        border-radius: 10px !important;
        box-shadow: 0px 0px 15px rgba(81, 48, 45, 0.6) !important;
        margin-bottom: 25px !important;
    }}

    /* Gaya untuk tombol */
    .stButton > button {{
        background-color: #51302D !important; /* Warna gelap dari palet */
        color: #FEEAE8 !important; /* Warna terang untuk teks tombol */
        font-weight: bold;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 25px !important;
        cursor: pointer;
        box-shadow: 0px 5px 10px rgba(81, 48, 45, 0.4) !important;
        transition: background-color 0.3s ease, transform 0.2s ease !important;
    }}

    .stButton > button:hover {{
        background-color: #7a4a47 !important; /* Sedikit lebih terang/beda saat hover */
        transform: translateY(-2px) !important; /* Efek sedikit terangkat saat hover */
    }}

    /* Gaya untuk kotak warna dalam palet */
    .palette-color {{
        display: inline-block;
        width: 100% !important;
        height: 80px !important;
        margin: 0 !important;
        border-radius: 10px !important;
        border: 3px solid #51302D !important; /* Border gelap senada lebih tebal */
        box-shadow: 0 0 10px rgba(81, 48, 45, 0.5) !important;
        cursor: pointer;
    }}

    /* Gaya untuk st.color_picker yang tampil di bawah kotak warna */
    .stColorPicker > div > div > div:first-child {{
        display: none !important; /* Sembunyikan label 'Warna X' bawaan color_picker */
    }}
    .stColorPicker label {{
        display: none !important; /* Sembunyikan label 'Warna X' bawaan color_picker */
    }}
    .stColorPicker {{
        margin-top: 8px !important;
        padding-bottom: 15px !important;
    }}
    
    /* Gaya untuk informasi RGB/Hex */
    p {{
        color: #51302D !important; /* Warna teks untuk RGB/Hex */
        font-size: 0.95em;
        text-align: center;
        margin: 2px 0 !important;
    }}

    /* Gaya untuk File Uploader */
    .stFileUploader {{
        background-color: rgba(253, 197, 203, 0.7) !important; /* Warna #FDC5CB lebih jelas */
        border-radius: 10px !important;
        padding: 20px !important;
        margin-bottom: 25px !important;
        border: 2px dashed #51302D !important;
    }}
    
    /* Gaya untuk radio button */
    .stRadio > label {{
        color: #51302D !important; /* Warna teks untuk label radio */
        font-weight: bold;
        margin-bottom: 10px !important;
    }}
    .stRadio div[role="radiogroup"] > label {{
        color: #51302D !important; /* Warna teks untuk opsi radio */
    }}

    /* Info box, Warning box, Success box - pastikan warnanya dari palet */
    .stAlert {{
        border-radius: 8px !important;
        margin-bottom: 20px !important;
        padding: 15px !important;
        font-weight: 500;
        box-shadow: 0px 2px 5px rgba(81, 48, 45, 0.2) !important;
    }}
    .stAlert.info {{
        background-color: #FDC5CB !important; /* Warna light pink */
        color: #51302D !important; /* Warna teks gelap */
        border-left: 5px solid #51302D !important; /* Border gelap */
    }}
    .stAlert.warning {{
        background-color: #F9CAC5 !important; /* Warna pink sedang */
        color: #51302D !important;
        border-left: 5px solid #51302D !important;
    }}
    .stAlert.success {{
        background-color: #FEEAE8 !important; /* Warna paling terang */
        color: #51302D !important;
        border-left: 5px solid #51302D !important;
    }}

    /* Mengatur jarak antar elemen secara global jika diperlukan */
    .stText, .stMarkdown, .stSubheader {{
        margin-bottom: 15px !important;
    }}

    /* Pastikan .streamlit-container di mana Streamlit menempatkan konten tidak mengganggu */
    .st-emotion-cache-1f81016 {{ /* atau .main .block-container jika versi lama */
        padding: 0 !important;
        margin: 0 !important;
    }}

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

# === Konten Aplikasi Utama (dalam satu blok, di atas background gummy.png) ===

# Judul dan uploader
st.title("🎨 Image Color Picker")
st.write("Unggah gambar untuk mendapatkan **5 warna paling dominan**.")

uploaded_file = st.file_uploader("📁 Pilih sebuah gambar untuk dianalisis...", type=["jpg", "png", "jpeg"])

# === Opsi pemilihan ruang warna ===
color_space_choice = st.radio(
    "Pilih ruang warna untuk analisis:",
    ('RGB', 'Lab (Disarankan untuk hasil yang lebih intuitif)'),
    horizontal=True
)

if uploaded_file is None:
    st.info("Silakan unggah gambar di sini untuk memulai analisis.")
else:
    image = Image.open(uploaded_file)
    st.subheader("📷 Gambar yang Diunggah")
    st.image(image, caption='Gambar Asli', use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("🔍 Menganalisis warna dominan...")

    dominant_colors = []
    if color_space_choice == 'RGB':
        dominant_colors = get_dominant_colors_rgb(image, num_colors=5)
    else: # Lab
        dominant_colors = get_dominant_colors_lab(image, num_colors=5)

    st.subheader("🎯 Palet Warna Dominan:")

    # Buat kolom untuk setiap warna (horizontal)
    cols_palette_display = st.columns(5)

    for i, color_rgb in enumerate(dominant_colors):
        hex_color = '#%02x%02x%02x' % (color_rgb.item(0), color_rgb.item(1), color_rgb.item(2))
        
        with cols_palette_display[i]: 
            st.markdown(
                f'<div class="palette-color" style="background-color: {hex_color};"></div>',
                unsafe_allow_html=True
            )
            st.color_picker(f"Warna {i+1}", hex_color, label_visibility="collapsed", key=f"cp{i}")
            st.markdown(f"<p style='text-align: center; margin-bottom: 0;'>RGB: ({color_rgb.item(0)}, {color_rgb.item(1)}, {color_rgb.item(2)})</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; margin-top: 0;'>Hex: {hex_color}</p>", unsafe_allow_html=True)