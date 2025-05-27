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

# --- Path ke gambar gummy Anda (yang akan mengisi kolom kiri) ---
gummy_image_path = "gummy.png"

# --- Konversi gambar gummy.png ke Base64 ---
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

# === CSS Custom untuk tata letak Coca-Cola dan palet warna ===
st.markdown(f"""
    <style>
    /* Menghapus celah di atas dan mengatur background dasar untuk seluruh halaman */
    html, body {{
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh !important; /* Pastikan body mengambil tinggi penuh viewport */
        overflow-x: hidden; /* Hindari scroll horizontal */
        background-color: #FEEAE8 !important; /* Warna fallback jika gambar tidak muncul */
        color: #51302D !important; /* Warna teks default */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* Pastikan .stApp juga tidak memiliki background image global dan padding/margin tambahan */
    .stApp {{
        background-image: none !important; /* Hapus background image dari stApp */
        background-color: #FEEAE8 !important; /* Warna dasar stApp */
        padding: 0 !important;
        margin: 0 !important;
        min-height: 100vh; /* Pastikan tinggi minimal 100% viewport height */
        display: flex; /* Gunakan flexbox untuk layout utama */
        flex-direction: row; /* Konten akan disusun secara horizontal */
    }}

    /* Gaya untuk sidebar Streamlit (jika ada) */
    .st-emotion-cache-1c7y2vl {{ /* ini adalah class untuk sidebar di Streamlit versi terbaru */
        background-color: #FDC5CB !important; /* Warna sidebar */
        padding: 0 !important;
        flex-shrink: 0; /* Jangan biarkan sidebar menyusut */
    }}

    /* Container utama konten Streamlit (yang membungkus col1 dan col2) */
    .st-emotion-cache-z5fcl4 > div > div {{
        background-color: transparent !important; /* Kontainer utama ini harus transparan */
        padding: 0 !important;
        margin: 0 !important;
        display: flex; /* Mengatur flexbox untuk kolom */
        width: 100%; /* Memastikan ini mengambil lebar penuh */
        height: 100vh; /* Mengambil tinggi penuh viewport */
    }}

    /* Kolom Kiri untuk gambar gummy.png */
    .st-emotion-cache-1r6dm16:first-child, /* Target kolom pertama yang dihasilkan oleh st.columns */
    [data-testid="stColumn"] > div:first-child {{
        background-color: #FEEAE8 !important; /* Background kolom kiri (paling terang) */
        flex: 1; /* Ambil proporsi lebar yang ditentukan di st.columns */
        padding: 0 !important;
        margin: 0 !important;
        display: flex;
        align-items: center; /* Pusatkan gambar secara vertikal */
        justify-content: center; /* Pusatkan gambar secara horizontal */
        overflow: hidden; /* Pastikan gambar tidak meluap */
    }}
    .left-column-image-wrapper {{
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #FEEAE8; /* Pastikan background wrapper juga senada */
    }}
    .left-column-image-wrapper img {{
        width: 100%; /* Gambar mengisi lebar wrapper */
        height: 100%; /* Gambar mengisi tinggi wrapper */
        object-fit: cover; /* Penting: agar gambar mengisi dan responsif tanpa distorsi */
        border-radius: 0 !important; /* Hapus border radius jika ingin edge-to-edge */
        box-shadow: none !important; /* Hapus bayangan jika ingin seamless */
    }}

    /* Kolom Kanan untuk konten aplikasi */
    .st-emotion-cache-1r6dm16:last-child, /* Target kolom kedua */
    [data-testid="stColumn"] > div:last-child {{
        background-color: #F9CAC5 !important; /* Background kolom kanan (pink sedang) */
        flex: 2; /* Ambil proporsi lebar yang ditentukan di st.columns */
        padding: 0 !important;
        margin: 0 !important;
        overflow-y: auto; /* Aktifkan scroll jika kontennya panjang */
        height: 100vh; /* Mengambil tinggi penuh viewport */
        display: flex;
        flex-direction: column;
        justify-content: flex-start; /* Konten dimulai dari atas */
    }}
    .right-column-content {{
        padding: 30px 40px !important; /* Padding lebih besar di dalam konten */
        flex-grow: 1; /* Pastikan konten mengisi ruang yang tersedia */
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
    .stText, .stMarkdown, .stSubheader, .stRadio {{
        margin-bottom: 15px !important;
    }}

    /* Mengatasi padding default di block-container */
    .main .block-container {{
        padding-top: 0 !important;
        padding-right: 0 !important;
        padding-left: 0 !important;
        padding-bottom: 0 !important;
    }}

    /* Penyesuaian responsif untuk layar kecil */
    @media (max-width: 768px) {{
        .stApp {{
            flex-direction: column !important; /* Ubah ke tumpukan vertikal di layar kecil */
        }}
        .st-emotion-cache-1r6dm16:first-child,
        .st-emotion-cache-1r6dm16:last-child {{
            flex: none !important; /* Hapus flex grow */
            width: 100% !important; /* Ambil lebar penuh */
            height: auto !important; /* Sesuaikan tinggi otomatis */
            padding: 20px !important;
        }}
        .left-column-image-wrapper {{
            height: 300px; /* Batasi tinggi gambar di layar kecil */
        }}
        .right-column-content {{
            padding: 20px !important; /* Kurangi padding di layar kecil */
        }}
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

# === Tata Letak Utama dengan st.columns ===
# Gunakan flexbox di CSS pada .stApp dan elemen kolom untuk mengontrol layout.
# Proporisi width untuk kolom kiri dan kanan
col1, col2 = st.columns([1, 2]) # Misalnya, gummy 1 bagian lebar, aplikasi 2 bagian lebar

with col1:
    # Wrapper untuk gambar gummy agar bisa di-align dan di-cover
    st.markdown('<div class="left-column-image-wrapper">', unsafe_allow_html=True)
    if gummy_image_loaded:
        # Gunakan st.image agar Streamlit bisa mengelola gambar, kemudian CSS akan menargetnya
        # Atau tetap pakai markdown jika ingin kontrol lebih (tapi st.image lebih mudah untuk responsif)
        # Saya akan menggunakan <img> tag dengan CSS untuk kontrol penuh over object-fit
        st.markdown(f"""
            <img src="{gummy_image_display_url}" alt="Gummy Character">
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