import requests
import json
import pandas as pd

'''
Get a list of movies that are currently in theatres.

'''

min_release_date = "2024-09-01"  
max_release_date = "2024-12-31"  

url = "https://api.themoviedb.org/3/discover/movie"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1N2U1MTYyYTU1ZTgyMDBmY2M0MzczYjhlNDhiM2YyZSIsIm5iZiI6MTczMjAzMjc2Ni41NDg0MTc2LCJzdWIiOiI2NTRhYjgzMDYzMzJmNzAwYzYzN2IwYjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.zMGN5nfBXnE78dm_-3qD99C7FUkBnksqaBCtKXrKLc8",
    "accept": "application/json",
}

def get_page_current_movies(page_nb : int, min_date : str, max_date : str) -> json :

    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": page_nb,
        "sort_by": "popularity.desc",
        "with_release_type": "2|3",
        "release_date.gte": min_date,
        "release_date.lte": max_date,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Erreur for {response.status_code}: {response.text}")

def get_all_current_movies() -> None :

    data = get_page_current_movies(1,min_date=min_release_date,max_date=max_release_date)
    #total_nb_pages = data['total_pages']
    total_nb_pages = 499
    total_nb_results = data['total_results']
    result_example = (data['results'])[0]
    index = range(0,total_nb_results)
    columns = list(result_example.keys())
    current_movies_df = pd.DataFrame(index=index,columns=columns)
    chemin_csv="extracted_data/current_movies/current_movies.csv"
    num_index=0

    for num_page in range(1,total_nb_pages):

        data = get_page_current_movies(num_page,min_date=min_release_date,max_date=max_release_date)
        is_extraction_finished = False

        for result in data['results'] :

            current_movies_df.loc[num_index] = list(result.values())

            if result['id'] in (None, "", [], {}) :
                print("Tout les films ont été ingérés")
                is_extraction_finished = True
                break

            num_index+=1 
        
        if is_extraction_finished :
            break

    current_movies_df.to_csv(chemin_csv, index=False)

    return None
        
get_all_current_movies()

