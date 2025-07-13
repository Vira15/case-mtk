import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Simulasi EOQ & ROP", layout="centered")

st.title("📦 Simulasi EOQ (Economic Order Quantity) & ROP (Reorder Point)")

# Studi kasus
st.markdown("""
### 🧾 Studi Kasus:
Sebuah toko sepatu menjual sepatu. Permintaan tahunan diperkirakan 1800 unit.
Setiap kali memesan, dikenakan biaya sebesar Rp 90.000.
Biaya penyimpanan per unit per tahun adalah Rp 2.500.
Waktu tunggu pengiriman (Lead Time) adalah 7 hari.

Berapa jumlah pemesanan optimal (EOQ) yang meminimalkan total biaya persediaan dan kapan harus melakukan pemesanan ulang (ROP)?
""")

# Rumus EOQ
st.markdown("""
### 📐 Rumus EOQ:
$$
EOQ = \\sqrt{\\frac{2DS}{H}}
$$
""")

# Rumus ROP
st.markdown("""
### 📐 Rumus ROP:
$$
ROP = (\\text{Permintaan Harian} \\times \\text{Waktu Tunggu}) + \\text{Stok Pengaman}
$$
""")

# Input variabel
D = st.number_input("Permintaan Tahunan (D)", value=1800.0, min_value=1.0, help="Jumlah total unit yang diminta dalam setahun.")
S = st.number_input("Biaya Pemesanan per Order (S)", value=90000.0, min_value=1.0, help="Biaya yang dikeluarkan setiap kali melakukan pemesanan.")
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=2500.0, min_value=1.0, help="Biaya untuk menyimpan satu unit barang selama satu tahun.")
LT = st.number_input("Waktu Tunggu Pengiriman (Lead Time) dalam Hari", value=7.0, min_value=0.0, help="Jumlah hari yang dibutuhkan dari pemesanan hingga barang diterima.")
safety_stock = st.number_input("Stok Pengaman (Safety Stock)", value=0.0, min_value=0.0, help="Stok tambahan yang disimpan untuk berjaga-jaga terhadap fluktuasi permintaan atau waktu tunggu.")


