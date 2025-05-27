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

# --- Path ke gambar utama Anda (karakter gummy) ---
gummy_image_path = "gummy.png"

# --- Konversi gambar gummy.png ke Base64 untuk ditampilkan di kolom kiri ---
gummy_image_display_url = ""
gummy_image_loaded = False
try:
    gummy_encoded_image = get_base64_encoded_image(gummy_image_path)
    gummy_image_display_url = f"data:image/png;base64,{gummy_encoded_image}"
    gummy_image_loaded = True
except FileNotFoundError:
    st.error(f"Error: Gambar '{gummy_image_path}' tidak ditemukan. Pastikan berada di folder yang sama.")
except Exception as e:
    st.error(f"Error saat memproses '{gummy_image_path}': {e}")


# === CSS Custom untuk palet warna baru dan tata letak kolom yang diperbaiki ===
st.markdown(f"""
    <style>
    /* Menghapus celah di atas dan mengatur background dasar untuk seluruh halaman */
    html, body {{
        margin: 0 !important;
        padding: 0 !important;
        background-color: #FEEAE8 !important; /* Warna paling terang dari palet sebagai background dasar */
        color: #51302D !important; /* Warna teks utama */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* Pastikan .stApp juga tidak memiliki background image dan padding/margin tambahan */
    .stApp {{
        background-image: none !important;
        background-color: #FEEAE8 !important; /* Pastikan warna dasar yang sama */
        padding: 0 !important;
        margin: 0 !important;
    }}

    /* Streamlit main container, pastikan tidak ada background yang menimpa */
    .st-emotion-cache-1c7y2vl, 
    .css-1aumxhk, 
    .st-emotion-cache-z5fcl4 {{
        background-color: transparent !important; /* Transparan agar warna body terlihat */
        padding: 0 !important;
    }}

    /* Ini adalah div yang membungkus konten aplikasi di kolom kanan */
    .right-column-content {{
        background-color: rgba(249, 202, 197, 0.95); /* #F9CAC5 dengan transparansi minimal */
        padding: 25px; /* Tambah padding agar konten tidak terlalu mepet */
        border-radius: 15px;
        box-shadow: 0px 5px 20px rgba(81, 48, 45, 0.4); /* Bayangan gelap yang lebih menonjol */
        margin: 20px; /* Jarak dari tepi dan gambar kiri */
        height: auto; /* Sesuaikan tinggi dengan konten */
        min-height: calc(100vh - 40px); /* Minimal tinggi agar terisi penuh */
        display: flex;
        flex-direction: column;
        justify-content: flex-start; /* Konten dimulai dari atas */
    }}

    /* Kolom kiri untuk gambar gummy.png */
    .left-column-image {{
        display: flex;
        align-items: center; /* Vertically center the image */
        justify-content: center; /* Horizontally center the image */
        padding: 20px; /* Padding di sekitar gambar */
        background-color: #FEEAE8; /* Background kolom kiri */
        height: 100vh; /* Tinggi penuh viewport */
        position: sticky; /* Agar gambar tetap di tempatnya saat scroll */
        top: 0;
    }}

    h1, h2, h3 {{
        color: #51302D !important; /* Warna gelap untuk judul */
        text-align: center;
        padding: 15px; /* Tambah padding judul */
        background-color: #FDC5CB !important; /* #FDC5CB untuk judul */
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0px 3px 8px rgba(81, 48, 45, 0.3);
    }}

    /* Gaya untuk gambar yang diunggah di aplikasi */
    .stImage {{
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(81, 48, 45, 0.6); /* Bayangan gelap lebih kuat */
        margin-bottom: 20px;
    }}

    /* Gaya untuk tombol */
    .stButton > button {{
        background-color: #51302D !important; /* Warna gelap dari palet */
        color: #FEEAE8 !important; /* Warna terang untuk teks tombol */
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 12px 25px; /* Ukuran tombol lebih besar */
        cursor: pointer;
        box-shadow: 0px 5px 10px rgba(81, 48, 45, 0.4);
        transition: background-color 0.3s ease, transform 0.2s ease;
    }}

    .stButton > button:hover {{
        background-color: #7a4a47 !important; /* Sedikit lebih terang/beda saat hover */
        transform: translateY(-2px); /* Efek sedikit terangkat saat hover */
    }}

    /* Gaya untuk kotak warna dalam palet */
    .palette-color {{
        display: inline-block;
        width: 100%;
        height: 80px;
        margin: 0;
        border-radius: 10px;
        border: 3px solid #51302D !important; /* Border gelap senada lebih tebal */
        box-shadow: 0 0 10px rgba(81, 48, 45, 0.5);
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
        margin-top: 8px;
        padding-bottom: 15px;
    }}
    
    /* Gaya untuk informasi RGB/Hex */
    p {{
        color: #51302D !important; /* Warna teks untuk RGB/Hex */
        font-size: 0.95em;
        text-align: center;
        margin: 2px 0; /* Kurangi margin vertikal */
    }}

    /* Gaya untuk File Uploader */
    .stFileUploader {{
        background-color: rgba(253, 197, 203, 0.7) !important; /* Warna #FDC5CB lebih jelas */
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        border: 2px dashed #51302D !important;
    }}
    
    /* Gaya untuk radio button */
    .stRadio > label {{
        color: #51302D !important; /* Warna teks untuk label radio */
        font-weight: bold;
        margin-bottom: 10px;
    }}
    .stRadio div[role="radiogroup"] > label {{
        color: #51302D !important; /* Warna teks untuk opsi radio */
    }}

    /* Info box, Warning box, Success box - pastikan warnanya dari palet */
    .stAlert {{
        border-radius: 8px;
        margin-bottom: 20px;
        padding: 15px;
        font-weight: 500;
        box-shadow: 0px 2px 5px rgba(81, 48, 45, 0.2);
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
        margin-bottom: 15px;
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

# === Tata Letak dengan Kolom ===
# Gunakan st.columns([width_col1, width_col2])
# Saya sarankan 1 untuk gambar dan 2 untuk aplikasi, atau 0.8 dan 2 tergantung preferensi visual
col1, col2 = st.columns([0.8, 2]) # Kolom kiri 0.8 bagian, kolom kanan 2 bagian

with col1:
    st.markdown('<div class="left-column-image">', unsafe_allow_html=True)
    if gummy_image_loaded:
        st.markdown(f"""
            <img src="{gummy_image_display_url}" style="width: 100%; height: auto; border-radius: 15px; box-shadow: 0px 0px 25px rgba(81, 48, 45, 0.8);">
            """, unsafe_allow_html=True)
    else:
        st.warning("Gambar `gummy.png` tidak dapat dimuat di sini.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="right-column-content">', unsafe_allow_html=True) # Wrapper untuk konten di kolom kanan
    
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
    
    st.markdown('</div>', unsafe_allow_html=True) # Penutup wrapper konten kanan