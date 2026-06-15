# pyrefly: ignore [missing-import]
import sys
import os
import importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# pyrefly: ignore [missing-import]
import streamlit as st
from modules.prediction_engine import load_all_models
from modules import page_home, page_prediksi, page_riwayat, page_analisis, page_tentang

# Force reload modules to ensure disk updates are applied dynamically in Streamlit
importlib.reload(page_home)
importlib.reload(page_prediksi)
importlib.reload(page_riwayat)
importlib.reload(page_analisis)
importlib.reload(page_tentang)

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
                <div class="nav-logo-icon" style="display: flex; align-items: center;">
                    <svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 96 960 960" width="32" fill="#0A84FF"><path d="m480 935-41-37q-106-97-175-167.5t-110-126Q113 549 96.5 504T80 413q0-90 60.5-150.5T290 202q57 0 105.5 27t84.5 78q42-54 89-79.5T670 202q89 0 149.5 60.5T880 413q0 46-16.5 91T806 604.5q-41 55.5-110 126T521 898l-41 37Z"/></svg>
                </div>
                <div style="display: flex; flex-direction: column; justify-content: center;">
                    <h1>CardioCare</h1>
                    <div class="nav-logo-sub">Sistem Deteksi Risiko Jantung Cerdas</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    current = st.session_state.current_page

    # Navigasi disesuaikan dengan icon asli (Material Symbols)
    nav_items = [
        ("home",     "Beranda",            "btn_home",     col_home, ":material/home:"),
        ("riwayat",  "Riwayat Pengecekan", "btn_riwayat",  col_dash, ":material/analytics:"),
        ("prediksi", "Analisis Penyakit Jantung",    "btn_prediksi", col_pred, ":material/monitor_heart:"),
        ("analisis", "Analisis Model",     "btn_analisis", col_anal, ":material/psychology:"),
        ("tentang",  "Tentang",            "btn_tentang",  col_team, ":material/info:"),
    ]

    for page_key, label, btn_key, col, icon in nav_items:
        with col:
            btn_type = "primary" if current == page_key else "secondary"
            if st.button(label, icon=icon, key=btn_key, type=btn_type, use_container_width=True):
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