import streamlit as st
import json
import pandas as pd

# Fonction pour charger les données depuis movies.json
def load_movies_data(file_path='extracted_data/all_movies.json'):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data if isinstance(data, list) else data.get("results", [])
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier JSON : {e}")
        return []

# Interface Streamlit
def main():
    st.title("Films actuellement en salle")

    # Charger les films depuis movies.json
    movies = load_movies_data()

    # Afficher les films sous forme de tableau si les données existent
    if movies:
        # Convertir les films en DataFrame pour un affichage plus facile
        df = pd.DataFrame(movies)
        
        # Ajouter une colonne avec l'URL complète pour les images des posters
        df['poster_url'] = df['poster_path'].apply(
            lambda x: f"https://image.tmdb.org/t/p/w500{x}" if pd.notna(x) else None
        )
        
        # Sélectionner les colonnes à afficher
        df_display = df[['title', 'release_date', 'overview', 'vote_average', 'poster_url']]
        
        # Renommer les colonnes pour l'affichage en français
        df_display = df_display.rename(columns={
            'title': 'Titre',
            'release_date': 'Date de sortie',
            'overview': 'Résumé',
            'vote_average': 'Note',
            'poster_url': 'Affiche'
        })

        # Créer une colonne 'Affiche' avec les images affichées directement dans le tableau
        df_display['Affiche'] = df_display['Affiche'].apply(lambda x: f'<img src="{x}" width="900" />' if pd.notna(x) else '')

        # Afficher le tableau avec les images
        st.markdown(df_display.to_html(escape=False), unsafe_allow_html=True)

        # Ajouter un bouton pour télécharger les films en CSV
        st.download_button("Télécharger les films en CSV", df_display.to_csv(index=False), "films.csv", "text/csv")
        
    else:
        st.warning("Aucun film trouvé dans le fichier movies.json.")

if __name__ == "__main__":
    main()