if D > 0 and S > 0 and H > 0:
    # Perhitungan EOQ
    EOQ = np.sqrt((2 * D * S) / H)

    st.success(f"📊 Jumlah pemesanan optimal (EOQ): {EOQ:.2f} unit")

    # Tampilkan proses perhitungan EOQ
    st.markdown("""
    ### 🔍 Proses Perhitungan EOQ:
    D = %.0f unit/tahun
    S = Rp %.0f per order
    H = Rp %.0f per unit/tahun

    $$
    EOQ = \\sqrt{\\frac{2 \\times %.0f \\times %.0f}{%.0f}} = \\sqrt{\\frac{%.0f}{%.0f}} = %.2f
    $$
    """ % (D, S, H, D, S, H, 2*D*S, H, EOQ))

    # Perhitungan ROP
    permintaan_harian = D / 365 # Asumsi 365 hari dalam setahun
    ROP = (permintaan_harian * LT) + safety_stock

    st.success(f"📈 Titik Pemesanan Ulang (ROP): {ROP:.2f} unit")

    # Tampilkan proses perhitungan ROP
    st.markdown("""
    ### 🔍 Proses Perhitungan ROP:
    Permintaan Tahunan (D) = %.0f unit/tahun
    Waktu Tunggu (Lead Time) = %.0f hari
    Stok Pengaman = %.0f unit

    Permintaan Harian = D / 365 = %.0f / 365 = %.2f unit/hari

    $$
    ROP = (\\text{Permintaan Harian} \\times \\text{Waktu Tunggu}) + \\text{Stok Pengaman} = (%.2f \\times %.0f) + %.0f = %.2f
    $$
    """ % (D, LT, safety_stock, D, permintaan_harian, permintaan_harian, LT, safety_stock, ROP))


    # Grafik total biaya
    # Pastikan Q memiliki nilai yang cukup untuk membuat grafik terlihat
    Q_min = max(1, int(EOQ * 0.5)) # Mulai dari 50% EOQ
    Q_max = int(EOQ * 2) # Sampai 200% EOQ
    Q = np.arange(Q_min, Q_max + 1) # Tambahkan 1 agar Q_max termasuk

    # Hindari pembagian dengan nol jika Q mengandung 0
    Q_filtered = Q[Q > 0]

    if len(Q_filtered) > 0:
        TC = (D / Q_filtered) * S + (Q_filtered / 2) * H

        fig, ax = plt.subplots(figsize=(8, 5)) # Ukuran grafik yang sedikit lebih besar
        ax.plot(Q_filtered, TC, label="Total Biaya", color='blue')
        ax.axvline(EOQ, color='red', linestyle='--', label=f"EOQ ≈ {EOQ:.0f}")
        ax.set_xlabel("Jumlah Pemesanan (Q)")
        ax.set_ylabel("Total Biaya (Rp)")
        ax.set_title("Grafik Total Biaya vs Jumlah Pemesanan")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7) # Tambahkan grid

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        st.image(buf, width=600) # Ukuran gambar yang sedikit lebih besar

        st.markdown("""
        ### 📝 Penjelasan:
        - **Grafik Total Biaya:**
            - Titik minimum pada grafik menunjukkan jumlah pemesanan optimal (EOQ), di mana total biaya persediaan (biaya pemesanan + biaya penyimpanan) adalah yang terendah.
            - Di kiri EOQ: Terlalu sering memesan, menyebabkan biaya pemesanan tinggi.
            - Di kanan EOQ: Jumlah persediaan yang disimpan besar, menyebabkan biaya penyimpanan tinggi.
        """)
    else:
        st.warning("Rentang jumlah pemesanan (Q) tidak valid untuk grafik. Sesuaikan nilai input.")

    # --- Grafik Simulasi Tingkat Persediaan (ROP) ---
    st.markdown("### 📈 Simulasi Tingkat Persediaan")

    # Simulation parameters
    sim_days = 90 # Simulate for 90 days
    inventory_level = [EOQ + safety_stock] # Start with initial inventory (EOQ + safety stock)
    days = [0]
    orders_placed = []
    orders_received = []
    current_inventory = EOQ + safety_stock
    order_in_transit = [] # Stores (arrival_day, quantity)

    for day in range(1, sim_days + 1):
        current_inventory -= permintaan_harian
        
        # Check for incoming orders
        newly_received_orders = []
        for i, (arrival_day, quantity) in enumerate(order_in_transit):
            if day >= arrival_day:
                current_inventory += quantity
                newly_received_orders.append(i)
                orders_received.append(day)
        
        # Remove received orders from in_transit list (iterate backwards to avoid index issues)
        for i in sorted(newly_received_orders, reverse=True):
            order_in_transit.pop(i)

        # Check if ROP is hit and place an order
        # Place an order if current inventory is at or below ROP AND no order is currently in transit
        # This prevents multiple orders being placed for the same cycle if inventory stays low
        if current_inventory <= ROP and not any(q > 0 for _, q in order_in_transit):
            orders_placed.append(day)
            order_arrival_day = day + LT
            order_in_transit.append((order_arrival_day, EOQ))
            
        inventory_level.append(max(0, current_inventory)) # Inventory cannot go below zero
        days.append(day)

    fig_rop, ax_rop = plt.subplots(figsize=(10, 6))
    ax_rop.plot(days, inventory_level, label="Tingkat Persediaan", color='green')
    ax_rop.axhline(ROP, color='purple', linestyle=':', label=f"ROP = {ROP:.0f}")
    ax_rop.axhline(0, color='black', linestyle='-', linewidth=0.8) # Zero inventory line

    # Mark order placements and receipts
    # Use a set to avoid duplicate labels in legend if multiple lines are plotted
    labels_placed = set()
    labels_received = set()

    for op_day in orders_placed:
        label = "Pemesanan Ditempatkan"
        ax_rop.axvline(op_day, color='blue', linestyle='--', alpha=0.6, label=label if label not in labels_placed else "")
        labels_placed.add(label)

    for or_day in orders_received:
        label = "Pemesanan Diterima"
        ax_rop.axvline(or_day, color='orange', linestyle='--', alpha=0.6, label=label if label not in labels_received else "")
        labels_received.add(label)

    ax_rop.set_xlabel("Hari")
    ax_rop.set_ylabel("Tingkat Persediaan (Unit)")
    ax_rop.set_title("Simulasi Tingkat Persediaan dengan EOQ dan ROP")
    ax_rop.legend()
    ax_rop.grid(True, linestyle='--', alpha=0.7)

    buf_rop = io.BytesIO()
    fig_rop.savefig(buf_rop, format="png", bbox_inches="tight")
    st.image(buf_rop, width=700)

    st.markdown("""
    - **Grafik Simulasi Tingkat Persediaan:**
        - Garis hijau menunjukkan fluktuasi tingkat persediaan dari waktu ke waktu.
        - Garis ungu putus-putus menunjukkan Reorder Point (ROP). Ketika tingkat persediaan mencapai atau di bawah garis ini, pesanan baru ditempatkan.
        - Garis vertikal biru putus-putus menunjukkan hari di mana pesanan baru ditempatkan.
        - Garis vertikal oranye putus-putus menunjukkan hari di mana pesanan yang ditempatkan sebelumnya diterima.
    """)

else:
    st.warning("Masukkan nilai D, S, dan H yang valid (semua harus > 0).")
