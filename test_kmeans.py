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

# --- Path ke gambar gummy Anda (akan jadi background sidebar) ---
gummy_sidebar_bg_path = "gummy.png"

# --- Konversi gambar gummy.png ke Base64 untuk background sidebar ---
gummy_sidebar_bg_url = ""
try:
    encoded_gummy_sidebar_bg = get_base64_encoded_image(gummy_sidebar_bg_path)
    gummy_sidebar_bg_url = f"data:image/png;base64,{encoded_gummy_sidebar_bg}"
except FileNotFoundError:
    st.error(f"Error: Gambar background sidebar '{gummy_sidebar_bg_path}' tidak ditemukan. Pastikan berada di folder yang sama.")
except Exception as e:
    st.error(f"Error saat memproses '{gummy_sidebar_bg_path}' sebagai background sidebar: {e}")

# === CSS Custom untuk mempercantik tampilan ===
st.markdown(f"""
    <style>
    /* Reset margin dan padding default Streamlit dan browser */
    html, body, #root, [data-testid="stAppViewContainer"] {{
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh !important; /* Pastikan tinggi penuh viewport */
        overflow-x: hidden !important; /* Hindari scrollbar horizontal yang tidak diinginkan */
        background-color: #FEEAE8 !important; /* Fallback jika main content tidak diatur */
    }}

    /* Mengatur background untuk main content area (di luar sidebar) */
    .stApp {{
        background-color: #FEEAE8 !important; /* Background main content dari palet (#FEEAE8) */
        background-image: none !important; /* Pastikan tidak ada gambar background di sini */
        padding: 0 !important;
        margin: 0 !important;
        height: 100vh !important; /* Pastikan tinggi penuh */
    }}

    /* Gaya untuk Sidebar */
    .stSidebar {{
        background-image: url("{gummy_sidebar_bg_url}") !important;
        background-size: cover !important; /* Menutupi seluruh area sidebar */
        background-position: center !important; /* Memposisikan gambar di tengah */
        background-repeat: no-repeat !important; /* Jangan ulangi gambar */
        background-attachment: fixed !important; /* Membuat background tetap saat scroll */
        min-width: 400px !important; /* Lebar minimum sidebar, atur sesuai keinginan */
        width: 400px !important; /* Lebar tetap sidebar */
        max-width: 400px !important; /* Lebar maksimum sidebar */
        padding: 0 !important; /* Hapus padding internal sidebar agar gambar mengisi penuh */
        box-shadow: 5px 0px 15px rgba(0, 0, 0, 0.4) !important; /* Bayangan di sisi kanan sidebar */
        overflow-y: hidden !important; /* Hindari scroll di sidebar jika hanya berisi gambar */
    }}

    /* Menyembunyikan tombol expand/collapse sidebar */
    [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}

    /* Menyembunyikan konten selain gambar di dalam sidebar jika ada (misal padding/margin default) */
    .stSidebar > div > div {{
        padding: 0 !important;
        margin: 0 !important;
        background-color: transparent !important; /* Pastikan transparan agar gambar terlihat */
    }}
    /* Pastikan gambar di dalam sidebar mengisi penuh dan terpusat */
    .stSidebar img {{
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        border-radius: 0 !important;
        box-shadow: none !important;
    }}

    /* Untuk main content area (di luar sidebar) */
    .main .block-container {{
        background-color: transparent !important; /* Pastikan ini transparan agar warna stApp terlihat */
        padding-top: 2rem !important; /* Padding atas untuk konten utama */
        padding-right: 2rem !important;
        padding-left: 2rem !important;
        padding-bottom: 2rem !important;
        color: #51302D !important; /* Warna teks utama untuk konten */
    }}

    h1, h2, h3 {{
        color: #51302D !important; /* Warna gelap untuk judul */
        text-align: center;
        padding: 15px !important;
        background-color: #FDC5CB !important; /* #FDC5CB untuk judul di main content */
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
    .stText, .stMarkdown, .stSubheader, .stRadio {{
        margin-bottom: 15px !important;
    }}

    /* Penyesuaian responsif untuk layar kecil (mobile) */
    @media (max-width: 768px) {{
        .stSidebar {{
            min-width: 100% !important;
            width: 100% !important;
            max-width: 100% !important;
            height: 200px !important; /* Tinggi tetap untuk gambar gummy di atas */
            overflow-y: hidden !important;
        }}
        .main .block-container {{
            padding: 1rem !important; /* Kurangi padding di layar kecil */
        }}
        /* Konten aplikasi di main content akan secara otomatis berada di bawah sidebar */
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

# === Konten Sidebar (Hanya Gambar Gummy) ===
with st.sidebar:
    if gummy_sidebar_bg_url:
        # Gunakan st.markdown untuk menyisipkan gambar sebagai bagian dari sidebar,
        # yang akan diatur oleh CSS sebagai background
        # Tidak perlu st.image di sini karena kita ingin background, bukan elemen gambar biasa.
        # st.markdown(f'<div class="sidebar-image-container" style="background-image: url({gummy_sidebar_bg_url});"></div>', unsafe_allow_html=True)
        # Atau, lebih sederhana, biarkan CSS .stSidebar yang mengatur background-nya.
        # Jika Anda ingin ada elemen <img> di dalam sidebar, cukup seperti ini:
        # st.image(gummy_sidebar_bg_path, use_container_width=True) # Ini akan dimasukkan ke dalam sidebar
        # Untuk kasus ini, karena Anda ingin "background" dari sidebar, kita tidak perlu elemen di sini
        # Cukup pastikan CSS .stSidebar bekerja.
        pass # Tidak ada konten Streamlit di dalam sidebar ini, hanya CSS background
    else:
        st.warning("Gambar `gummy.png` tidak dapat dimuat di sidebar.")


# === Konten Aplikasi Utama (di area main content) ===

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