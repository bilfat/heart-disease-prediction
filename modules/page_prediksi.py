import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import datetime
from modules.prediction_engine import predict_single, predict_all

def render():
    st.markdown("## 👤 Analisis Penyakit Jantung")

    col_metode, col_model = st.columns(2)

    with col_metode:
        metode = st.radio(
            "Cara Input Data:",
            ["Input Manual", "Upload CSV"],
            horizontal=True
        )

    with col_model:
        model_pilihan = st.selectbox(
            "Model yang Digunakan:",
            ["Semua Model (4 Sekaligus)", "KNN", "SVM", "Decision Tree", "Neural Network"]
        )

    st.divider()

    # ---- A. INPUT MANUAL ----
    # ---- A. INPUT MANUAL ----
    if metode == "Input Manual":
        if "manual_prediction_results" not in st.session_state:
            st.session_state.manual_prediction_results = None

        with st.expander("📖 Penjelasan Singkat Setiap Input (Klik untuk Buka)", expanded=False):
            st.markdown(
                """
                <div class="guide-box">
                    <div class="guide-title">🩺 Panduan Pengisian Data</div>
                    <table class="guide-table">
                        <tr><td>Usia</td><td>Umur pasien saat ini (dalam tahun).</td></tr>
                        <tr><td>Jenis Kelamin</td><td>Laki-laki atau Perempuan.</td></tr>
                        <tr><td>Tipe Nyeri Dada</td><td>Jenis rasa sakit di dada: bisa nyeri khas jantung, nyeri biasa, atau tidak ada gejala sama sekali.</td></tr>
                        <tr><td>Tekanan Darah</td><td>Angka tekanan darah saat sedang istirahat (biasanya diukur pakai alat tensi). Normal sekitar 120.</td></tr>
                        <tr><td>Kolesterol</td><td>Kadar lemak dalam darah. Semakin tinggi, semakin berisiko. Idealnya di bawah 200.</td></tr>
                        <tr><td>Gula Darah Puasa</td><td>Apakah gula darah saat puasa tinggi (di atas 120)? Ini bisa menandakan risiko diabetes.</td></tr>
                        <tr><td>Hasil Rekam Jantung</td><td>Hasil pemeriksaan listrik jantung (EKG): Normal, Ada kelainan ringan, atau Ada pembesaran jantung.</td></tr>
                        <tr><td>Detak Jantung Maks</td><td>Detak jantung paling cepat yang pernah dicapai saat olahraga / tes fisik.</td></tr>
                        <tr><td>Nyeri Saat Olahraga</td><td>Apakah dada terasa sakit saat berolahraga atau beraktivitas berat?</td></tr>
                        <tr><td>Oldpeak</td><td>Seberapa besar perubahan aktivitas listrik jantung setelah olahraga. Makin tinggi = makin lelah jantungnya.</td></tr>
                        <tr><td>Kemiringan ST</td><td>Pola grafik jantung saat olahraga: naik (bagus), datar (waspada), atau turun (perlu perhatian).</td></tr>
                        <tr><td>Pembuluh Darah</td><td>Berapa banyak pembuluh darah besar di jantung yang tersumbat (0 = tidak ada, 4 = banyak).</td></tr>
                        <tr><td>Thalassemia</td><td>Kondisi kelainan darah: Normal, Cacat permanen, Cacat sementara (bisa pulih), atau Parah.</td></tr>
                    </table>
                </div>
                """,
                unsafe_allow_html=True
            )

        left_col, right_col = st.columns([1, 1])

        with left_col:
            with st.container(border=True):
                st.markdown(
                    """
                    <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.2rem;">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 96 960 960" width="24" fill="#0d7377"><path d="M480 576q-75 0-127.5-52.5T300 396q0-75 52.5-127.5T480 216q75 0 127.5 52.5T660 396q0 75-52.5 127.5T480 576Zm0-80q42 0 71-29t29-71q0-42-29-71t-71-29q-42 0-71 29t-29 71q0 42 29 71t71 29Zm0 368q-142 0-252.5-74T80 600q0-29 11.5-56t31.5-49.5q20-22.5 49-36.5t63-14q47 18 97.5 27t102.5 9q52 0 102.5-9t97.5-27q34 0 63 14t49 36.5q20 22.5 31.5 49.5T880 600q-35 116-145.5 190T480 864Zm0-80q105 0 188.5-51T794 600q-21-41-69.5-62.5T480 516q-95 0-143.5 21.5T267 600q30 82 113.5 133T480 784Z"/></svg>
                        <h3 style="margin: 0 !important; color: #1e293b;">Data Klinis Pasien</h3>
                    </div>
                    <p style="margin: 0 0 1.2rem 0; font-size: 0.78rem !important; color: #64748b;">
                        Silakan lengkapi formulir parameter medis di bawah ini.
                    </p>
                    """,
                    unsafe_allow_html=True
                )

                col1, col2 = st.columns(2)

                with col1:
                    usia = st.number_input(
                        "Usia",
                        min_value=1, max_value=120, value=45,
                        help="Umur pasien saat ini"
                    )

                    jenis_kelamin = st.selectbox(
                        "Jenis Kelamin",
                        [0, 1],
                        format_func=lambda x: "Perempuan" if x == 0 else "Laki-laki",
                        index=1,
                        help="Pilih jenis kelamin pasien"
                    )

                    nyeri_dada = st.selectbox(
                        "Tipe Nyeri Dada",
                        [0, 1, 2, 3],
                        format_func=lambda x: {
                            0: "Nyeri khas jantung (Tipe 0)",
                            1: "Nyeri tidak khas (Tipe 1)",
                            2: "Nyeri bukan jantung (Tipe 2)",
                            3: "Tidak ada gejala (Tipe 3)"
                        }[x],
                        help="Jenis rasa sakit yang dirasakan di dada"
                    )

                    tekanan_darah = st.number_input(
                        "Tekanan Darah Saat Istirahat",
                        min_value=50, max_value=250, value=120,
                        help="Angka tensi atas saat istirahat (normal ~120)"
                    )

                    kolesterol = st.number_input(
                        "Kolesterol",
                        min_value=100, max_value=600, value=220,
                        help="Kadar lemak dalam darah (idealnya <200)"
                    )

                    gula_darah = st.selectbox(
                        "Gula Darah Puasa > 120?",
                        [0, 1],
                        format_func=lambda x: "Tidak" if x == 0 else "Ya",
                        index=0,
                        help="Apakah gula darah saat puasa di atas 120 mg/dl?"
                    )

                    hasil_ecg = st.selectbox(
                        "Hasil Rekam Jantung (EKG)",
                        [0, 1, 2],
                        format_func=lambda x: {
                            0: "Normal (Tipe 0)",
                            1: "Ada kelainan ringan (Tipe 1)",
                            2: "Pembesaran jantung (Tipe 2)"
                        }[x],
                        help="Hasil pemeriksaan listrik jantung"
                    )

                with col2:
                    detak_jantung = st.number_input(
                        "Detak Jantung Maksimum",
                        min_value=50, max_value=250, value=150,
                        help="Detak jantung tercepat saat olahraga"
                    )

                    angina = st.selectbox(
                        "Nyeri Dada Saat Olahraga?",
                        [0, 1],
                        format_func=lambda x: "Tidak" if x == 0 else "Ya",
                        help="Apakah muncul rasa sakit di dada saat olahraga?"
                    )

                    oldpeak = st.number_input(
                        "Oldpeak",
                        min_value=0.0, max_value=10.0, value=1.5, step=0.1,
                        help="Perubahan grafik jantung setelah olahraga (0 = normal)"
                    )

                    slope = st.selectbox(
                        "Pola Grafik Jantung (Slope)",
                        [0, 1, 2],
                        format_func=lambda x: {
                            0: "Naik / bagus (Tipe 0)",
                            1: "Datar / waspada (Tipe 1)",
                            2: "Turun / perlu perhatian (Tipe 2)"
                        }[x],
                        index=1,
                        help="Bentuk grafik jantung saat olahraga berat"
                    )

                    ca = st.selectbox(
                        "Pembuluh Darah Tersumbat",
                        [0, 1, 2, 3, 4],
                        help="Jumlah pembuluh darah besar yang tersumbat (0 = tidak ada)"
                    )

                    thal = st.selectbox(
                        "Kondisi Thalassemia",
                        [0, 1, 2, 3],
                        format_func=lambda x: {
                            0: "Normal (Tipe 0)",
                            1: "Cacat permanen (Tipe 1)",
                            2: "Cacat sementara (Tipe 2)",
                            3: "Parah (Tipe 3)"
                        }[x],
                        index=2,
                        help="Kondisi kelainan pada sel darah merah"
                    )

                st.divider()
                btn_prediksi = st.button("Jalankan Komputasi Risiko", type="primary", use_container_width=True, key="run_computation")

        with right_col:
            if btn_prediksi:
                patient_data = pd.DataFrame([[
                    usia, jenis_kelamin, nyeri_dada, tekanan_darah, kolesterol,
                    gula_darah, hasil_ecg, detak_jantung, angina, oldpeak,
                    slope, ca, thal
                ]], columns=[
                    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
                ])
                st.session_state.manual_prediction_results = {
                    "patient_data": patient_data,
                    "model_pilihan": model_pilihan,
                    "usia": usia,
                    "jenis_kelamin": jenis_kelamin,
                    "kolesterol": kolesterol
                }

            with st.container(border=True):
                st.markdown(
                    """
                    <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.8rem;">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 96 960 960" width="24" fill="#0d7377"><path d="M200 936q-33 0-56.5-23.5T120 856V296q0-33 23.5-56.5T200 216h560q33 0 56.5 23.5T840 296v560q0 33-23.5 23.5T760 936H200Zm0-80h560V376H200v480Zm280-80q83 0 141.5-58.5T680 576q0-83-58.5-141.5T480 376q-83 0-141.5 58.5T280 576q0 83 58.5 141.5T480 776Z"/></svg>
                        <h3 style="margin: 0 !important; color: #1e293b;">Status & Hasil Prediksi</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                results_state = st.session_state.manual_prediction_results

                if results_state is None:
                    st.markdown(
                        """
                        <div class="result-placeholder-card">
                            <div class="heart-pulse-icon">
                                <svg xmlns="http://www.w3.org/2000/svg" height="80" viewBox="0 96 960 960" width="80" fill="#dc2626">
                                    <path d="m480 935-41-37q-106-97-175-167.5t-110-126Q113 549 96.5 504T80 413q0-90 60.5-150.5T290 202q57 0 105.5 27t84.5 78q42-54 89-79.5T670 202q89 0 149.5 60.5T880 413q0 46-16.5 91T806 604.5q-41 55.5-110 126T521 898l-41 37Z"/>
                                </svg>
                            </div>
                            <h2>Siap Memproses Data</h2>
                            <p>Silakan lengkapi formulir klinis di panel kiri. Sistem cerdas akan mengoordinasikan kluster data secara simultan.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    p_data = results_state["patient_data"]
                    m_pilihan = results_state["model_pilihan"]
                    u_age = results_state["usia"]
                    u_sex = results_state["jenis_kelamin"]
                    u_chol = results_state["kolesterol"]

                    st.markdown("<div style='min-height: 440px;'>", unsafe_allow_html=True)
                    if m_pilihan == "Semua Model (4 Sekaligus)":
                        results = predict_all(p_data)
                        row1 = st.columns(2)
                        row2 = st.columns(2)
                        grid_cols = [row1[0], row1[1], row2[0], row2[1]]

                        all_preds = {}
                        for idx, (name, res) in enumerate(results.items()):
                            with grid_cols[idx]:
                                if res["status"] == "success":
                                    pred = res["prediction"][0]
                                    all_preds[name] = "Terindikasi Penyakit Jantung" if pred == 1 else "Sehat dari Penyakit Jantung"

                                    if pred == 1:
                                        st.markdown(
                                            f"""
                                            <div class="result-positive" style="text-align:center; min-height:120px; display:flex; flex-direction:column; justify-content:center; margin-bottom: 0.6rem;">
                                                <h4 style="margin:0; font-size:0.85rem !important;">{name}</h4>
                                                <p style="font-size:1.5rem !important; margin:0.2rem 0;">⚠️</p>
                                                <p style="font-weight:700; margin:0; font-size:0.75rem !important;">Terindikasi</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )
                                    else:
                                        st.markdown(
                                            f"""
                                            <div class="result-negative" style="text-align:center; min-height:120px; display:flex; flex-direction:column; justify-content:center; margin-bottom: 0.6rem;">
                                                <h4 style="margin:0; font-size:0.85rem !important;">{name}</h4>
                                                <p style="font-size:1.5rem !important; margin:0.2rem 0;">✅</p>
                                                <p style="font-weight:700; margin:0; font-size:0.75rem !important;">Sehat</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )
                                else:
                                    st.error(f"{name} Error")
                                    all_preds[name] = "Error"

                        indicated_count = sum(1 for p in all_preds.values() if p == "Terindikasi Penyakit Jantung")
                        st.markdown("<br>", unsafe_allow_html=True)
                        if indicated_count >= 2:
                            st.error(
                                f"⚠️ **{indicated_count} dari 4 model** mendeteksi risiko penyakit jantung. "
                                "Disarankan segera berkonsultasi ke dokter."
                            )
                        else:
                            st.success(
                                "✅ Mayoritas model menunjukkan **tidak ada indikasi** penyakit jantung."
                            )

                        if btn_prediksi:
                            st.session_state.history.append({
                                "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "metode": "Manual",
                                "data_pasien": f"Usia: {u_age}, JK: {'L' if u_sex==1 else 'P'}, Kolesterol: {u_chol}",
                                "model": "Semua Model",
                                "hasil": f"KNN: {all_preds.get('KNN')}, SVM: {all_preds.get('SVM')}, DT: {all_preds.get('Decision Tree')}, NN: {all_preds.get('Neural Network')}"
                            })

                    else:
                        try:
                            preds, probs = predict_single(m_pilihan, p_data)
                            pred = preds[0]
                            hasil_text = "Terindikasi Penyakit Jantung" if pred == 1 else "Sehat dari Penyakit Jantung"

                            if pred == 1:
                                st.markdown(
                                    f"""
                                    <div class="result-positive" style="min-height: 180px; display: flex; flex-direction: column; justify-content: center; padding: 1.5rem; text-align: center;">
                                        <h3 style="margin-top:0;">⚠️ Terindikasi Penyakit Jantung</h3>
                                        <h4 style="margin: 0.3rem 0; font-weight:700;">Model: {m_pilihan}</h4>
                                        <p style="margin: 0.5rem 0 0 0; font-size: 0.82rem !important; line-height:1.6;">Model mendeteksi adanya risiko penyakit jantung pada data ini. Segera konsultasikan ke dokter untuk pemeriksaan lebih lanjut.</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            else:
                                st.markdown(
                                    f"""
                                    <div class="result-negative" style="min-height: 180px; display: flex; flex-direction: column; justify-content: center; padding: 1.5rem; text-align: center;">
                                        <h3 style="margin-top:0;">✅ Sehat dari Penyakit Jantung</h3>
                                        <h4 style="margin: 0.3rem 0; font-weight:700;">Model: {m_pilihan}</h4>
                                        <p style="margin: 0.5rem 0 0 0; font-size: 0.82rem !important; line-height:1.6;">Model tidak mendeteksi risiko penyakit jantung. Tetap jaga pola makan sehat dan olahraga teratur.</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                            if btn_prediksi:
                                st.session_state.history.append({
                                    "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "metode": "Manual",
                                    "data_pasien": f"Usia: {u_age}, JK: {'L' if u_sex==1 else 'P'}, Kolesterol: {u_chol}",
                                    "model": m_pilihan,
                                    "hasil": hasil_text
                                })
                        except Exception as e:
                            st.error(f"Terjadi kesalahan: {e}")

                    st.markdown("</div>", unsafe_allow_html=True)

                    if st.button("Reset / Input Baru", use_container_width=True, key="reset_prediction"):
                        st.session_state.manual_prediction_results = None
                        st.rerun()

    # ---- B. UPLOAD CSV ----
    else:
        with st.container(border=True):
            st.markdown("### 📁 Prediksi dari File CSV")

            template_file_path = "dataset/template_heart.csv"
            if os.path.exists(template_file_path):
                with open(template_file_path, "rb") as f:
                    template_data = f.read()
                st.download_button(
                    label="📥 Download Template CSV",
                    data=template_data,
                    file_name="template_pasien.csv",
                    mime="text/csv",
                    help="Gunakan template ini agar format data sesuai."
                )
            else:
                st.warning("File template tidak ditemukan.")

            st.divider()

            uploaded_file = st.file_uploader("Upload file CSV pasien:", type=["csv"])

            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.markdown("#### Preview Data")
                    st.dataframe(df.head(10), use_container_width=True)

                    required_cols = [
                        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
                    ]
                    missing_cols = [c for c in required_cols if c not in df.columns]

                    if missing_cols:
                        st.error(
                            f"Kolom tidak lengkap: {', '.join(missing_cols)}. "
                            "Silakan gunakan template CSV di atas."
                        )
                    else:
                        btn_csv = st.button("📊 Proses Prediksi", use_container_width=True)

                        if btn_csv:
                            features_df = df[required_cols].copy()

                            st.markdown("#### Hasil Prediksi")

                            if model_pilihan == "Semua Model (4 Sekaligus)":
                                results_all = predict_all(features_df)
                                for name, res in results_all.items():
                                    if res["status"] == "success":
                                        df[f"Hasil {name}"] = np.where(
                                            res["prediction"] == 1, "Terindikasi Penyakit Jantung", "Sehat dari Penyakit Jantung"
                                        )
                                st.success("Prediksi selesai untuk semua model!")
                                st.dataframe(df, use_container_width=True)

                                csv_out = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download Hasil",
                                    data=csv_out,
                                    file_name="hasil_prediksi_semua_model.csv",
                                    mime="text/csv"
                                )

                                st.session_state.history.append({
                                    "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "metode": "CSV",
                                    "data_pasien": f"Batch ({len(df)} data)",
                                    "model": "Semua Model",
                                    "hasil": f"{len(df)} data diproses."
                                })

                            else:
                                preds, _ = predict_single(model_pilihan, features_df)
                                df[f"Hasil ({model_pilihan})"] = np.where(
                                    preds == 1, "Terindikasi Penyakit Jantung", "Sehat dari Penyakit Jantung"
                                )
                                st.success(f"Prediksi selesai ({model_pilihan})!")
                                st.dataframe(df, use_container_width=True)

                                csv_out = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download Hasil",
                                    data=csv_out,
                                    file_name=f"hasil_{model_pilihan.lower().replace(' ','_')}.csv",
                                    mime="text/csv"
                                )

                                st.session_state.history.append({
                                    "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "metode": "CSV",
                                    "data_pasien": f"Batch ({len(df)} data)",
                                    "model": model_pilihan,
                                    "hasil": f"{len(df)} data diproses."
                                })

                except Exception as e:
                    st.error(f"Gagal membaca file: {e}")
