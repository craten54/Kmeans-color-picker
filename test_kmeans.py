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
        box-shadow: 0 0
