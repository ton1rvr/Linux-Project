import sys
import json
import pandas as pd

def process_movies(file_path):
    # Lire le fichier JSON
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}")
        sys.exit(1)

    # Vérifier si les résultats existent
    results = data.get("results", [])
    if not results:
        print("Aucun film trouvé dans les données.")
        sys.exit(0)

    # Extraire les informations des films
    movies = [
        {
            "Title": movie.get("title"),
            "Release Date": movie.get("release_date"),
            "Overview": movie.get("overview")
        }
        for movie in results
    ]

    # Convertir en DataFrame pour un traitement plus facile
    df = pd.DataFrame(movies)
    print("\nFilms disponibles :\n")
    print(df)

    # Sauvegarder les résultats dans un fichier CSV (optionnel)
    df.to_csv("movies.csv", index=False)
    print("\nLes données ont été enregistrées dans movies.csv.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation : python3 process_movies.py <fichier_movies.json>")
        sys.exit(1)

    json_file = sys.argv[1]
    process_movies(json_file)

