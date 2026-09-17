import os
import subprocess
import sys

# 1. Instalacija potrebnih paketa
print("Instaliram Streamlit...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])

# 2. Kod same aplikacije
app_code = '''import os
import shutil
import streamlit as st

st.set_page_config(
    page_title="Registar atesta i Izjava o svojstvima",
    page_icon="📋",
    layout="wide"
)

STORAGE_DIR = "baza_dokumenata"
os.makedirs(STORAGE_DIR, exist_ok=True)

def dohvati_proizvode():
    return sorted([
        d for d in os.listdir(STORAGE_DIR)
        if os.path.isdir(os.path.join(STORAGE_DIR, d))
    ])

st.title("📋 Baza Izjava o svojstvima (DoP) i atesta")

# Bočni izbornik
with st.sidebar:
    st.header("⚙️ Proizvodi")
    
    novi_proizvod = st.text_input("Novi proizvod / šifra:")
    if st.button("➕ Dodaj proizvod", use_container_width=True):
        naziv = novi_proizvod.strip().replace("/", "_").replace("\\\\", "_")
        if naziv:
            putanja = os.path.join(STORAGE_DIR, naziv)
            if not os.path.exists(putanja):
                os.makedirs(putanja)
                st.success(f"Dodan: {naziv}")
                st.rerun()
            else:
                st.warning("Proizvod već postoji!")
        else:
            st.error("Unesite naziv!")

    st.divider()

    proizvodi = dohvati_proizvode()
    if proizvodi:
        st.subheader("🗑️ Brisanje")
        za_brisanje = st.selectbox("Odaberi za brisanje:", proizvodi)
        potvrda = st.checkbox("Potvrđujem trajno brisanje")
        if st.button("Obriši proizvod", type="primary", use_container_width=True):
            if potvrda:
                shutil.rmtree(os.path.join(STORAGE_DIR, za_brisanje))
                st.success(f"Obrisan: {za_brisanje}")
                st.rerun()
            else:
                st.error("Potvrdite kvačicom!")

# Glavni prozor
proizvodi = dohvati_proizvode()

if not proizvodi:
    st.info("Baza je prazna. U lijevom izborniku dodajte prvi proizvod.")
else:
    odabrani = st.selectbox("Odaberi proizvod za rad:", proizvodi)
    mapa = os.path.join(STORAGE_DIR, odabrani)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader(f"📤 Upload: {odabrani}")
        datoteke = st.file_uploader(
            "Učitaj PDF, DoP, ateste ili slike",
            accept_multiple_files=True,
            type=["pdf", "png", "jpg", "jpeg", "docx", "xlsx"]
        )
        if datoteke and st.button("Spremi učitane datoteke", use_container_width=True):
            for d in datoteke:
                with open(os.path.join(mapa, d.name), "wb") as f:
                    f.write(d.getbuffer())
            st.success("Uspješno spremljeno!")
            st.rerun()

    with col2:
        st.subheader("📑 Dokumenti u bazi")
        stavke = sorted(os.listdir(mapa))
        if not stavke:
            st.write("Nema spremljenih dokumenata.")
        else:
            for dok in stavke:
                p = os.path.join(mapa, dok)
                c_naziv, c_down, c_del = st.columns([3, 1, 1])
                c_naziv.write(f"📄 {dok}")
                with open(p, "rb") as f:
                    c_down.download_button("Preuzmi", f, file_name=dok, key=f"dl_{dok}")
                if c_del.button("Briši", key=f"del_{dok}"):
                    os.remove(p)
                    st.rerun()
'''

# 3. Zapisivanje app.py
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("Projekt pripremljen!")

# 4. Automatsko pokretanje aplikacije
subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])