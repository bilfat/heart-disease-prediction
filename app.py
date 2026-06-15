# pyrefly: ignore [missing-import]
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# pyrefly: ignore [missing-import]
import streamlit as st
from modules.prediction_engine import load_all_models
from modules import page_home, page_prediksi, page_riwayat, page_analisis, page_tentang

# ====================================
# KONFIGURASI HALAMAN & CSS
# ====================================
st.set_page_config(
    page_title="CardioCare | Portal Prediksi Penyakit Jantung",
    page_icon="❤️",
    layout="wide"
)

def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# ====================================
# INISIALISASI SESSION STATE
# ====================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "history" not in st.session_state:
    st.session_state.history = []

# Pre-load models in background/cache
models_status = load_all_models()

# ====================================
# TOP NAVIGATION BAR
# ====================================
def render_navbar():
    st.markdown('<div class="nav-container-marker"></div>', unsafe_allow_html=True)

    # Menyesuaikan rasio kolom agar muat dengan nama halaman yang baru
    col_logo, col_space, col_home, col_dash, col_pred, col_anal, col_team = st.columns(
        [3, 1.5, 1.1, 1.6, 1.6, 1.6, 1.1]
    )

    with col_logo:
        st.markdown(
            """
            <div class="nav-logo">
                <span class="nav-logo-icon">❤️</span>
                <div>
                    <h1>CardioCare</h1>
                    <div class="nav-logo-sub">Sistem Deteksi Risiko Jantung Cerdas</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    current = st.session_state.current_page

    # Navigasi disesuaikan dengan gambar referensi dari user
    nav_items = [
        ("home",     "🏠 Beranda",          "btn_home",     col_home),
        ("riwayat",  "📈 Riwayat Pengecekan",    "btn_riwayat",  col_dash),
        ("prediksi", "👤 Analisis Risiko",   "btn_prediksi", col_pred),
        ("analisis", "🧠 Analisis Model",    "btn_analisis", col_anal),
        ("tentang",  "ℹ️ Tentang",          "btn_tentang",  col_team),
    ]

    for page_key, label, btn_key, col in nav_items:
        with col:
            btn_type = "primary" if current == page_key else "secondary"
            if st.button(label, key=btn_key, type=btn_type, use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

# Render Navbar di atas halaman
render_navbar()

# ====================================
# ROUTING HALAMAN (MODULAR)
# ====================================
if st.session_state.current_page == "home":
    page_home.render()
elif st.session_state.current_page == "riwayat":
    page_riwayat.render()
elif st.session_state.current_page == "prediksi":
    page_prediksi.render()
elif st.session_state.current_page == "analisis":
    page_analisis.render()
elif st.session_state.current_page == "tentang":
    page_tentang.render()