import streamlit as st
import pandas as pd
from simulation import run_simulation
from visualisation import afficher_stock

# Titre de l'app
st.title("📦 Simulation de Chaîne d’Approvisionnement")

# Choix utilisateur
produit = st.selectbox("Sélectionnez un produit :", ["Pommes", "Bananes", "Oranges"])
lieu = st.selectbox("Sélectionnez un lieu :", ["Depot_A", "Depot_B", "Magasin_C"])

# Bouton simulation
if st.button("Lancer la simulation"):
    run_simulation()
    st.success("✅ Simulation terminée.")

    # Affichage du graphique
    st.plotly_chart(afficher_stock("historique_stock.csv", produit=produit, lieu=lieu), use_container_width=True)
