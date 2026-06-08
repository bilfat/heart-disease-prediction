import streamlit as st

from modules.knn import show as show_knn
from modules.svm import show as show_svm
from modules.decision_tree import show as show_decision_tree
from modules.neural_network import show as show_neural_network

# ====================================
# KONFIGURASI HALAMAN
# ====================================

st.set_page_config(
    page_title="Prediksi Penyakit Jantung",
    page_icon="❤️",
    layout="wide"
)

# ====================================
# SIDEBAR
# ====================================

with st.sidebar:

    st.title("❤️ Heart Disease Prediction")

    st.markdown("---")

    selected_model = st.radio(
        "Pilih Model",
        [
            "KNN",
            "SVM",
            "Decision Tree",
            "Neural Network"
        ]
    )

# ====================================
# ROUTING MODEL
# ====================================

if selected_model == "KNN":
    show_knn()

elif selected_model == "SVM":
    show_svm()

elif selected_model == "Decision Tree":
    show_decision_tree()

elif selected_model == "Neural Network":
    show_neural_network()