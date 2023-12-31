import pandas as pd
import requests
import os


def new_wine_data():
    if os.path.isfile('wine.csv'):
            df = pd.read_csv('wine.csv', index_col = 0)
            
    
    else:
    
            df = pd.read_csv("https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv")
            df.to_csv('wine.csv')
            
    return df

def get_swapi_data(url):
    data = []
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            results = json_data['results']
            data.extend(results)
            url = json_data['next']
            if url is None:
                break
        else:
            print(f"Error: {response.status_code}")
            break
    return pd.DataFrame(data)



def combine_api_data():
    df1 = get_swapi_data('https://swapi.dev/api/people/')
    df2 = get_swapi_data('https://swapi.dev/api/planets/')
    df3 = get_swapi_data('https://swapi.dev/api/starships/')
    
    ppl_planet_df = pd.merge(df1, df2, left_on='homeworld', right_on='url', how='left', suffixes=['_people', '_planets'])

    ppl_planet_df['starships'] = [', '.join(map(str, l)) for l in ppl_planet_df['starships']]
    
    return ppl_planet_df
    
