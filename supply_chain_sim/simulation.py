import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

def run_simulation():
    # Paramètres
    capacite_entrepot = {
        "Depot_A": 1000,
        "Depot_B": 1000,
        "Magasin_C": 800
    }

    # Chargement des données
    df = pd.read_csv("flux_produits.csv")
    df["date"] = pd.to_datetime(df["date"])

    # Période de simulation
    date_debut = df["date"].min()
    date_fin = df["date"].max() + pd.Timedelta(days=5)
    dates = pd.date_range(date_debut, date_fin)

    # Initialisation des stocks
    stock = defaultdict(lambda: defaultdict(int))  # stock[entrepot][produit]
    historique = []  # pour suivre l'évolution du stock

    # Simulation jour par jour
    for current_date in dates:
        # 1. Réception des produits
        livraisons = df[(df["date"] + pd.to_timedelta(df["temps_transport (j)"], unit="D")) == current_date]
        for _, row in livraisons.iterrows():
            stock[row["entrepot_destination"]][row["produit"]] += row["quantité"]

        # 2. Expédition des produits
        expeditions = df[df["date"] == current_date]
        for _, row in expeditions.iterrows():
            source = row["entrepot_source"]
            produit = row["produit"]
            quantite = row["quantité"]
            # Si le stock le permet, on expédie
            if stock[source][produit] >= quantite:
                stock[source][produit] -= quantite
            else:
                print(f"⚠️ Rupture : {source} n'a pas assez de {produit} le {current_date.date()}")

        # 3. Enregistrement des stocks journaliers
        for lieu in capacite_entrepot:
            for produit in ["Pommes", "Bananes", "Oranges"]:
                qte = stock[lieu][produit]
                historique.append({
                    "date": current_date,
                    "lieu": lieu,
                    "produit": produit,
                    "stock": qte
                })

    # Transformation en DataFrame
    df_stock = pd.DataFrame(historique)

    # Sauvegarde (optionnel)
    df_stock.to_csv("historique_stock.csv", index=False)
    print("📊 Simulation terminée, historique des stocks généré.")
