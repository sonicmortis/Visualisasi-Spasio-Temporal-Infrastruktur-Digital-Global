# 🌍 Analisis dan Pemetaan Infrastruktur Digital Global melalui Visualisasi Spasio-Temporal dan Machine Learning Tahun 2000 - 2022


### Identitas

| **Nama** | Muhammad Luthfi Kautsar Rizata |
|----------|-------------------------------|
| **NIM** | 2311532020 |
| **Mata Kuliah** | Visualisasi Data Spasio-Temporal |
| **Dosen Pengampu** | Nurfiah S.ST., M.Kom |

---
## 📋 Deskripsi Proyek

Proyek ini merupakan dashboard interaktif untuk menganalisis dan memvisualisasikan perkembangan infrastruktur digital global dari tahun 2000 hingga 2022. Menggunakan data dari **Our World in Data**, dashboard ini menampilkan tiga indikator utama:

1. **Penggunaan Internet (%)** - Persentase penduduk yang menggunakan internet
2. **Akses Listrik (%)** - Persentase penduduk dengan akses listrik
3. **GDP per Kapita (USD)** - Rata-rata output ekonomi per penduduk pada suatu negara

### Metode yang Digunakan

- **K-Means Clustering** (k=3) - Mengelompokkan negara ke dalam tiga kategori: *Digital Advanced*, *Digital Developing*, dan *Digital Emerging*
- **Prophet dan ARIMA Forecasting** - Prediksi nilai untuk ketiga indikator pada periode 2023-2027
- **Analisis Spasio-Temporal** - Visualisasi perubahan pola dari waktu ke waktu menggunakan peta animasi

---
##  🎯 Fitur Aplikasi

| No | Fitur | Deskripsi |
|----|-------|-----------|
| 1 | **Animasi Peta Klaster** | Peta dunia  yang menunjukkan perubahan klaster infrastruktur digital setiap tahun (2000-2022) |
| 2 | **Dropdown Pemilihan Fitur** | Pilih fitur (Internet/Listrik/GDP) untuk mengubah tampilan grafik tren dan top 10 negara |
| 3 | **Tren per Klaster** | Grafik tren rata-rata fitur terpilih per klaster dari 2000-2022 |
| 4 | **Top 10 Negara** | Grafik 10 negara tertinggi untuk fitur terpilih pada tahun 2022 |
| 5 | **Jumlah Negara per Klaster** | Grafik batang bertumpuk yang menunjukkan perubahan jumlah negara di setiap klaster per tahun |
| 6 | **Historis vs Forecast** | Perbandingan data historis dan prediksi 2023-2027 untuk 3 fitur sekaligus per negara |

---
## 🛠️ Instalasi

### Prasyarat

- Python 3.11.0 atau lebih baru
- Pip (Python package manager)
- Git (opsional, untuk clone repository)

### Langkah-langkah

**1. Clone repository**

```bash
git clone https://github.com/sonicmortis/Visualisasi-Spasio-Temporal-Infrastruktur-Digital-Global.git
cd project-akhir
```

**2. Buat virtual environment**

```bash
python -m venv venv
```

**3. Aktifkan virtual environment (Windows)**

```bash
venv\Scripts\activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Jalankan Aplikasi**

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada alamat:

```bash
http://localhost:8501
```
## Penggunaan
1. Amati animasi perubahan klaster di peta dunia
2. Pilih fitur yang ingin dianalisis (Internet/Listrik/GDP) di sidebar
3. Lihat grafik tren dan distribusi di bagian bawah
4. Pilih negara tertentu untuk melihat perbandingan historis vs forecast```markdown

##  📁 Struktur Proyek
<img width="400" height="370" alt="image" src="https://github.com/user-attachments/assets/b3a0557f-4c4b-4fe3-b7e8-2df9232287dd" />

## 📊 Sumber Data

Seluruh dataset berasal dari **Our World in Data** dengan periode 2000-2022:

| Dataset | Deskripsi | Sumber |
|---------|-----------|--------|
| Internet Usage | Persentase penduduk yang menggunakan internet | Our World in Data |
| Electricity Access | Persentase penduduk dengan akses listrik | Our World in Data |
| GDP per Capita | Rata-rata output ekonomi per penduduk suatu negara (USD) | Our World in Data |

Data telah melalui tahapan:
- ✅ Cleaning (penanganan missing values, format konsistensi)
- ✅ Emerging ketiga dataset menjadi satu
- ✅ Transformasi (log transformasi untuk GDP)
- ✅ Feature scaling (StandardScaler)
- ✅ Clustering (K-Means, k=3)
- ✅ Forecasting ARIMA dan Prophet 

---
## 🔬 Metodologi

### 1. Feature Selection

Tiga fitur utama yang digunakan:
- `internet_usage` - Mewakili tingkat digitalisasi
- `electricity_access` - Mewakili infrastruktur dasar
- `log_gdp` - Mewakili kapasitas ekonomi (setelah transformasi log)

### 2. Clustering (K-Means)

- Jumlah cluster: **3** (ditentukan berdasarkan Elbow Method)
- Label cluster:
  - **Digital Advanced** - Negara dengan infrastruktur digital tertinggi
  - **Digital Developing** - Negara dengan infrastruktur digital menengah
  - **Digital Emerging** - Negara dengan infrastruktur digital rendah

### 3. Forecasting (Prophet & ARIMA)

- **Prophet**: Digunakan untuk forecasting `electricity_access` (MAE: 1.22)
- **ARIMA**: Digunakan untuk forecasting `internet_usage` (MAE: 4.65) dan `gdp_per_capita` (MAE: 786.68)

### 4. Evaluasi Model

| Fitur | Model Terbaik | MAE | RMSE |
|-------|---------------|-----|------|
| Internet Usage | ARIMA | 4.65 | 5.29 |
| Electricity Access | Prophet | 1.22 | 1.44 |
| GDP per Kapita | ARIMA | 786.68 | 957.16 |

---
## ⚙️ Teknologi yang Digunakan

| Teknologi | Kegunaan |
|-----------|----------|
| **Python 3.11** | Bahasa pemrograman utama |
| **Streamlit** | Framework dashboard interaktif |
| **Plotly** | Visualisasi interaktif (peta, grafik) |
| **Pandas** | Manipulasi dan analisis data |
| **NumPy** | Komputasi numerik |
| **Scikit-learn** | K-Means clustering, StandardScaler |
| **Prophet** | Time series forecasting |
| **Statsmodels** | ARIMA forecasting |
| **Joblib** | Serialisasi model |


---

## 📧 Kontak

| Nama | Muhammad Luthfi Kautsar Rizata |
|------|-------------------------------|
| NIM | 2311532020 |
| Email | luthfikautsarrizata@gmail.com |
| GitHub | sonicmortis |

---

**Terima kasih telah membaca!**

---
