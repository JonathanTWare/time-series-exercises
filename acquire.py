import pandas as pd
import requests


def read_csv(file_path):
    
    df = pd.read_csv(file_path)
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
    
    combined_df = pd.concat([df1, df2, df3],ignore_index=True)
    
    return combined_df
    
