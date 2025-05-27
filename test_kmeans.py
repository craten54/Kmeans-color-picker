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

# --- Path ke gambar background/utama Anda ---
gummy_image_path = "gummy.png" # Asumsi gummy.png adalah gambar karakter yang Anda inginkan di kiri

# --- Konversi gambar gummy.png ke Base64 untuk ditampilkan di kolom kiri ---
gummy_encoded_image = ""
try:
    gummy_encoded_image = get_base64_encoded_image(gummy_image_path)
    gummy_image_display_url = f"data:image/png;base64,{gummy_encoded_image}"
    gummy_image_loaded = True
except FileNotFoundError:
    st.error(f"Error: Gambar '{gummy_image_path}' tidak ditemukan. Pastikan berada di folder yang sama.")
    gummy_image_loaded = False
except Exception as e:
    st.error(f"Error saat memproses '{gummy_image_path}': {e}")
    gummy_image_loaded = False


# === CSS Custom untuk mempercantik tampilan dengan palet baru dan tata letak kolom ===
st.markdown(f"""
    <style>
    /* Mengatur warna dasar body */
    body {{
        background-color: #FEEAE8; /* Warna paling terang dari palet */
        color: #51302D; /* Warna teks utama */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* Hapus background global dari stApp, karena kita akan pakai kolom */
    .stApp {{
        background-image: none;
        background-color: #FEEAE8; /* Pastikan warna dasar yang sama */
        padding: 0; /* Hapus padding default stApp */
    }}

    /* Container utama Streamlit (biasanya elemen yang membungkus konten) */
    /* st-emotion-cache-1c7y2vl untuk main container, css-1aumxhk untuk sidebar, st-emotion-cache-z5fcl4 untuk stVerticalBlock, [data-testid="stVerticalBlock"] > div > div untuk konten utama */
    /* Kita akan target elemen yang membungkus konten di kolom kanan */
    .st-emotion-cache-1c7y2vl, 
    .css-1aumxhk, 
    .st-emotion-cache-z5fcl4, 
    [data-testid="stVerticalBlock"] > div > div {{
        background-color: transparent !important; /* Biarkan transparan di level ini */
        padding: 0 !important; /* Hapus padding default */
    }}

    /* Ini adalah div yang membungkus konten aplikasi di kolom kanan */
    .right-column-content {{
        background-color: rgba(249, 202, 197, 0.9); /* #F9CAC5 dengan sedikit transparansi */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(81, 48, 45, 0.3); /* Bayangan gelap senada */
        margin-left: 10px; /* Jarak dari gambar kiri */
        margin-right: 10px;
        flex-grow: 1; /* Pastikan mengisi ruang */
        height: fit-content; /* Sesuaikan tinggi dengan konten */
    }}

    h1, h2, h3 {{
        color: #51302D; /* Warna gelap untuk judul */
        text-align: center;
        padding-top: 10px;
        padding-bottom: 10px;
        background-color: rgba(253, 197, 203, 0.7); /* #FDC5CB semi-transparan untuk judul */
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0px 2px 5px rgba(81, 48, 45, 0.2);
    }}

    /* Mengatur gaya untuk gambar yang diunggah di aplikasi */
    .stImage {{
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(81, 48, 45, 0.5); /* Bayangan gelap */
        margin-bottom: 15px;
    }}

    /* Gaya untuk tombol */
    .stButton > button {{
        background-color: #51302D; /* Warna gelap dari palet */
        color: #FEEAE8; /* Warna terang untuk teks tombol */
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
        box-shadow: 0px 4px 8px rgba(81, 48, 45, 0.3);
        transition: background-color 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: #7a4a47; /* Sedikit lebih terang/beda saat hover */
    }}

    /* Gaya untuk kotak warna dalam palet */
    .palette-color {{
        display: inline-block;
        width: 100%;
        height: 80px;
        margin: 0;
        border-radius: 10px;
        border: 2px solid #51302D; /* Border gelap senada */
        box-shadow: 0 0 8px rgba(81, 48, 45, 0.4);
        cursor: pointer;
    }}

    /* Gaya untuk st.color_picker yang tampil di bawah kotak warna */
    .stColorPicker > div > div > div:first-child {{
        display: none; /* Sembunyikan label 'Warna X' bawaan color_picker */
    }}
    .stColorPicker label {{
        display: none; /* Sembunyikan label 'Warna X' bawaan color_picker */
    }}
    .stColorPicker {{
        margin-top: 5px;
        padding-bottom: 10px; /* Tambah padding bawah untuk color picker */
    }}
    
    /* Gaya untuk informasi RGB/Hex */
    p {{
        color: #51302D; /* Warna teks untuk RGB/Hex */
        font-size: 0.9em;
    }}

    /* Gaya untuk File Uploader */
    .stFileUploader {{
        background-color: rgba(253, 197, 203, 0.5); /* Warna #FDC5CB semi-transparan */
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px dashed #51302D;
    }}
    
    /* Gaya untuk radio button */
    .stRadio > label {{
        color: #51302D; /* Warna teks untuk label radio */
        font-weight: bold;
    }}
    .stRadio div[role="radiogroup"] > label {{
        color: #51302D; /* Warna teks untuk opsi radio */
    }}

    /* Info box */
    .stAlert {{
        background-color: rgba(254, 234, 232, 0.9); /* #FEEAE8 semi-transparan */
        color: #51302D;
        border-left: 5px solid #FDC5CB; /* Border warna highlight */
        border-radius: 8px;
    }}

    </style>
""", unsafe_allow_html=True)

