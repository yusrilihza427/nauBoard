import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === 1. Load Dataset ===
df = pd.read_csv("layoffs_cleaned_featured.csv")

st.set_page_config(page_title="Dashboard PHK Global 2020–2025", layout="wide")

st.title("📊 Dashboard Analisis PHK Global (2020–2025)")
st.markdown("### Pendekatan Data Sains dengan Dashboard Interaktif")

# === 2. Sidebar Filter ===
st.sidebar.header("🔍 Filter Data")
selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)
selected_region = st.sidebar.multiselect(
    "Pilih Region",
    options=df["region"].dropna().unique(),
    default=df["region"].dropna().unique()
)

df_filtered = df[(df["year"].isin(selected_year)) & (df["region"].isin(selected_region))]

# === 3. Ringkasan Utama ===
st.subheader("📈 Ringkasan Data Utama")
col1, col2, col3 = st.columns(3)
col1.metric("Total Perusahaan", len(df_filtered["company"].unique()))
col2.metric("Total PHK", int(df_filtered["total_laid_off"].sum()))
col3.metric("Rata-rata Persentase PHK", f"{df_filtered['percentage_laid_off'].mean():.2f}%")

# === 4. Visualisasi Interaktif ===
st.subheader("📉 Tren PHK per Tahun")
trend = df_filtered.groupby("year")["total_laid_off"].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=trend, x="year", y="total_laid_off", marker="o", ax=ax1)
ax1.set_title("Tren Total PHK per Tahun")
ax1.set_xlabel("Tahun")
ax1.set_ylabel("Jumlah PHK")
st.pyplot(fig1)

st.subheader("🌍 Distribusi PHK Berdasarkan Region")
region_summary = df_filtered.groupby("region")["total_laid_off"].sum().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=region_summary, x="region", y="total_laid_off", ax=ax2)
ax2.set_title("Distribusi Total PHK per Region")
ax2.set_xlabel("Region")
ax2.set_ylabel("Total PHK")
st.pyplot(fig2)

st.subheader("🏢 Skala PHK Perusahaan")
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.countplot(data=df_filtered, x="layoff_scale", palette=["green", "orange", "red"], ax=ax3)
ax3.set_title("Distribusi Skala PHK")
st.pyplot(fig3)

# === 5. Data Table ===
st.subheader("📋 Data Tabel")
st.dataframe(df_filtered)

# === 6. Catatan Analitik ===
st.markdown("""
**Insight Awal:**
- PHK global menunjukkan tren meningkat terutama setelah tahun 2022.
- Wilayah Amerika Utara dan Asia menjadi dua region paling terdampak.
- Mayoritas PHK terjadi pada perusahaan dengan skala sedang hingga besar.
""")
