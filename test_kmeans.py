import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import io

st.set_page_config(layout="wide")

# Tambahkan background Gummy pakai CSS
st.markdown(
    """
    <style>
    body {
        background-image: url('gummy.png');
        background-size: cover;
        background-position: center;
    }
    .main > div {
        background-color: rgba(255, 255, 255, 0.9); /* agar konten tidak ketimpa */
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Konten utama
st.title("🎨 Image Color Picker")
st.markdown("Unggah gambar untuk mendapatkan 5 warna paling dominan menggunakan K-Means.")

uploaded_file = st.file_uploader("Upload file gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='📷 Gambar yang diunggah', use_column_width=True)

    img_data = np.array(image)
    if img_data.shape[-1] == 4:
        img_data = img_data[:, :, :3]  # buang alpha channel kalau ada

    img_data = img_data.reshape((-1, 3))

    # Jalankan K-Means
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(img_data)
    colors = kmeans.cluster_centers_.astype(int)

    st.subheader("🎨 Palet Warna Dominan")
    cols = st.columns(5)
    for i, col in enumerate(cols):
        hex_color = '#%02x%02x%02x' % tuple(colors[i])
        with col:
            st.markdown(
                f"<div style='width:100%; height:100px; background-color:{hex_color}; border-radius:8px;'></div>",
                unsafe_allow_html=True
            )
            st.markdown(f"<center>{hex_color}</center>", unsafe_allow_html=True)