# === Fungsi untuk mengambil warna dominan menggunakan K-Means (ruang RGB) ===
def get_dominant_colors_rgb(image, num_colors=5):
    """
    Mengambil warna dominan dari gambar menggunakan K-Means pada ruang warna RGB.
    """
    image_array = np.array(image)
    # Reshape array menjadi 2D (piksel, RGB)
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
    
    # Ubah gambar dari RGB ke Lab
    # Perhatikan: scikit-image mengharapkan input gambar dalam range [0, 1] jika float,
    # atau [0, 255] jika uint8. PIL Image.open() biasanya memberikan uint8.
    lab_image = color.rgb2lab(image_array)
    
    # Reshape array menjadi 2D (piksel, Lab)
    reshaped_lab_image = lab_image.reshape(-1, 3) # Perbaikan: Gunakan lab_image, bukan lab_lab_image
    
    # Latih model K-Means pada data piksel di ruang Lab
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(reshaped_lab_image)
    
    dominant_lab_colors = kmeans.cluster_centers_
    
    # Ubah kembali dari Lab ke RGB
    # Hasilnya akan dalam float [0, 1], jadi perlu dikalikan 255 dan diubah ke int
    dominant_rgb_colors = (color.lab2rgb(dominant_lab_colors) * 255).astype(int)
    
    return dominant_rgb_colors

# === Tata Letak dengan Kolom ===
col1, col2 = st.columns([1, 2]) # Kolom kiri 1 bagian, kolom kanan 2 bagian

with col1:
    if gummy_image_loaded:
        st.markdown(f"""
            <img src="{gummy_image_display_url}" style="width: 100%; height: auto; border-radius: 10px; box-shadow: 0px 0px 20px rgba(81, 48, 45, 0.7);">
            """, unsafe_allow_html=True)
    else:
        st.warning("Gambar `gummy.png` tidak dapat dimuat di sini.")

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

        for i, color_rgb in enumerate(dominant_colors): # Ganti nama variabel agar tidak konflik dengan `color` dari skimage
            # Menggunakan .item() untuk mendapatkan nilai skalar dari array NumPy, menghindari error format
            hex_color = '#%02x%02x%02x' % (color_rgb.item(0), color_rgb.item(1), color_rgb.item(2))
            
            with cols_palette_display[i]: 
                st.markdown(
                    f'<div class="palette-color" style="background-color: {hex_color};"></div>',
                    unsafe_allow_html=True
                )
                st.color_picker(f"Warna {i+1}", hex_color, label_visibility="collapsed", key=f"cp{i}")
                st.markdown(f"<p style='text-align: center; font-size: 0.9em; margin-bottom: 0;'>RGB: ({color_rgb.item(0)}, {color_rgb.item(1)}, {color_rgb.item(2)})</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-size: 0.9em; margin-top: 0;'>Hex: {hex_color}</p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # Penutup wrapper konten kanan