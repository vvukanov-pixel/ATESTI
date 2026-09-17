import os
import shutil
import streamlit as st

st.set_page_config(
    page_title="Registar atesta i Izjava o svojstvima",
    page_icon="📋",
    layout="wide"
)

# Sprječava Google Chrome automatski prijevod na hrvatski (sprječava "PAMETNO KLIZANJE", "OGLAS", itd.)
st.html('<meta name="google" content="notranslate">')

STORAGE_DIR = "baza_dokumenata"
os.makedirs(STORAGE_DIR, exist_ok=True)

def dohvati_proizvode():
    return sorted([
        d for d in os.listdir(STORAGE_DIR)
        if os.path.isdir(os.path.join(STORAGE_DIR, d))
    ])

def dodaj_novi_proizvod():
    naziv = st.session_state.get("unos_proizvoda", "").strip().replace("/", "_").replace("\\", "_")
    if naziv:
        putanja = os.path.join(STORAGE_DIR, naziv)
        if not os.path.exists(putanja):
            os.makedirs(putanja)
            st.session_state.poruka = ("success", f"Uspješno dodan: {naziv}")
            st.session_state.unos_proizvoda = ""  # Prazni unos
        else:
            st.session_state.poruka = ("warning", f"Proizvod '{naziv}' već postoji!")
    else:
        st.session_state.poruka = ("error", "Upišite naziv proizvoda!")

st.title("📋 Registar atesta i Izjava o svojstvima (DoP)")

# Bočni izbornik
with st.sidebar:
    st.header("⚙️ Proizvodi")
    
    st.text_input("Upiši novi proizvod / šifru:", key="unos_proizvoda")
    st.button("➕ Dodaj proizvod", on_click=dodaj_novi_proizvod, use_container_width=True)

    if "poruka" in st.session_state:
        tip, tekst = st.session_state.poruka
        if tip == "success":
            st.success(tekst)
        elif tip == "warning":
            st.warning(tekst)
        elif tip == "error":
            st.error(tekst)

    st.divider()

    proizvodi = dohvati_proizvode()
    if proizvodi:
        st.subheader("🗑️ Brisanje proizvoda")
        za_brisanje = st.selectbox("Odaberi proizvod za trajno brisanje:", proizvodi, key="sb_brisanje")
        potvrda = st.checkbox("Potvrđujem trajno brisanje", key="cb_brisanje")
        if st.button("Obriši proizvod", type="primary", use_container_width=True):
            if potvrda:
                shutil.rmtree(os.path.join(STORAGE_DIR, za_brisanje))
                st.session_state.poruka = ("success", f"Obrisan: {za_brisanje}")
                st.rerun()
            else:
                st.error("Označite kvačicu za potvrdu!")

# Glavni radni prostor
proizvodi = dohvati_proizvode()

if not proizvodi:
    st.info("Baza je prazna. U lijevom izborniku unesite prvi proizvod.")
else:
    odabrani = st.selectbox(
        "👉 ODABERITE PROIZVOD S KOJIM RADITE:",
        proizvodi,
        index=0,
        key="glavni_odabir"
    )
    mapa = os.path.join(STORAGE_DIR, odabrani)

    st.divider()
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader(f"📤 Upload dokumenata za: {odabrani}")
        datoteke = st.file_uploader(
            "Izaberi ateste, DoP ili slike s diska (moguće više odjednom)",
            accept_multiple_files=True,
            type=["pdf", "png", "jpg", "jpeg", "docx", "xlsx"]
        )
        if datoteke and st.button("💾 Spremi učitane datoteke", use_container_width=True):
            for d in datoteke:
                with open(os.path.join(mapa, d.name), "wb") as f:
                    f.write(d.getbuffer())
            st.success("Dokumenti uspješno spremljeni!")
            st.rerun()

    with col2:
        st.subheader(f"📑 Spremljeni dokumenti za: {odabrani}")
        stavke = sorted(os.listdir(mapa))
        if not stavke:
            st.write("Nema spremljenih dokumenata za ovaj proizvod.")
        else:
            for dok in stavke:
                p = os.path.join(mapa, dok)
                c_naziv, c_down, c_del = st.columns([3, 1, 1])
                c_naziv.write(f"📄 **{dok}**")
                with open(p, "rb") as f:
                    c_down.download_button("Preuzmi", f, file_name=dok, key=f"dl_{dok}")
                if c_del.button("Briši", key=f"del_{dok}"):
                    os.remove(p)
                    st.rerun()