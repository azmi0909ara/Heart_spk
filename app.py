
# 🫀 Sistem Penunjang Keputusan: Diagnosa Risiko Penyakit Jantung
# Metode: Logika Fuzzy (scikit-fuzzy)
# Mode: Gabungan (Dataset Kaggle + Input Manual)
# Dibuat oleh: Azmi .A (Tugas Proyek SPK)


import streamlit as st
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


# 🔹 Pengaturan Halaman Streamlit

st.set_page_config(page_title="Sistem Fuzzy Diagnosa Jantung", page_icon="🫀", layout="centered")
st.title("🫀 Sistem Penunjang Keputusan: Diagnosa Risiko Penyakit Jantung (Logika Fuzzy)")

st.markdown("""
Aplikasi ini menggunakan **Logika Fuzzy adaptif** untuk memprediksi **tingkat risiko penyakit jantung** 
berdasarkan variabel kesehatan dari dataset Kaggle Heart Disease.
Anda dapat memilih data pasien dari dataset atau mengisi data secara manual.
""")


# 🔹 Load Dataset

@st.cache_data
def load_data():
    df = pd.read_csv("heart.csv")
    return df

try:
    df = load_data()
    st.success("✅ Dataset berhasil dimuat!")
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()


# 🔹 Tentukan batas distribusi otomatis dari dataset

def get_range(col):
    return df[col].min(), df[col].mean(), df[col].max()

age_min, age_mean, age_max = get_range('age')
trestbps_min, trestbps_mean, trestbps_max = get_range('trestbps')
chol_min, chol_mean, chol_max = get_range('chol')
thalach_min, thalach_mean, thalach_max = get_range('thalach')
oldpeak_min, oldpeak_mean, oldpeak_max = get_range('oldpeak')


# 🔹 Pilihan Mode Input

mode = st.radio("Pilih Mode Input:", ["Gunakan Data dari Dataset", "Input Manual"])

if mode == "Gunakan Data dari Dataset":
    st.markdown("### 📋 Pilih Data Pasien dari Dataset")
    index = st.slider("Pilih nomor pasien (index baris dataset)", 0, len(df) - 1, 0)
    patient = df.iloc[index]
    st.dataframe(patient.to_frame().T)

    age = patient["age"]
    trestbps = patient["trestbps"]
    chol = patient["chol"]
    thalach = patient["thalach"]
    oldpeak = patient["oldpeak"]

else:
    st.markdown("### ✍️ Input Manual Data Pasien")
    age = st.slider("Usia Pasien", int(age_min), int(age_max), int(age_mean))
    trestbps = st.slider("Tekanan Darah (mmHg)", int(trestbps_min), int(trestbps_max), int(trestbps_mean))
    chol = st.slider("Kolesterol (mg/dl)", int(chol_min), int(chol_max), int(chol_mean))
    thalach = st.slider("Detak Jantung Maksimum (bpm)", int(thalach_min), int(thalach_max), int(thalach_mean))
    oldpeak = st.slider("Nilai Oldpeak", float(oldpeak_min), float(oldpeak_max), float(oldpeak_mean))


# 🔹 Definisi Variabel Fuzzy (menggunakan distribusi dataset)

age_f = ctrl.Antecedent(np.arange(age_min, age_max + 1, 1), 'age')
trestbps_f = ctrl.Antecedent(np.arange(trestbps_min, trestbps_max + 1, 1), 'trestbps')
chol_f = ctrl.Antecedent(np.arange(chol_min, chol_max + 1, 1), 'chol')
thalach_f = ctrl.Antecedent(np.arange(thalach_min, thalach_max + 1, 1), 'thalach')
oldpeak_f = ctrl.Antecedent(np.arange(oldpeak_min, oldpeak_max + 0.1, 0.1), 'oldpeak')
risk = ctrl.Consequent(np.arange(0, 101, 1), 'risk')


# 🔹 Fungsi Keanggotaan Otomatis Berdasarkan Distribusi Data

age_f['muda'] = fuzz.trimf(age_f.universe, [age_min, age_min, age_mean])
age_f['paruh_baya'] = fuzz.trimf(age_f.universe, [age_min, age_mean, age_max])
age_f['tua'] = fuzz.trimf(age_f.universe, [age_mean, age_max, age_max])

trestbps_f['rendah'] = fuzz.trimf(trestbps_f.universe, [trestbps_min, trestbps_min, trestbps_mean])
trestbps_f['normal'] = fuzz.trimf(trestbps_f.universe, [trestbps_min, trestbps_mean, trestbps_max])
trestbps_f['tinggi'] = fuzz.trimf(trestbps_f.universe, [trestbps_mean, trestbps_max, trestbps_max])

chol_f['rendah'] = fuzz.trimf(chol_f.universe, [chol_min, chol_min, chol_mean])
chol_f['normal'] = fuzz.trimf(chol_f.universe, [chol_min, chol_mean, chol_max])
chol_f['tinggi'] = fuzz.trimf(chol_f.universe, [chol_mean, chol_max, chol_max])

