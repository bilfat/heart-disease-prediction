import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
import altair as alt

def render():
    # Header halaman
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.5rem;">
            <span style="font-size: 1.8rem;">🤖</span>
            <h2 style="margin: 0 !important;">Analisis Optimasi Performa Model</h2>
        </div>
        <p style="margin-top: 0; margin-bottom: 1.5rem; color: var(--text-secondary);">
            Komparasi nilai akurasi algoritma sebelum dan sesudah penerapan Hyperparameter Tuning (HPO) berdasarkan data riset asli.
        </p>
        """,
        unsafe_allow_html=True
    )

    # ====================================
    # 1. EKSPLORASI DATASET
    # ====================================
    try:
        df = pd.read_csv('dataset/heart.csv')

        # Container Utama untuk Dashboard Data
        with st.container(border=True):
            st.markdown(
                """
                <div style="font-weight: 700; color: #1e293b; font-size: 1.1rem; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.2rem;">
                    <span style="font-size: 1.3rem;">🩺</span> Eksplorasi Karakteristik Dataset
                </div>
                """,
                unsafe_allow_html=True
            )

            # Baris 1: Tiga Kartu Informasi
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.markdown(
                    """
                    <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.2rem; background-color: #f8fafc; height: 100%; min-height: 120px;">
                        <div style="font-weight: 700; color: #1e293b; font-size: 0.88rem; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span style="color: #2563eb;">📅</span> Distribusi Umur
                        </div>
                        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
                            Mayoritas pasien terindikasi rentan berada pada kluster rentang usia di atas 50 tahun.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_stat2:
                st.markdown(
                    """
                    <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.2rem; background-color: #f8fafc; height: 100%; min-height: 120px;">
                        <div style="font-weight: 700; color: #1e293b; font-size: 0.88rem; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span style="color: #ef4444;">🩸</span> Tekanan Darah
                        </div>
                        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
                            Rata-rata resting blood pressure populasi terpusat pada rentang 120-140 mmHg.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_stat3:
                st.markdown(
                    """
                    <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.2rem; background-color: #f8fafc; height: 100%; min-height: 120px;">
                        <div style="font-weight: 700; color: #1e293b; font-size: 0.88rem; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span style="color: #10b981;">📈</span> Korelasi Utama
                        </div>
                        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
                            Parameter depresi ST (oldpeak) terbukti memiliki signifikansi tinggi terhadap hasil akhir target.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # Baris 2: Dua Grafik (Kolesterol & Target)
            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                with st.container(border=True):
                    st.markdown(
                        """
                        <div style="font-weight: 700; color: #1e293b; font-size: 0.95rem; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                            <span style="color: #2563eb;">📈</span> Distribusi Parameter Kolesterol Serum Pasien
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Binning kolesterol
                    bins = [0, 199, 239, 279, 319, float('inf')]
                    labels = ['<200', '200-239', '240-279', '280-319', '>320']
                    df_chol = df.copy()
                    df_chol['chol_bin'] = pd.cut(df_chol['chol'], bins=bins, labels=labels)
                    chol_counts = df_chol['chol_bin'].value_counts().reindex(labels).reset_index()
                    chol_counts.columns = ['Kolesterol', 'Jumlah']

                    # Line Chart
                    line = alt.Chart(chol_counts).mark_line(interpolate='monotone', color='#3b82f6', strokeWidth=3).encode(
                        x=alt.X('Kolesterol:N', sort=labels, title=None, axis=alt.Axis(labelAngle=0, labelFontSize=11, domain=False, ticks=False)),
                        y=alt.Y('Jumlah:Q', title=None, axis=alt.Axis(grid=True, gridColor='#f1f5f9', domain=False, ticks=False))
                    )
                    points = alt.Chart(chol_counts).mark_point(color='#3b82f6', size=60, fill='white', strokeWidth=2).encode(
                        x=alt.X('Kolesterol:N', sort=labels),
                        y=alt.Y('Jumlah:Q')
                    )
                    
                    st.altair_chart((line + points), use_container_width=True)

            with col_chart2:
                with st.container(border=True):
                    st.markdown(
                        """
                        <div style="font-weight: 700; color: #1e293b; font-size: 0.95rem; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                            <span style="color: #ef4444;">🔴</span> Proporsi Rasio Kelas Target Pasien
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    target_counts = df['target'].value_counts().reset_index()
                    target_counts.columns = ['Status', 'Jumlah']
                    target_counts['Status'] = target_counts['Status'].map({1: 'Risiko Tinggi', 0: 'Risiko Rendah'})

                    donut = alt.Chart(target_counts).mark_arc(innerRadius=60, outerRadius=95).encode(
                        theta=alt.Theta('Jumlah:Q'),
                        color=alt.Color('Status:N', scale=alt.Scale(
                            domain=['Risiko Tinggi', 'Risiko Rendah'],
                            range=['#e11d48', '#10b981']
                        ), legend=alt.Legend(
                            orient='bottom',
                            title=None,
                            direction='horizontal',
                            labelFontSize=11,
                            symbolType='square'
                        ))
                    ).properties(height=260)

                    st.altair_chart(donut, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal memuat visualisasi dataset: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ====================================
    # 2. Tabel Analisis
    # ====================================
    with st.container(border=True):
        # Insight Box
        st.markdown(
            """
            <div class="insight-box" style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-left: 5px solid #22c55e; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 1.5rem; display: flex; align-items: flex-start; gap: 0.8rem;">
                <span style="font-size: 1.5rem; line-height: 1;">🏅</span>
                <div>
                    <div style="font-weight: 700; color: #166534; font-size: 0.88rem; margin-bottom: 0.2rem;">Insight Optimasi (HPO)</div>
                    <div style="color: #166534; font-size: 0.85rem; line-height: 1.6;">
                        Penerapan Hyperparameter Tuning berhasil memberikan peningkatan akurasi paling signifikan pada model 
                        <strong>K-Nearest Neighbors (KNN) dengan lonjakan +6.0%</strong>, sementara model Support Vector Machine (SVM) 
                        tetap stabil dan Neural Network (NN) mengalami penurunan -2.0%.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # HPO Table
        st.markdown(
            """
            <table class="hpo-table">
                <thead>
                    <tr>
                        <th>Arsitektur Algoritma</th>
                        <th style="text-align:center;">Akurasi Sebelum HPO</th>
                        <th style="text-align:center;">Akurasi Sesudah HPO</th>
                        <th style="text-align:center;">Peningkatan (Delta)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>K-Nearest Neighbors (KNN)</strong></td>
                        <td style="text-align:center;">80.0%</td>
                        <td style="text-align:center;"><span class="badge-blue">86.0%</span></td>
                        <td style="text-align:center;"><span class="delta-up">↗ +6.0%</span></td>
                    </tr>
                    <tr>
                        <td><strong>Support Vector Machine (SVM)</strong></td>
                        <td style="text-align:center;">84.0%</td>
                        <td style="text-align:center;"><span class="badge-green">84.0%</span></td>
                        <td style="text-align:center;"><span class="delta-stable">= 0.0% (Stabil)</span></td>
                    </tr>
                    <tr>
                        <td><strong>Decision Tree Classifier</strong></td>
                        <td style="text-align:center;">75.0%</td>
                        <td style="text-align:center;"><span class="badge-blue">78.0%</span></td>
                        <td style="text-align:center;"><span class="delta-up">↗ +3.0%</span></td>
                    </tr>
                    <tr>
                        <td><strong>Neural Network (NN)</strong></td>
                        <td style="text-align:center;">78.0%</td>
                        <td style="text-align:center;"><span class="badge-red">76.0%</span></td>
                        <td style="text-align:center;"><span class="delta-down">↘ -2.0%</span></td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )

    # ====================================
    # 3. Card Grafik Perbandingan
    # ====================================
    with st.container(border=True):
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 1.2rem;">
                <span style="font-size: 1.3rem;">📊</span>
                <h3 style="margin: 0 !important;">Grafik Komparasi Efektivitas Hyperparameter Tuning</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Data untuk Altair
        data_list = [
            {"Algoritma": "KNN", "Tipe": "Sebelum HPO", "Akurasi": 80.0},
            {"Algoritma": "KNN", "Tipe": "Sesudah HPO", "Akurasi": 86.0},
            {"Algoritma": "SVM", "Tipe": "Sebelum HPO", "Akurasi": 84.0},
            {"Algoritma": "SVM", "Tipe": "Sesudah HPO", "Akurasi": 84.0},
            {"Algoritma": "Decision Tree", "Tipe": "Sebelum HPO", "Akurasi": 75.0},
            {"Algoritma": "Decision Tree", "Tipe": "Sesudah HPO", "Akurasi": 78.0},
            {"Algoritma": "Neural Network", "Tipe": "Sebelum HPO", "Akurasi": 78.0},
            {"Algoritma": "Neural Network", "Tipe": "Sesudah HPO", "Akurasi": 76.0},
        ]
        df_chart = pd.DataFrame(data_list)

        # Plot Altair Bar Chart
        chart = alt.Chart(df_chart).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X('Tipe:N', title=None, axis=alt.Axis(labels=False, ticks=False, domain=False)),
            y=alt.Y('Akurasi:Q', title=None, scale=alt.Scale(domain=[65, 100]), axis=alt.Axis(
                values=[65, 70, 75, 80, 85, 90, 95, 100],
                grid=True,
                gridColor='#f1f5f9',
                domain=False,
                ticks=False
            )),
            color=alt.Color('Tipe:N', scale=alt.Scale(
                domain=['Sebelum HPO', 'Sesudah HPO'],
                range=['#cbd5e1', '#3b82f6']
            ), legend=alt.Legend(
                orient='top',
                title=None,
                direction='horizontal',
                labelFontSize=12,
                symbolSize=100
            )),
            column=alt.Column('Algoritma:N', title=None, header=alt.Header(
                labelOrient='bottom',
                labelFontSize=12,
                labelPadding=12
            ))
        ).properties(
            width=alt.Step(35),
            height=280
        ).configure_view(
            stroke=None
        ).configure_facet(
            spacing=30
        )

        st.altair_chart(chart, use_container_width=False)
