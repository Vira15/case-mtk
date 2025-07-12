# Struktur project ini terdiri dari 5 file aplikasi matematika berbasis Streamlit:

# ========== 1. Aplikasi Optimasi Produksi (Linear Programming) ==========
# File: optimasi_produksi.py
optimasi_produksi = '''
import streamlit as st
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Optimasi Produksi", layout="centered")
st.title("\U0001F3ED Aplikasi Optimasi Produksi Masker dan Hand Sanitizer")

st.markdown("### Input Data Produksi")
c1 = st.number_input("Keuntungan Masker (Rp/unit)", value=5000)
c2 = st.number_input("Keuntungan Hand Sanitizer (Rp/unit)", value=8000)
b1 = st.number_input("Total Jam Kerja", value=100)
b2 = st.number_input("Total Bahan Baku", value=80)

a11 = st.number_input("Jam kerja per Masker", value=2)
a12 = st.number_input("Jam kerja per Hand Sanitizer", value=4)
a21 = st.number_input("Bahan per Masker", value=1)
a22 = st.number_input("Bahan per Hand Sanitizer", value=2)

c = [-c1, -c2]
A = [[a11, a12], [a21, a22]]
b = [b1, b2]

x_bounds = (0, None)
y_bounds = (0, None)

res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

if res.success:
    x_opt, y_opt = res.x
    st.success("\u2705 Solusi Ditemukan!")
    st.write(f"Produksi optimal Masker: **{x_opt:.2f} unit**")
    st.write(f"Produksi optimal Hand Sanitizer: **{y_opt:.2f} unit**")
    st.write(f"Total Keuntungan Maksimum: **Rp {(-res.fun):,.0f}**")

    st.markdown("### Visualisasi Area Feasible")
    x = np.linspace(0, 100, 200)
    y1 = (b1 - a11*x) / a12
    y2 = (b2 - a21*x) / a22

    plt.figure(figsize=(7,5))
    plt.plot(x, y1, label="2x + 4y <= 100")
    plt.plot(x, y2, label="x + 2y <= 80")
    plt.fill_between(x, 0, np.minimum(y1, y2), where=(np.minimum(y1, y2) >= 0), color='skyblue', alpha=0.4)
    plt.plot(x_opt, y_opt, 'ro', label="Solusi Optimal")
    plt.xlabel("Jumlah Masker (x)")
    plt.ylabel("Jumlah Hand Sanitizer (y)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
else:
    st.error("\u274C Tidak ada solusi yang memenuhi semua kendala.")
'''

# ========== 2. Aplikasi EOQ ==========
# File: eoq_app.py
eoq_app = '''
import streamlit as st
import math

st.set_page_config(page_title="Perhitungan EOQ", layout="centered")
st.title("\U0001F4E6 Aplikasi Perhitungan EOQ")

D = st.number_input("Permintaan Tahunan (unit)", value=1200)
S = st.number_input("Biaya Pemesanan per Order (Rp)", value=10000)
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", value=2000)

if D > 0 and S > 0 and H > 0:
    EOQ = math.sqrt((2 * D * S) / H)
    freq_order = D / EOQ
    total_cost = (D / EOQ) * S + (EOQ / 2) * H

    st.success("\u2705 Hasil Perhitungan EOQ")
    st.write(f"EOQ (Jumlah Pemesanan Optimal): **{EOQ:.2f} unit**")
    st.write(f"Frekuensi Pemesanan per Tahun: **{freq_order:.2f} kali**")
    st.write(f"Total Biaya Persediaan: **Rp {total_cost:,.0f}**")
else:
    st.warning("Masukkan semua nilai dengan benar.")
'''

# ========== 3. Aplikasi Simulasi Antrian ==========
# File: queue_simulation.py
queue_simulation = '''
import streamlit as st

st.set_page_config(page_title="Simulasi Antrian", layout="centered")
st.title("\u23F3 Aplikasi Simulasi Antrian (Model M/M/1)")

λ = st.number_input("Rata-rata Kedatangan (λ)", value=3.0)
μ = st.number_input("Rata-rata Pelayanan (μ)", value=5.0)

if λ > 0 and μ > λ:
    ρ = λ / μ
    L = λ / (μ - λ)
    Lq = ρ * L
    W = 1 / (μ - λ)
    Wq = ρ * W

    st.success("\u2705 Hasil Simulasi")
    st.write(f"Tingkat Utilisasi (ρ): **{ρ:.2f}**")
    st.write(f"Pelanggan dalam sistem (L): **{L:.2f}**")
    st.write(f"Pelanggan dalam antrian (Lq): **{Lq:.2f}**")
    st.write(f"Waktu rata-rata dalam sistem (W): **{W:.2f}** menit")
    st.write(f"Waktu rata-rata tunggu (Wq): **{Wq:.2f}** menit")
else:
    st.warning("Syarat: μ harus lebih besar dari λ.")
'''

# ========== 4. Kalkulator Kalkulus ==========
# File: kalkulus_app.py
kalkulus_app = '''
import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kalkulator Kalkulus", layout="centered")
st.title("\U0001F4C8 Kalkulator Integral & Turunan")

expr_str = st.text_input("Masukkan Fungsi (misal: x**2 + 3*x)")
x = sp.symbols('x')

try:
    expr = sp.sympify(expr_str)
    diff_expr = sp.diff(expr, x)
    integ_expr = sp.integrate(expr, x)

    st.write("### Turunan:")
    st.latex(f"f'(x) = {sp.latex(diff_expr)}")

    st.write("### Integral Tak Tentu:")
    st.latex(f"\int f(x) dx = {sp.latex(integ_expr)} + C")

    x_vals = np.linspace(-10, 10, 400)
    f = sp.lambdify(x, expr, "numpy")
    f_diff = sp.lambdify(x, diff_expr, "numpy")

    plt.figure(figsize=(6,4))
    plt.plot(x_vals, f(x_vals), label="f(x)")
    plt.plot(x_vals, f_diff(x_vals), label="f'(x)", linestyle='--')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

except:
    st.warning("Masukkan fungsi yang valid.")
'''

# ========== 5. Statistik Deskriptif ==========
# File: statistik_deskriptif.py
statistik_deskriptif = '''
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Statistik Deskriptif", layout="centered")
st.title("\U0001F4CA Statistik Deskriptif")

uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
manual_input = st.text_area("Atau masukkan data manual, pisahkan dengan koma", "")

data = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    col = st.selectbox("Pilih kolom data:", df.columns)
    data = df[col].dropna()
elif manual_input:
    try:
        data = pd.Series([float(i) for i in manual_input.split(",")])
    except:
        st.error("Format data tidak valid.")

if data is not None:
    st.write(f"Mean: {np.mean(data):.2f}")
    st.write(f"Median: {np.median(data):.2f}")
    st.write(f"Modus: {data.mode().tolist()}")
    st.write(f"Standar Deviasi: {np.std(data):.2f}")
    st.write(f"Varians: {np.var(data):.2f}")

    st.markdown("### Boxplot")
    fig, ax = plt.subplots()
    sns.boxplot(data, ax=ax)
    st.pyplot(fig)
'''

