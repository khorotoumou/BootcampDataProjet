import pandas as pd
import plotly.express as px

def afficher_stock(historique_path, produit=None, lieu=None):
    df = pd.read_csv(historique_path)
    df["date"] = pd.to_datetime(df["date"])

    # Filtres optionnels
    if produit:
        df = df[df["produit"] == produit]
    if lieu:
        df = df[df["lieu"] == lieu]

    # Graphique interactif
    fig = px.line(df, x="date", y="stock", color="lieu", line_group="produit",
                  title=f"Évolution du stock{' - ' + produit if produit else ''}{' à ' + lieu if lieu else ''}",
                  labels={"stock": "Stock", "date": "Date"})

    fig.update_layout(xaxis_title="Date", yaxis_title="Stock (unités)")
    fig.show()
