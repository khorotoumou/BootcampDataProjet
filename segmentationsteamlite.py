import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🧠 Outil de Segmentation de Clientèle")
st.markdown("Importe un fichier CSV, et on te fait une segmentation automatique des clients 💼")

# 1. Upload CSV
uploaded_file = st.file_uploader("📂 Importer un fichier CSV", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.subheader("📊 Aperçu des données")
    st.write(data.head())

    # 2. Sélection des variables numériques
    features = data.select_dtypes(include=['int64', 'float64'])

    if features.empty:
        st.warning("Aucune colonne numérique détectée pour la segmentation.")
    else:
        # 3. Standardisation
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # 4. Elbow Method pour choisir k
        inertia = []
        K_range = range(1, 11)
        for k in K_range:
            km = KMeans(n_clusters=k, init='k-means++', random_state=42)
            km.fit(scaled_features)
            inertia.append(km.inertia_)

        st.subheader("📈 Méthode du coude (Elbow Method)")
        fig, ax = plt.subplots()
        ax.plot(K_range, inertia, marker='o')
        ax.set_xlabel("Nombre de clusters (k)")
        ax.set_ylabel("Inertie")
        st.pyplot(fig)

        # 5. Sélection de k
        k = st.slider("🔢 Choisir le nombre de clusters", 2, 10, 5)

        # 6. KMeans clustering
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
        labels = kmeans.fit_predict(scaled_features)
        data['Cluster'] = labels

        st.subheader("📋 Données avec Cluster")
        st.write(data.head())

        # 7. Visualisation
        if features.shape[1] >= 2:
            st.subheader("🎯 Visualisation des groupes")
            fig2, ax2 = plt.subplots()
            sns.scatterplot(
                x=features.columns[0],
                y=features.columns[1],
                hue=data['Cluster'],
                palette='tab10',
                data=data,
                ax=ax2
            )
            st.pyplot(fig2)

        # 8. Téléchargement
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Télécharger les résultats CSV", csv, "segmentation_result.csv", "text/csv")