thalach_f['rendah'] = fuzz.trimf(thalach_f.universe, [thalach_min, thalach_min, thalach_mean])
thalach_f['sedang'] = fuzz.trimf(thalach_f.universe, [thalach_min, thalach_mean, thalach_max])
thalach_f['tinggi'] = fuzz.trimf(thalach_f.universe, [thalach_mean, thalach_max, thalach_max])

oldpeak_f['normal'] = fuzz.trimf(oldpeak_f.universe, [oldpeak_min, oldpeak_min, oldpeak_mean])
oldpeak_f['sedang'] = fuzz.trimf(oldpeak_f.universe, [oldpeak_min, oldpeak_mean, oldpeak_max])
oldpeak_f['tinggi'] = fuzz.trimf(oldpeak_f.universe, [oldpeak_mean, oldpeak_max, oldpeak_max])

risk['rendah'] = fuzz.trimf(risk.universe, [0, 0, 40])
risk['sedang'] = fuzz.trimf(risk.universe, [30, 50, 70])
risk['tinggi'] = fuzz.trimf(risk.universe, [60, 100, 100])


# 🔹 Aturan Fuzzy

rules = [
    ctrl.Rule(age_f['tua'] & trestbps_f['tinggi'] & chol_f['tinggi'], risk['tinggi']),
    ctrl.Rule(age_f['paruh_baya'] & trestbps_f['normal'] & chol_f['normal'], risk['sedang']),
    ctrl.Rule(age_f['muda'] & trestbps_f['rendah'] & chol_f['rendah'], risk['rendah']),
    ctrl.Rule(thalach_f['tinggi'] & oldpeak_f['normal'], risk['rendah']),
    ctrl.Rule(oldpeak_f['tinggi'] | trestbps_f['tinggi'], risk['tinggi']),
    ctrl.Rule(chol_f['tinggi'] & oldpeak_f['sedang'], risk['sedang']),
]

risk_ctrl = ctrl.ControlSystem(rules)
risk_sim = ctrl.ControlSystemSimulation(risk_ctrl)


# 🔹 Proses Inferensi Fuzzy

try:
    risk_sim.input['age'] = age
    risk_sim.input['trestbps'] = trestbps
    risk_sim.input['chol'] = chol
    risk_sim.input['thalach'] = thalach
    risk_sim.input['oldpeak'] = oldpeak
    risk_sim.compute()
    hasil = risk_sim.output.get('risk', np.nan)

    if np.isnan(hasil):
        st.error("❌ Tidak ada aturan yang cocok untuk kondisi input ini.")
    else:
        st.subheader("📊 Hasil Diagnosa Fuzzy")
        st.write(f"**Nilai Risiko (defuzzifikasi):** `{hasil:.2f} / 100`")

        if hasil < 40:
            st.success("🟢 Risiko Rendah — Jantung dalam kondisi baik.")
        elif hasil < 70:
            st.warning("🟡 Risiko Sedang — Perlu pemeriksaan lanjutan.")
        else:
            st.error("🔴 Risiko Tinggi — Segera konsultasi ke dokter jantung.")

        # Visualisasi hasil
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.set_xlim(0, 100)
        ax.barh([""], [100], color="#eee", height=0.3)
        ax.barh([""], [hasil], color=("green" if hasil < 40 else "gold" if hasil < 70 else "red"), height=0.3)
        ax.text(hasil + 1, 0, f"{hasil:.1f}%", va="center", fontsize=10)
        ax.set_yticks([])
        ax.set_title("Indikator Risiko Penyakit Jantung", fontsize=12)
        st.pyplot(fig)

except Exception as e:
    st.error(f"Terjadi kesalahan saat menghitung fuzzy: {e}")


# 🔹 Penjelasan Variabel

with st.expander("ℹ️ Penjelasan Variabel Input"):
    st.markdown("""
    **🧾 Penjelasan Data Masukan:**
    - **Usia:** Semakin tua, semakin tinggi risiko jantung.
    - **Tekanan Darah (`trestbps`):** Normal sekitar 120 mmHg; tinggi >140 menandakan hipertensi.
    - **Kolesterol (`chol`):** Normal 180–220 mg/dl; di atas 240 dianggap tinggi.
    - **Detak Jantung Maksimum (`thalach`):** Semakin tinggi (>=150) menandakan jantung masih kuat.
    - **Oldpeak:** Nilai depresi ST; semakin tinggi, semakin berisiko.

    **🎯 Interpretasi Nilai Risiko:**
    - 0–39 → Risiko **Rendah**
    - 40–69 → Risiko **Sedang**
    - 70–100 → Risiko **Tinggi**
    """)

st.markdown("---")
st.caption("🧠 Dibangun menggunakan Streamlit + scikit-fuzzy | Proyek SPK 2025 oleh Azmi .A")
