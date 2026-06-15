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
    st.markdown("## 👤 Analisis Risiko Penyakit Jantung")

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
    if metode == "Input Manual":

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

        with st.container(border=True):
            st.markdown("### 📝 Formulir Data Pasien")

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

            btn_prediksi = st.button("🔍 Jalankan Prediksi", use_container_width=True)

        if btn_prediksi:
            patient_data = pd.DataFrame([[
                usia, jenis_kelamin, nyeri_dada, tekanan_darah, kolesterol,
                gula_darah, hasil_ecg, detak_jantung, angina, oldpeak,
                slope, ca, thal
            ]], columns=[
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
            ])

            with st.container(border=True):
                st.markdown("### 📊 Hasil Prediksi")

                if model_pilihan == "Semua Model (4 Sekaligus)":
                    results = predict_all(patient_data)
                    r_cols = st.columns(4)

                    all_preds = {}
                    for idx, (name, res) in enumerate(results.items()):
                        with r_cols[idx]:
                            if res["status"] == "success":
                                pred = res["prediction"][0]
                                all_preds[name] = "Terindikasi" if pred == 1 else "Tidak Terindikasi"

                                if pred == 1:
                                    st.markdown(
                                        f"""
                                        <div class="result-positive" style="text-align:center; min-height:160px; display:flex; flex-direction:column; justify-content:center;">
                                            <h4 style="margin:0;">{name}</h4>
                                            <p style="font-size:2rem !important; margin:0.3rem 0;">⚠️</p>
                                            <p style="font-weight:700; margin:0;">Terindikasi</p>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                                else:
                                    st.markdown(
                                        f"""
                                        <div class="result-negative" style="text-align:center; min-height:160px; display:flex; flex-direction:column; justify-content:center;">
                                            <h4 style="margin:0;">{name}</h4>
                                            <p style="font-size:2rem !important; margin:0.3rem 0;">✅</p>
                                            <p style="font-weight:700; margin:0;">Aman</p>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                            else:
                                st.error(f"{name}: {res['error']}")
                                all_preds[name] = "Error"

                    indicated_count = sum(1 for p in all_preds.values() if p == "Terindikasi")
                    st.markdown("<br>", unsafe_allow_html=True)
                    if indicated_count >= 2:
                        st.error(
                            f"⚠️ **{indicated_count} dari 4 model** mendeteksi risiko penyakit jantung. "
                            "Disarankan untuk segera berkonsultasi ke dokter."
                        )
                    else:
                        st.success(
                            "✅ Mayoritas model menunjukkan **tidak ada indikasi** penyakit jantung. "
                            "Tetap jaga pola hidup sehat ya!"
                        )

                    st.session_state.history.append({
                        "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "metode": "Manual",
                        "data_pasien": f"Usia: {usia}, JK: {'L' if jenis_kelamin==1 else 'P'}, Kolesterol: {kolesterol}",
                        "model": "Semua Model",
                        "hasil": f"KNN: {all_preds.get('KNN')}, SVM: {all_preds.get('SVM')}, DT: {all_preds.get('Decision Tree')}, NN: {all_preds.get('Neural Network')}"
                    })

                else:
                    try:
                        preds, probs = predict_single(model_pilihan, patient_data)
                        pred = preds[0]
                        hasil_text = "Terindikasi" if pred == 1 else "Tidak Terindikasi"

                        if pred == 1:
                            st.markdown(
                                f"""
                                <div class="result-positive">
                                    <h3>⚠️ Terindikasi Penyakit Jantung — {model_pilihan}</h3>
                                    <p>Model <strong>{model_pilihan}</strong> mendeteksi adanya risiko penyakit jantung pada data ini. Segera konsultasikan ke dokter untuk pemeriksaan lebih lanjut.</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                f"""
                                <div class="result-negative">
                                    <h3>✅ Tidak Terindikasi — {model_pilihan}</h3>
                                    <p>Model <strong>{model_pilihan}</strong> tidak mendeteksi risiko penyakit jantung. Tetap jaga pola makan sehat dan olahraga teratur.</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        st.session_state.history.append({
                            "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "metode": "Manual",
                            "data_pasien": f"Usia: {usia}, JK: {'L' if jenis_kelamin==1 else 'P'}, Kolesterol: {kolesterol}",
                            "model": model_pilihan,
                            "hasil": hasil_text
                        })
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")

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
                                            res["prediction"] == 1, "Terindikasi", "Aman"
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
                                    preds == 1, "Terindikasi", "Aman"
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
