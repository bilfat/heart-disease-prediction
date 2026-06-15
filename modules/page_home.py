# pyrefly: ignore [missing-import]
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pyrefly: ignore [missing-import]
import streamlit as st

def render():
    # ====================================
    # 1. HERO BANNER
    # ====================================
    st.markdown(
        """
        <div class="hero">
            <h1>Selamat Datang di CardioCare</h1>
            <p>Portal prediksi risiko penyakit jantung berbasis kecerdasan buatan — cepat, akurat, dan mudah digunakan.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ====================================
    # 2. KPI METRIC CARDS
    # ====================================
    st.markdown(
        """
        <div class="kpi-row">
            <div class="kpi-card">
                <div class="kpi-icon" style="background: linear-gradient(135deg, #3b82f6, #6366f1);">
                    <svg xmlns="http://www.w3.org/2000/svg" height="22" viewBox="0 96 960 960" width="22" fill="white"><path d="M160 896V256h640v640H160Zm80-80h480V336H240v480Zm40-60h120V476H280v280Zm160 0h120V396h-120v360Zm160 0h120V536H600v220Z"/></svg>
                </div>
                <div class="kpi-value">1,025 Pasien</div>
                <div class="kpi-label">Total Dataset</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon" style="background: linear-gradient(135deg, #10b981, #14b8a6);">
                    <svg xmlns="http://www.w3.org/2000/svg" height="22" viewBox="0 96 960 960" width="22" fill="white"><path d="M120 936V216h720v720H120Zm80-80h560V376H200v480Zm100-60q-17 0-28.5-11.5T260 756V556q0-17 11.5-28.5T300 516q17 0 28.5 11.5T340 556v200q0 17-11.5 28.5T300 796Zm180 0q-17 0-28.5-11.5T440 756V436q0-17 11.5-28.5T480 396q17 0 28.5 11.5T520 436v320q0 17-11.5 28.5T480 796Zm180 0q-17 0-28.5-11.5T620 756V596q0-17 11.5-28.5T660 556q17 0 28.5 11.5T700 596v160q0 17-11.5 28.5T660 796Z"/></svg>
                </div>
                <div class="kpi-value">14 Parameter</div>
                <div class="kpi-label">Jumlah Fitur Kesehatan</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon" style="background: linear-gradient(135deg, #f59e0b, #f97316);">
                    <svg xmlns="http://www.w3.org/2000/svg" height="22" viewBox="0 96 960 960" width="22" fill="white"><path d="M320 816q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47Zm320 0q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47Zm-320-80q33 0 56.5-23.5T400 656q0-33-23.5-56.5T320 576q-33 0-56.5 23.5T240 656q0 33 23.5 56.5T320 736Zm320 0q33 0 56.5-23.5T720 656q0-33-23.5-56.5T640 576q-33 0-56.5 23.5T560 656q0 33 23.5 56.5T640 736Z"/></svg>
                </div>
                <div class="kpi-value">4 Model AI</div>
                <div class="kpi-label">Model (KNN, SVM, DT, NN)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon" style="background: linear-gradient(135deg, #ef4444, #ec4899);">
                    <svg xmlns="http://www.w3.org/2000/svg" height="22" viewBox="0 96 960 960" width="22" fill="white"><path d="m344 956-76-128-144-32 14-148-98-112 98-112-14-148 144-32 76-128 136 58 136-58 76 128 144 32-14 148 98 112-98 112 14 148-144 32-76 128-136-58-136 58Zm94-278 226-226-56-58-170 170-86-84-56 56 142 142Z"/></svg>
                </div>
                <div class="kpi-value">86.0%</div>
                <div class="kpi-label">Akurasi Tertinggi (KNN)</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ====================================
    # 3. APA ITU CARDIOCARE
    # ====================================
    with st.container(border=True):
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.8rem;">
                <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 96 960 960" width="24" fill="#0d7377"><path d="M480 976q-83 0-156-31.5T197 859q-54-54-85.5-127T80 576q0-83 31.5-156T197 293q54-54 127-85.5T480 176q83 0 156 31.5T763 293q54 54 85.5 127T880 576q0 83-31.5 156T763 859q-54 54-127 85.5T480 976Zm-40-82v-78q-33 0-56.5-23.5T360 736v-40L168 504q-3 18-5.5 36t-2.5 36q0 121 79.5 212T440 894Zm276-102q26-36 43-78t23-86H642l74 164Zm-356 0 120-268H360L240 684q28 40 64.5 70.5T360 792Zm120-340h120l-60-136-60 136Z"/></svg>
                <h3 style="margin: 0 !important; color: #1e293b;">Apa Itu CardioCare?</h3>
            </div>
            <p style="margin: 0; line-height: 1.75; color: var(--text-secondary);">
                CardioCare adalah sistem prediksi risiko penyakit jantung berbasis <strong>Machine Learning</strong> 
                yang menganalisis data klinis pasien menggunakan empat algoritma klasifikasi sekaligus:
                <strong>K-Nearest Neighbors (KNN)</strong>, <strong>Support Vector Machine (SVM)</strong>, 
                <strong>Decision Tree</strong>, dan <strong>Neural Network</strong>. 
                Dengan pendekatan <em>multi-model ensemble</em>, hasil diagnosis menjadi lebih akurat dan objektif.
            </p>
            """,
            unsafe_allow_html=True
        )

    # ====================================
    # 4. RINGKASAN DATASET & INFORMASI WEB
    # ====================================
    with st.container(border=True):
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.8rem;">
                <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 96 960 960" width="24" fill="#0d7377"><path d="M480 616q-117 0-198.5-25.5T200 536v-80q0-29 81.5-54.5T480 376q117 0 198.5 25.5T760 456v80q0 29-81.5 54.5T480 616Zm0 200q-117 0-198.5-25.5T200 736v-80q38 28 112 46t168 18q94 0 168-18t112-46v80q0 29-81.5 54.5T480 816Zm0 200q-117 0-198.5-25.5T200 936v-80q38 28 112 46t168 18q94 0 168-18t112-46v80q0 29-81.5 54.5T480 1016Z"/></svg>
                <h3 style="margin: 0 !important; color: #1e293b;">Ringkasan Dataset & Informasi Web</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        col_data1, col_data2 = st.columns(2)
        with col_data1:
            st.markdown(
                """
                <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.2rem; height: 100%;">
                    <div style="font-weight: 700; color: #0d7377; font-size: 0.88rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
                        <span>📂</span> Sumber Dataset
                    </div>
                    <p style="margin: 0; font-size: 0.82rem; line-height: 1.65; color: var(--text-secondary);">
                        Menggunakan dataset sekunder (seperti <strong>Cleveland Heart Disease dataset</strong> dari <strong>UCI Machine Learning Repository</strong>) 
                        yang telah divalidasi oleh para ahli medis dan berisi total <strong>1,025 data pasien</strong>.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_data2:
            st.markdown(
                """
                <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.2rem; height: 100%;">
                    <div style="font-weight: 700; color: #0d7377; font-size: 0.88rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
                        <span>🔑</span> Atribut Kunci (Fitur Kesehatan)
                    </div>
                    <p style="margin: 0; font-size: 0.82rem; line-height: 1.65; color: var(--text-secondary);">
                        Sistem mendeteksi parameter medis penting seperti <strong>Usia</strong>, <strong>Jenis Kelamin</strong>, 
                        <strong>Tekanan Darah (trestbps)</strong>, <strong>Kolesterol (chol)</strong>, <strong>Detak Jantung Maksimum (thalach)</strong>, 
                        dan indikator klinis lainnya untuk menghasilkan analisis risiko yang komprehensif.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ====================================
    # 5. QUICK ACTION — INPUT DATA
    # ====================================
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 0.6rem; margin: 1.2rem 0 1rem 0;">
            <svg xmlns="http://www.w3.org/2000/svg" height="22" viewBox="0 96 960 960" width="22" fill="#0d7377"><path d="M200 936q-33 0-56.5-23.5T120 856V296q0-33 23.5-56.5T200 216h560q33 0 56.5 23.5T840 296v560q0 33-23.5 23.5T760 936H200Zm0-80h560V376H200v480Zm280-80q83 0 141.5-58.5T680 576q0-83-58.5-141.5T480 376q-83 0-141.5 58.5T280 576q0 83 58.5 141.5T480 776Z"/></svg>
            <h3 style="margin: 0 !important; color: #1e293b;">Mulai Analisis Sekarang</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem;">
                    <svg xmlns="http://www.w3.org/2000/svg" height="20" viewBox="0 96 960 960" width="20" fill="#3b82f6"><path d="M200 856V296q0-33 23.5-56.5T280 216h400q33 0 56.5 23.5T760 296v560q0 33-23.5 56.5T680 936H280q-33 0-56.5-23.5T200 856Zm80 0h400V296H280v560Zm40-80h200v-80H320v80Zm0-120h320v-80H320v80Zm0-120h320v-80H320v80Z"/></svg>
                    <span style="font-weight: 700; font-size: 1rem; color: #1e293b;">Input Data Manual</span>
                </div>
                <p style="margin: 0; font-size: 0.84rem; line-height: 1.65; color: #475569;">
                    Masukkan data kesehatan satu per satu. Setiap kolom sudah dilengkapi penjelasan 
                    singkat agar Anda paham apa yang harus diisi.
                </p>
                """,
                unsafe_allow_html=True
            )
            if st.button("Mulai Input Manual", icon=":material/edit_note:", use_container_width=True, key="home_manual"):
                st.session_state.current_page = "prediksi"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem;">
                    <svg xmlns="http://www.w3.org/2000/svg" height="20" viewBox="0 96 960 960" width="20" fill="#10b981"><path d="M440 656V376q0-17 11.5-28.5T480 336q17 0 28.5 11.5T520 376v280q0 17-11.5 28.5T480 696q-17 0-28.5-11.5T440 656Zm40 240q-17 0-28.5-11.5T440 856v-40q0-17 11.5-28.5T480 776q17 0 28.5 11.5T520 816v40q0 17-11.5 28.5T480 896ZM200 936q-33 0-56.5-23.5T120 856V296q0-33 23.5-56.5T200 216h560q33 0 56.5 23.5T840 296v560q0 33-23.5 56.5T760 936H200Z"/></svg>
                    <span style="font-weight: 700; font-size: 1rem; color: #1e293b;">Upload File CSV</span>
                </div>
                <p style="margin: 0; font-size: 0.84rem; line-height: 1.65; color: #475569;">
                    Punya banyak data pasien sekaligus? Upload file CSV dan dapatkan hasil prediksi 
                    untuk semua data dalam hitungan detik.
                </p>
                """,
                unsafe_allow_html=True
            )
            if st.button("Upload File CSV", icon=":material/upload_file:", use_container_width=True, key="home_csv"):
                st.session_state.current_page = "prediksi"
                st.rerun()
