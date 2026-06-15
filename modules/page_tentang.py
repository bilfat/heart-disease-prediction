import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pyrefly: ignore [missing-import]
import streamlit as st

def render():
    st.markdown("## ℹ️ Tentang CardioCare")

    col_info, col_sys = st.columns([1.5, 1])

    with col_info:
        st.markdown(
            """
            <div class="card">
                <h3>📚 Dataset yang Digunakan</h3>
                <p>Kami menggunakan dataset <strong>Cleveland Heart Disease</strong> dari UCI Machine Learning Repository. 
                Dataset ini berisi 303 data pasien dengan 13 parameter kesehatan dan 1 label 
                (ada/tidak ada penyakit jantung). Dataset ini sudah digunakan secara luas 
                di dunia penelitian kesehatan dan machine learning.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_sys:
        st.markdown(
            """
            <div class="card">
                <h3>🔬 Teknologi yang Dipakai</h3>
                <p>Dibangun dengan <strong>Streamlit</strong> (Python), model dilatih menggunakan <strong>Scikit-Learn</strong>, 
                dan disimpan dalam format <strong>Joblib</strong>. Setiap model memiliki scaler tersendiri 
                agar perbandingan antar model tetap adil.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 👥 Tim Pengembang")

    cols_team = st.columns(4)

    team_members = [
        {"nama": "Nabil",   "role": "Lead ML Engineer",       "inisial": "NB"},
        {"nama": "Karomah", "role": "Data Scientist",          "inisial": "KR"},
        {"nama": "Eci",     "role": "UI/UX Designer",          "inisial": "EC"},
        {"nama": "Fatya",   "role": "Backend Developer & QA",  "inisial": "FT"}
    ]

    for idx, member in enumerate(team_members):
        with cols_team[idx]:
            st.markdown(
                f"""
                <div class="team-card">
                    <div class="team-avatar">{member['inisial']}</div>
                    <div class="team-name">{member['nama']}</div>
                    <div class="team-role">{member['role']}</div>
                    <div class="team-sub">CardioCare Team</div>
                </div>
                """,
                unsafe_allow_html=True
            )
