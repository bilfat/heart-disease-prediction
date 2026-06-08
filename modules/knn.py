import streamlit as st
import pandas as pd
import joblib
import numpy as np


def show():

    st.title("❤️ Prediksi Penyakit Jantung - KNN")

    try:

        model = joblib.load(
            "models/knn/knn_model.pkl"
        )

        scaler = joblib.load(
            "models/knn/scaler.pkl"
        )

        st.success("✅ Model KNN berhasil dimuat")

    except Exception as e:

        st.error(
            f"Gagal memuat model: {e}"
        )

        return

    metode = st.radio(
        "Pilih Metode Input",
        [
            "Input Manual",
            "Upload CSV"
        ]
    )

    # ====================================
    # INPUT MANUAL
    # ====================================

    if metode == "Input Manual":

        st.subheader("📝 Input Data Pasien")

        col1, col2 = st.columns(2)

        with col1:

            usia = st.number_input(
                "Usia",
                min_value=1,
                max_value=120,
                value=30
            )

            jenis_kelamin = st.selectbox(
                "Jenis Kelamin",
                [0, 1],
                format_func=lambda x:
                "Perempuan" if x == 0 else "Laki-laki"
            )

            nyeri_dada = st.number_input(
                "Tipe Nyeri Dada (CP)",
                min_value=0,
                max_value=3,
                value=0
            )

            tekanan_darah = st.number_input(
                "Tekanan Darah Istirahat",
                min_value=50,
                max_value=250,
                value=120
            )

            kolesterol = st.number_input(
                "Kolesterol",
                min_value=100,
                max_value=600,
                value=200
            )

            gula_darah = st.selectbox(
                "Gula Darah Saat Puasa > 120 mg/dl",
                [0, 1],
                format_func=lambda x:
                "Tidak" if x == 0 else "Ya"
            )

            hasil_ecg = st.number_input(
                "Hasil ECG",
                min_value=0,
                max_value=2,
                value=0
            )

        with col2:

            detak_jantung = st.number_input(
                "Detak Jantung Maksimum",
                min_value=50,
                max_value=250,
                value=150
            )

            angina = st.selectbox(
                "Angina Saat Olahraga",
                [0, 1],
                format_func=lambda x:
                "Tidak" if x == 0 else "Ya"
            )

            oldpeak = st.number_input(
                "Oldpeak",
                min_value=0.0,
                max_value=10.0,
                value=1.0
            )

            slope = st.number_input(
                "Slope",
                min_value=0,
                max_value=2,
                value=1
            )

            ca = st.number_input(
                "Jumlah Pembuluh Darah Utama (CA)",
                min_value=0,
                max_value=4,
                value=0
            )

            thal = st.number_input(
                "Thal",
                min_value=0,
                max_value=3,
                value=2
            )

        st.divider()

        st.info(
            "💡 Lengkapi seluruh data pasien untuk melakukan prediksi."
        )

        if st.button(
            "🔍 Prediksi Penyakit Jantung",
            use_container_width=True
        ):

            data = [[
                usia,
                jenis_kelamin,
                nyeri_dada,
                tekanan_darah,
                kolesterol,
                gula_darah,
                hasil_ecg,
                detak_jantung,
                angina,
                oldpeak,
                slope,
                ca,
                thal
            ]]

            data_scaled = scaler.transform(data)

            hasil = model.predict(data_scaled)

            st.divider()

            if hasil[0] == 1:

                st.error(
                    "❤️ Pasien Terindikasi Penyakit Jantung"
                )

            else:

                st.success(
                    "✅ Pasien Tidak Terindikasi Penyakit Jantung"
                )

    # ====================================
    # UPLOAD CSV
    # ====================================

    # ====================================
# UPLOAD CSV
# ====================================

    else:

        st.subheader("📁 Upload File CSV")

        st.info(
            """
            Upload file CSV dengan urutan kolom:

            age, sex, cp, trestbps, chol,
            fbs, restecg, thalach,
            exang, oldpeak, slope,
            ca, thal
            """
        )

        uploaded_file = st.file_uploader(
            "Upload File CSV",
            type=["csv"]
        )

        if uploaded_file is not None:

            df = pd.read_csv(
                uploaded_file
            )

            st.subheader(
                "Preview Data"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            if st.button(
                "📊 Prediksi dari File",
                use_container_width=True
            ):

                try:

                    data_scaled = scaler.transform(
                        df
                    )

                    hasil = model.predict(
                        data_scaled
                    )

                    df[
                        "Hasil Prediksi"
                    ] = np.where(
                        hasil == 1,
                        "Terindikasi",
                        "Tidak Terindikasi"
                    )

                    st.success(
                        "Prediksi berhasil dilakukan"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    csv = df.to_csv(
                        index=False
                    )

                    st.download_button(
                        label="📥 Download Hasil Prediksi",
                        data=csv,
                        file_name="hasil_prediksi_knn.csv",
                        mime="text/csv"
                    )

                except Exception as e:

                    st.error(
                        f"Terjadi kesalahan: {e}"
                    )