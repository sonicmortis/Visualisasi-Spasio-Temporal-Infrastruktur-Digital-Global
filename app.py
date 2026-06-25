import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import joblib
import numpy as np

st.set_page_config(layout="wide", page_title="Visualisasi Spasio-Temporal Infrastruktur Digital")

st.title("🌍 Visualisasi Spasio-Temporal Infrastruktur Digital Global")
st.markdown("---")

@st.cache_data
def load_data():
    df_cluster = pd.read_csv("Dataset/merged_data_with_clusters.csv")
    df_forecast = pd.read_csv("Dataset/forecast_results_prophet.csv")
    return df_cluster, df_forecast

@st.cache_resource
def load_models():
    models = {}
    models['kmeans'] = joblib.load("forecasting_model/kmeans_model.pkl")
    models['scaler'] = joblib.load("forecasting_model/scaler.pkl")
    return models

df_cluster, df_forecast = load_data()
models = load_models()

df_cluster = df_cluster.dropna(subset=['cluster_label', 'Entity'])

fitur_labels = {
    'internet_usage': 'Penggunaan Internet (%)',
    'electricity_access': 'Akses Listrik (%)',
    'gdp_per_capita': 'GDP per Kapita (USD)'
}

cluster_colors = {
    'Digital Advanced': '#2ecc71',
    'Digital Developing': '#f39c12',
    'Digital Emerging': '#e74c3c'
}

st.sidebar.header("Kontrol Visualisasi")

fitur = st.sidebar.selectbox(
    "Pilih Fitur",
    options=['internet_usage', 'electricity_access', 'gdp_per_capita'],
    format_func=lambda x: fitur_labels[x]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Sumber Data:** Our World in Data\n"
    "**Periode:** 2000-2022\n"
)

df_year = df_cluster[df_cluster['Year'] == 2022].copy()

st.subheader("🎬 Animasi Perubahan Klaster dari Tahun ke Tahun")

df_animasi = df_cluster.copy()
df_animasi = df_animasi.dropna(subset=['cluster_label'])

fig_animasi = px.choropleth(
    df_animasi,
    locations="Code",
    color="cluster_label",
    hover_name="Entity",
    hover_data={
        'internet_usage': ':.2f',
        'electricity_access': ':.2f',
        'gdp_per_capita': ':.0f'
    },
    animation_frame="Year",
    color_discrete_map=cluster_colors,
    category_orders={"cluster_label": ["Digital Advanced", "Digital Developing", "Digital Emerging"]}
)

fig_animasi.update_layout(
    height=600,
    width=1200,
    legend_title_text="Klaster",
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    ),
    updatemenus=[
        {
            "type": "buttons",
            "buttons": [
                {
                    "label": "▶ Play",
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {"duration": 500, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 300}
                        }
                    ]
                },
                {
                    "label": "⏸ Pause",
                    "method": "animate",
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }
                    ]
                }
            ]
        }
    ],
    sliders=[
        {
            "steps": [
                {
                    "method": "animate",
                    "label": str(year),
                    "args": [
                        [str(year)],
                        {
                            "frame": {"duration": 300, "redraw": True},
                            "mode": "immediate",
                            "transition": {"duration": 300}
                        }
                    ]
                }
                for year in sorted(df_animasi['Year'].unique())
            ]
        }
    ]
)

st.plotly_chart(fig_animasi, use_container_width=True)

st.markdown("---")
st.subheader("📊 Analisis Tren dan Distribusi")

cluster_trend = df_cluster.groupby(['Year', 'cluster_label'])[fitur].mean().reset_index()

fig1 = px.line(
    cluster_trend,
    x='Year',
    y=fitur,
    color='cluster_label',
    color_discrete_map=cluster_colors,
    title=f'Tren Rata-rata {fitur_labels[fitur]} per Klaster (2000-2022)',
    labels={fitur: fitur_labels[fitur], 'cluster_label': 'Klaster'},
    category_orders={"cluster_label": ["Digital Advanced", "Digital Developing", "Digital Emerging"]}
)

fig1.update_layout(height=400, width=None)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

df_year_clean = df_year[df_year[fitur].notna()]
top10 = df_year_clean.nlargest(10, fitur)

fig2 = px.bar(
    top10,
    x='Entity',
    y=fitur,
    color='cluster_label',
    color_discrete_map=cluster_colors,
    title=f'Top 10 Negara - {fitur_labels[fitur]} (2022)',
    labels={fitur: fitur_labels[fitur], 'Entity': 'Negara', 'cluster_label': 'Klaster'},
    category_orders={"cluster_label": ["Digital Advanced", "Digital Developing", "Digital Emerging"]}
)

fig2.update_layout(height=400, width=None, xaxis_tickangle=-45)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

cluster_counts = df_cluster.groupby(['Year', 'cluster_label']).size().reset_index(name='count')

fig3 = px.bar(
    cluster_counts,
    x='Year',
    y='count',
    color='cluster_label',
    color_discrete_map=cluster_colors,
    title='Perubahan Jumlah Negara per Klaster (2000-2022)',
    labels={'count': 'Jumlah Negara', 'cluster_label': 'Klaster'},
    category_orders={"cluster_label": ["Digital Advanced", "Digital Developing", "Digital Emerging"]},
    barmode='stack'
)

fig3.update_layout(height=400, width=None, xaxis_tickangle=-45)

st.plotly_chart(fig3, use_container_width=True)

country_options = sorted(df_cluster['Entity'].unique())
selected_country = st.selectbox("Pilih Negara untuk Perbandingan Historis vs Forecast", country_options, index=country_options.index('Indonesia') if 'Indonesia' in country_options else 0)

hist_data = df_cluster[df_cluster['Entity'] == selected_country].sort_values('Year')
forecast_data = df_forecast[df_forecast['Entity'] == selected_country]

fig4 = make_subplots(rows=1, cols=3, subplot_titles=('Internet Usage', 'Electricity Access', 'GDP per Kapita'))

features = ['internet_usage', 'electricity_access', 'gdp_per_capita']
colors = ['#2ecc71', '#3498db', '#e74c3c']

for i, feature in enumerate(features):
    fig4.add_trace(
        go.Scatter(
            x=hist_data['Year'],
            y=hist_data[feature],
            mode='lines+markers',
            name='Historis',
            line=dict(color=colors[i], width=2),
            marker=dict(size=6),
            showlegend=(i==0)
        ),
        row=1, col=i+1
    )

    fcast = forecast_data[forecast_data['feature'] == feature]
    if not fcast.empty:
        fcast = fcast.sort_values('Year')
        fig4.add_trace(
            go.Scatter(
                x=fcast['Year'],
                y=fcast['forecast_value'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color=colors[i], width=2, dash='dash'),
                marker=dict(size=8, symbol='diamond'),
                showlegend=(i==0)
            ),
            row=1, col=i+1
        )

        fig4.add_trace(
            go.Scatter(
                x=fcast['Year'].tolist() + fcast['Year'].tolist()[::-1],
                y=fcast['upper_ci'].tolist() + fcast['lower_ci'].tolist()[::-1],
                fill='toself',
                fillcolor=f'rgba({i*80}, {180-i*50}, 50, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval',
                showlegend=(i==0)
            ),
            row=1, col=i+1
        )

fig4.update_layout(height=400, width=None, showlegend=True)
fig4.update_xaxes(title_text='Tahun', row=1, col=1)
fig4.update_xaxes(title_text='Tahun', row=1, col=2)
fig4.update_xaxes(title_text='Tahun', row=1, col=3)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.caption("Tugas Akhir Visualisasi Data Spasio-Temporal | Data: Our World in Data")