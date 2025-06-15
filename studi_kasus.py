import streamlit as st
from scipy.optimize import linprog
import pandas as pd
import numpy as np
import math
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Set judul utama
st.set_page_config(page_title="Aplikasi Operasional Industri", layout="centered")
st.title("🏭 Aplikasi Analisis Operasional Industri")

# Buat tabs
tabs = st.tabs(["🔧 Optimasi Produksi", "📦 EOQ Persediaan", "🧮 Model Antrian", "📉 Prediksi Downtime"])

# ================== TAB 1: Optimasi Produksi ==================
with tabs[0]:
    st.header("🔧 Optimasi Produksi - Linear Programming")

    st.markdown("Masukkan data produksi di bawah ini:")

    profit_A = st.number_input("Keuntungan per unit Produk A", min_value=0.0, value=30.0, key="profit_A")
    profit_B = st.number_input("Keuntungan per unit Produk B", min_value=0.0, value=20.0, key="profit_B")

    st.subheader("Batasan Sumber Daya")
    resource_1 = st.number_input("Jumlah maksimum Sumber Daya 1", min_value=1.0, value=100.0, key="resource_1")
    resource_2 = st.number_input("Jumlah maksimum Sumber Daya 2", min_value=1.0, value=80.0, key="resource_2")

    st.markdown("*Konsumsi per Unit Produk*")
    cons_A_r1 = st.number_input("Produk A - konsumsi Sumber Daya 1", min_value=0.0, value=2.0, key="cons_A_r1")
    cons_B_r1 = st.number_input("Produk B - konsumsi Sumber Daya 1", min_value=0.0, value=1.0, key="cons_B_r1")
    cons_A_r2 = st.number_input("Produk A - konsumsi Sumber Daya 2", min_value=0.0, value=1.0, key="cons_A_r2")
    cons_B_r2 = st.number_input("Produk B - konsumsi Sumber Daya 2", min_value=0.0, value=1.0, key="cons_B_r2")

    if st.button("🔍 Hitung Optimasi", key="btn_optimasi"):
        c = [-profit_A, -profit_B]
        A = [[cons_A_r1, cons_B_r1], [cons_A_r2, cons_B_r2]]
        b = [resource_1, resource_2]
        bounds = [(0, None), (0, None)]

        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

        if result.success:
            produk_A = result.x[0]
            produk_B = result.x[1]
            keuntungan = -result.fun

            st.success("✅ Optimasi berhasil ditemukan:")
            st.write(f"Produksi Produk A: *{produk_A:.2f} unit*")
            st.write(f"Produksi Produk B: *{produk_B:.2f} unit*")
            st.write(f"Total Keuntungan Maksimum: *Rp {keuntungan:,.2f}*")

            df = pd.DataFrame({
                "Produk": ["A", "B"],
                "Jumlah Produksi": [produk_A, produk_B],
                "Keuntungan per Unit": [profit_A, profit_B],
                "Total Keuntungan": [produk_A * profit_A, produk_B * profit_B]
            })
            st.dataframe(df)
        else:
            st.error("❌ Tidak ditemukan solusi optimal. Periksa parameter dan batasan.")

# ================== TAB 2: EOQ ==================
with tabs[1]:
    st.header("📦 Model Persediaan Tahunan - EOQ")

    D = st.number_input("Permintaan tahunan (unit/tahun)", min_value=1.0, value=1000.0, key="D")
    S = st.number_input("Biaya pemesanan per kali (Rp)", min_value=0.0, value=50000.0, key="S")
    H = st.number_input("Biaya penyimpanan per unit per tahun (Rp)", min_value=0.0, value=1000.0, key="H")

    if st.button("📊 Hitung EOQ", key="btn_eoq"):
        if H == 0:
            st.error("❌ Biaya penyimpanan tidak boleh nol.")
        else:
            eoq = math.sqrt((2 * D * S) / H)
            frek = D / eoq
            biaya_pesan = S * frek
            biaya_simpan = (eoq / 2) * H
            total_biaya = biaya_pesan + biaya_simpan

            st.success("✅ Hasil Perhitungan:")
            st.write(f"Jumlah EOQ optimal: *{eoq:.2f} unit*")
            st.write(f"Frekuensi pemesanan per tahun: *{frek:.2f} kali*")
            st.write(f"Total biaya pemesanan: *Rp {biaya_pesan:,.2f}*")
            st.write(f"Total biaya penyimpanan: *Rp {biaya_simpan:,.2f}*")
            st.write(f"Total biaya persediaan tahunan: *Rp {total_biaya:,.2f}*")

# ================== TAB 3: Antrian M/M/1 ==================
with tabs[2]:
    st.header("🧮 Model Antrian M/M/1")

    lambda_rate = st.number_input("Rata-rata kedatangan (λ, per jam)", min_value=0.1, value=5.0, key="lambda")
    mu_rate = st.number_input("Rata-rata pelayanan (μ, per jam)", min_value=0.1, value=8.0, key="mu")

    if st.button("📊 Hitung Model Antrian", key="btn_antrian"):
        if lambda_rate >= mu_rate:
            st.error("❌ Sistem tidak stabil. Rata-rata kedatangan harus lebih kecil dari rata-rata pelayanan.")
        else:
            rho = lambda_rate / mu_rate
            L = lambda_rate / (mu_rate - lambda_rate)
            Lq = (lambda_rate ** 2) / (mu_rate * (mu_rate - lambda_rate))
            W = 1 / (mu_rate - lambda_rate)
            Wq = lambda_rate / (mu_rate * (mu_rate - lambda_rate))

            st.success("✅ Hasil Perhitungan:")
            st.write(f"Utilisasi sistem (ρ): *{rho:.2f}*")
            st.write(f"Rata-rata pelanggan dalam sistem (L): *{L:.2f}*")
            st.write(f"Rata-rata pelanggan dalam antrian (Lq): *{Lq:.2f}*")
            st.write(f"Rata-rata waktu dalam sistem (W): *{W:.2f} jam*")
            st.write(f"Rata-rata waktu dalam antrian (Wq): *{Wq:.2f} jam*")

# ================== TAB 4: Prediksi Downtime ==================
with tabs[3]:
    st.header("📉 Prediksi Downtime Mesin Industri")

    jam_operasional = st.number_input("Jam Operasional per Minggu", 10, 100, 40, key="jam")
    umur_mesin = st.number_input("Umur Mesin (Tahun)", 1, 20, 5, key="umur")

    data = {
        "jam_operasional": np.random.randint(20, 100, 50),
        "umur_mesin": np.random.randint(1, 20, 50)
    }
    df = pd.DataFrame(data)
    df["downtime"] = 0.1 * df["jam_operasional"] + 0.5 * df["umur_mesin"] + np.random.normal(0, 2, 50)

    X = df[["jam_operasional", "umur_mesin"]]
    y = df["downtime"]
    model = LinearRegression()
    model.fit(X, y)

    input_data = np.array([[jam_operasional, umur_mesin]])
    prediksi_downtime = model.predict(input_data)[0]

    st.subheader("Hasil Prediksi")
    st.write(f"Perkiraan Downtime Mesin: *{prediksi_downtime:.2f} jam/minggu*")

    st.subheader("Visualisasi Downtime")
    fig, ax = plt.subplots()
    ax.scatter(df["jam_operasional"], df["downtime"], label="Data Historis", alpha=0.6)
    ax.scatter(jam_operasional, prediksi_downtime, color="red", label="Prediksi Anda", s=100)
    ax.set_xlabel("Jam Operasional per Minggu")
    ax.set_ylabel("Downtime (jam)")
    ax.legend()
    st.pyplot(fig)