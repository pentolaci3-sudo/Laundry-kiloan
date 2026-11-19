import re
import streamlit as st

st.set_page_config(page_title="Laundry Kiloan - Struk Digital", page_icon="🧺", layout="centered")

# ---------- Logika perhitungan ----------
def rupiah(n):
    return "Rp " + f"{n:,}".replace(",", ".")


def valid_nim(nim):
    return len(nim) == 10 and nim.isascii() and nim.isdigit()


def parse_berat(teks):
    """Kembalikan bilangan bulat > 0, atau None jika tidak valid."""
    teks = teks.strip()
    if not re.fullmatch(r"-?\d+", teks):
        return None
    nilai = int(teks)
    return nilai if nilai > 0 else None


def hitung(nim, berat):
    digit_genap = sum(1 for d in nim if int(d) % 2 == 0)  # 0 dihitung genap
    tarif = 5000 + int(nim[-1]) * 500
    diskon = digit_genap  # persen
    normal = berat * tarif
    potongan = normal * diskon // 100
    return {
        "tarif": tarif,
        "genap": digit_genap,
        "diskon": diskon,
        "normal": normal,
        "potongan": potongan,
        "total": normal - potongan,
    }


# ---------- State ----------
st.session_state.setdefault("nim", "")
st.session_state.setdefault("berat", "")
st.session_state.setdefault("hasil", None)
st.session_state.setdefault("error", [])


def on_hitung():
    nim = st.session_state.nim.strip()
    berat_teks = st.session_state.berat
    errors = []
    if not valid_nim(nim):
        errors.append("NIM tidak valid: harus terdiri dari tepat 10 digit angka.")
    berat = parse_berat(berat_teks)
    if berat is None:
        errors.append("Berat cucian tidak valid: harus bilangan bulat lebih dari 0.")
    st.session_state.error = errors
    st.session_state.hasil = None if errors else {"nim": nim, "berat": berat, **hitung(nim, berat)}


def on_reset():
    st.session_state.nim = ""
    st.session_state.berat = ""
    st.session_state.hasil = None
    st.session_state.error = []


# ---------- Gaya ----------
st.markdown(
    """
<style>
.stApp { background: linear-gradient(160deg, #0f172a 0%, #1e1b4b 55%, #312e81 100%); }
h1, h2, h3, label, p, span, div { color: #e2e8f0; }
.hero { text-align:center; padding: 8px 0 18px; }
.hero h1 { font-size: 2.1rem; margin: 0; letter-spacing: 1px; }
.hero p { color:#a5b4fc; margin: 4px 0 0; }
.struk { background:#fffdf5; color:#1f2937; border-radius:14px; padding:22px 24px;
         font-family:'Courier New', monospace; box-shadow:0 12px 30px rgba(0,0,0,.45);
         border-top:8px dashed #f59e0b; }
.struk * { color:#1f2937 !important; }
.struk h3 { text-align:center; margin:0 0 2px; font-size:1.2rem; }
.struk .sub { text-align:center; font-size:.8rem; color:#6b7280 !important; margin-bottom:10px; }
.struk hr { border:none; border-top:2px dashed #9ca3af; margin:10px 0; }
.row { display:flex; justify-content:space-between; padding:3px 0; font-size:.95rem; }
.total { display:flex; justify-content:space-between; font-weight:800; font-size:1.25rem;
         background:#d1fae5; border-radius:8px; padding:8px 10px; margin-top:6px; }
.badge { display:inline-block; background:#4f46e5; color:#fff !important; border-radius:20px;
         padding:2px 12px; font-size:.78rem; margin-bottom:8px; }
.err { background:#fee2e2; border-left:6px solid #dc2626; padding:10px 14px; border-radius:8px; margin-top:8px; }
.err * { color:#7f1d1d !important; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><h1>🧺 Laundry Kiloan</h1><p>Struk digital · diskon dari digit genap NIM</p></div>',
    unsafe_allow_html=True,
)

# ---------- Input ----------
st.text_input("NIM (10 digit)", key="nim", placeholder="contoh: 2411001347", max_chars=30)
st.text_input("Berat cucian (kg, bilangan bulat)", key="berat", placeholder="contoh: 10")

c1, c2 = st.columns(2)
c1.button("🧮 Hitung", on_click=on_hitung, use_container_width=True, type="primary")
c2.button("♻️ Reset", on_click=on_reset, use_container_width=True)

# ---------- Output ----------
for pesan in st.session_state.error:
    st.markdown(f'<div class="err">⚠️ {pesan}</div>', unsafe_allow_html=True)

h = st.session_state.hasil
if h:
    st.markdown(
        f"""
<div class="struk">
  <h3>LAUNDRY KILOAN</h3>
  <div class="sub">— struk pembayaran —</div>
  <span class="badge">NIM {h['nim']}</span>
  <div class="row"><span>Berat cucian</span><span>{h['berat']} kg</span></div>
  <hr>
  <div class="row"><span>Tarif per kg</span><span>{rupiah(h['tarif'])}</span></div>
  <div class="row"><span>Jumlah digit genap</span><span>{h['genap']}</span></div>
  <div class="row"><span>Persen diskon</span><span>{h['diskon']} %</span></div>
  <hr>
  <div class="row"><span>Biaya normal</span><span>{rupiah(h['normal'])}</span></div>
  <div class="row"><span>Potongan</span><span>- {rupiah(h['potongan'])}</span></div>
  <div class="total"><span>TOTAL BAYAR</span><span>{rupiah(h['total'])}</span></div>
  <div class="sub" style="margin-top:12px">Terima kasih sudah mencuci di sini 💙</div>
</div>
""",
        unsafe_allow_html=True,
    )
