# pyrefly: ignore [missing-import]
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pyrefly: ignore [missing-import]
import streamlit as st

def render():
    st.markdown(
        """
        <div class="hero">
            <h1>❤️ Selamat Datang di CardioCare</h1>
            <p>Portal prediksi risiko penyakit jantung berbasis kecerdasan buatan — cepat, akurat, dan mudah digunakan.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">
            <h3>💡 Apa Itu CardioCare?</h3>
            <p>CardioCare membantu Anda memeriksa kemungkinan risiko penyakit jantung berdasarkan data kesehatan. 
            Sistem ini menggunakan 4 model kecerdasan buatan sekaligus: 
            <strong>KNN, SVM, Decision Tree, dan Neural Network</strong> — sehingga hasilnya lebih bisa dipercaya.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 📝 Input Data Manual")
            st.write(
                "Masukkan data kesehatan satu per satu. Setiap kolom sudah dilengkapi penjelasan "
                "singkat agar Anda paham apa yang harus diisi."
            )
            if st.button("Mulai Input Manual", use_container_width=True, key="home_manual"):
                st.session_state.current_page = "prediksi"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 📁 Upload File CSV")
            st.write(
                "Punya banyak data pasien sekaligus? Upload file CSV dan dapatkan hasil prediksi "
                "untuk semua data dalam hitungan detik."
            )
            if st.button("Upload File CSV", use_container_width=True, key="home_csv"):
                st.session_state.current_page = "prediksi"
                st.rerun()
