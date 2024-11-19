import requests
from bs4 import BeautifulSoup

URL_RACINE = 'https://fr.global.nba.com/scores/2024-11-11/'

response = requests.get(URL_RACINE)


if response.status_code == 200:

    html = response.text
    f = open("response.html","w")
    f.write(html)
    f.close()
    
    # Créez l'objet BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Trouvez toutes les balises <div> avec les classes et attributs spécifiques
    # game_score_table = soup.find("div", class_="GameSnapshot_finalGameTableWrapper__YRr6a", attrs={"data-cy": "game-score-table"})
    game_score_table = soup.find("div", attrs={"data-cy": "game-score-table"})
    print(game_score_table)

else:
    print(f"Erreur lors de la récupération de la page : {response.status_code}")
