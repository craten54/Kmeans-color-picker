import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# === CSS Custom untuk mempercantik tampilan ===
st.markdown("""
    <style>
    body {
        background-color: #1e1e2f;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    h1, h2, h3 {
        color: #f7f7f7;
        text-align: center;
    }

    .css-1aumxhk {
        background-color: #2b2b3c !important;
        padding: 20px;
        border-radius: 10px;
    }

    img {
        border-radius: 10px;
        box-shadow: 0px 0px 10px #000000aa;
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
    }

    .stButton>button:hover {
        background-color: #45a049;
    }

    .palette-color {
        display: inline-block;
        width: 80px;
        height: 80px;
        margin: 10px;
        border-radius: 10px;
        border: 2px solid #fff;
        box-shadow: 0 0 5px #ccc;
    }
    </style>
""", unsafe_allow_html=True)

# === Fungsi untuk mengambil warna dominan ===
def get_dominant_colors(image, num_colors=5):
    image_array = np.array(image)
    reshaped_image = image_array.reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(reshaped_image)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    return dominant_colors

# === Judul dan uploader ===
st.title("🎨 Image Color Picker")
st.write("Unggah gambar untuk mendapatkan **5 warna paling dominan**.")

uploaded_file = st.file_uploader("📁 Pilih sebuah gambar...", type=["jpg", "png", "jpeg"])

# === Jika gambar diunggah ===
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='📷 Gambar yang diunggah', use_container_width=True)
    st.write("🔍 Menganalisis warna dominan...")

    dominant_colors = get_dominant_colors(image, num_colors=5)

    st.subheader("🎯 Palet Warna Dominan:")
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i, color in enumerate(dominant_colors):
        hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])
        with cols[i]:
            st.markdown(
                f'<div class="palette-color" style="background-color: {hex_color};"></div>',
                unsafe_allow_html=True
            )
            st.color_picker(f"Warna {i+1}", hex_color)
            st.write(f"RGB: ({color[0]}, {color[1]}, {color[2]})")
            st.write(f"Hex: {hex_color}")