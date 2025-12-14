import streamlit as st
from generer import creer_haiku_et_image
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.title("🎋 Générateur de Haïkus Illustrés")

mots = st.text_input("Entrez 1 à 3 mots (séparés par des virgules)")

if st.button("Générer"):
    with st.spinner("Création en cours..., cela peut prendre plusieurs minutes"):
        mots_cles = [m.strip() for m in mots.split(",")]
        resultat = creer_haiku_et_image(mots_cles)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(resultat['haiku'])

        with col2:
            st.image(resultat["url_image"])

# Affichage de l'historique
st.header("📜 Historique des Haïkus")
# Barre de recherche
mots_recherche = st.text_input("Entrez des mots séparés par des virgules", "")
response = requests.get(f"{os.getenv('URL_BACK', 'http://127.0.0.1:5000/')}?mots={mots_recherche}")
history = response.json()
for h in history:
    st.markdown(f"**Mots-clés :** {h['mots_cles']}")
    st.markdown(h['haiku'])
    st.image(h['image_path'])
    st.markdown(f"*Créé le {h['created_at']}*")
    st.markdown("---")