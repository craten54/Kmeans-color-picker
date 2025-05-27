import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage import color 
import base64

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

background_image_path = "gummy.png" 

try:
    encoded_image = get_base64_encoded_image(background_image_path)
    background_image_url = f"data:image/png;base64,{encoded_image}" 
except FileNotFoundError:
    st.error(f"Error: Gambar background '{background_image_path}' tidak ditemukan. Pastikan berada di folder yang sama.")
    background_image_url = ""


st.markdown(f"""
    <style>
    body {{
        background-color: #1e1e2f; /* Fallback color */
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* Mengatur gambar latar belakang untuk seluruh aplikasi Streamlit */
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover; /* Menutupi seluruh area */
        background-position: center; /* Memposisikan gambar di tengah */
        background-repeat: no-repeat; /* Jangan ulangi gambar */
        background-attachment: fixed; /* Membuat background tetap saat scroll */
        background-color: #1e1e2f; /* Warna fallback jika gambar tidak muncul */
    }}

    h1, h2, h3 {{
        color: #f7f7f7;
        text-align: center;
        padding-top: 20px;
        /* Tambahkan background semi-transparan untuk keterbacaan teks di atas gambar */
        background-color: rgba(0, 0, 0, 0.5); 
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }}

    /* Mengatur gaya untuk kontainer utama konten agar terlihat di atas background */
    .css-1aumxhk {{ /* Ini mungkin berubah tergantung versi Streamlit, periksa dengan inspector */
        background-color: rgba(43, 43, 60, 0.8) !important; /* Latar belakang semi-transparan */
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}

    /* Gaya untuk gambar yang diunggah */
    img {{
        border-radius: 10px;
        box-shadow: 0px 0px 10px #000000aa;
    }}

    /* Gaya untuk tombol */
    .stButton > button {{
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
    }}

    .stButton > button:hover {{
        background-color: #45a049;
    }}

    /* Gaya untuk kotak warna dalam palet */
    .palette-color {{
        display: inline-block;
        width: 100%; /* Agar memenuhi kolom Streamlit */
        height: 80px;
        margin: 0; /* Sesuaikan margin jika diperlukan */
        border-radius: 10px;
        border: 2px solid #fff;
        box-shadow: 0 0 5px #ccc;
        cursor: pointer; /* Menunjukkan bisa diklik (meskipun tidak ada fungsi klik di sini) */
    }}

    /* Gaya untuk st.color_picker yang tampil di bawah kotak warna */
    .stColorPicker > div > div > div:first-child {{
        display: none; /* Sembunyikan label 'Warna X' bawaan color_picker */
    }}
    .stColorPicker label {{
        display: none; /* Sembunyikan label 'Warna X' bawaan color_picker */
    }}
    .stColorPicker {{
        margin-top: 5px; /* Sedikit spasi antara kotak warna dan color picker */
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
    reshaped_lab_image = lab_image.reshape(-1, 3)
    
    # Latih model K-Means pada data piksel di ruang Lab
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(reshaped_lab_image)
    
    dominant_lab_colors = kmeans.cluster_centers_
    
    # Ubah kembali dari Lab ke RGB
    # Hasilnya akan dalam float [0, 1], jadi perlu dikalikan 255 dan diubah ke int
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
    
    # Tampilkan gambar yang diunggah
    st.image(image, caption='📷 Gambar yang diunggah', use_container_width=True)
    st.write("🔍 Menganalisis warna dominan...")

    dominant_colors = []
    if color_space_choice == 'RGB':
        dominant_colors = get_dominant_colors_rgb(image, num_colors=5)
    else: # Lab
        dominant_colors = get_dominant_colors_lab(image, num_colors=5)

    st.subheader("🎯 Palet Warna Dominan:")
    
    # Buat kolom untuk setiap warna
    cols = st.columns(5) # Membuat 5 kolom

    for i, color in enumerate(dominant_colors):
        hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])
        
        with cols[i]:
            # Menampilkan kotak warna menggunakan markdown dengan CSS custom
            st.markdown(
                f'<div class="palette-color" style="background-color: {hex_color};"></div>',
                unsafe_allow_html=True
            )
            # st.color_picker digunakan hanya untuk menampilkan nilai hex yang bisa disalin
            # Label disembunyikan via CSS
            st.color_picker(f"Warna {i+1}", hex_color, label_visibility="collapsed", key=f"cp{i}")
            st.markdown(f"<p style='text-align: center; font-size: 0.9em; margin-bottom: 0;'>RGB: ({color[0]}, {color[1]}, {color[2]})</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 0.9em; margin-top: 0;'>Hex: {hex_color}</p>", unsafe_allow_html=True)