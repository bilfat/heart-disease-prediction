import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
import altair as alt

def render():
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.5rem;">
            <span style="font-size: 1.8rem;">📊</span>
            <h2 style="margin: 0 !important;">Dashboard Data & Eksplorasi Dataset</h2>
        </div>
        <p style="margin-top: 0; margin-bottom: 1.5rem; color: var(--text-secondary);">
            Visualisasi sebaran variabel klinis dari 1,025 sampel data latih awal penyakit jantung.
        </p>
        """,
        unsafe_allow_html=True
    )

    # ====================================
    # RIWAYAT PENGECEKAN SESI
    # ====================================
    with st.container(border=True):
        st.markdown(
            """
            <div style="font-weight: 700; color: #1e293b; font-size: 1.1rem; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <span>📋</span> Riwayat Pengecekan Sesi Aktif
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.write(
            "Daftar pemeriksaan risiko yang dilakukan selama sesi aktif ini. "
            "Data riwayat akan terhapus apabila tab browser di-refresh."
        )

        if st.session_state.history:
            history_df = pd.DataFrame(st.session_state.history)
            history_df.columns = ["Waktu", "Metode", "Data Pasien", "Model", "Hasil"]
            st.dataframe(history_df, use_container_width=True)

            col_clear, _ = st.columns([1, 4])
            with col_clear:
                if st.button("🗑️ Hapus Riwayat", use_container_width=True):
                    st.session_state.history = []
                    st.rerun()
        else:
            st.info("Belum ada riwayat pengecekan untuk sesi ini. Silakan jalankan prediksi terlebih dahulu.")
