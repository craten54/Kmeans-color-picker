import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def get_dominant_colors(image, num_colors=5):
    # Ubah gambar ke array NumPy
    image_array = np.array(image)
    
    # Reshape array menjadi 2D (piksel, RGB)
    # Setiap baris adalah piksel, setiap kolom adalah komponen warna (R, G, B)
    reshaped_image = image_array.reshape(-1, 3) # -1 akan otomatis menghitung jumlah piksel
    
    # Inisialisasi K-Means
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10) # n_init disarankan untuk versi sklearn terbaru
    
    # Latih model K-Means pada data piksel
    kmeans.fit(reshaped_image)
    
    # Dapatkan centroid (warna dominan)
    dominant_colors = kmeans.cluster_centers_
    
    # Ubah nilai centroid menjadi integer (nilai RGB)
    dominant_colors = dominant_colors.astype(int)
    
    return dominant_colors

st.title("Image Color Picker")
st.write("Unggah gambar untuk mendapatkan 5 warna paling dominan.")

uploaded_file = st.file_uploader("Pilih sebuah gambar...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Gambar yang diunggah', use_column_width=True)
    st.write("")
    st.write("Menganalisis warna dominan...")

    dominant_colors = get_dominant_colors(image, num_colors=5)

    st.subheader("Palet Warna Dominan:")
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i, color in enumerate(dominant_colors):
        hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])
        with cols[i]:
            st.color_picker(f"Warna {i+1}", hex_color)
            st.write(f"RGB: ({color[0]}, {color[1]}, {color[2]})")
            st.write(f"Hex: {hex_color}")