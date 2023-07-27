import pandas as pd
import requests
import os




def new_tsa_data():
    conn = get_db_url('tsa_item_demand')

    query = '''
           #SELECT *
           # FROM items
           # JOIN sales ON items.item_id = sales.item_id
           # JOIN stores ON sales.store_id = stores.store_id;
           # '''


    
    df = pd.read_sql(query, conn)
    return df
    
    
def get_tsa_data():
   

    if os.path.isfile('tsa_item_data.csv'):
        df = pd.read_csv('tsa_item_data.csv', index_col = 0)
        

    else:

        df = get_tsa_data()
        df.to_csv('tsa_item_data.csv')
        
    return df

def prep_tsa_data(df):
    
    df.sale_date = pd.to_datetime(df.sale_date)
    df = df.set_index("sale_date").sort_index()
    df['month'] = df.index.month
    df['day_of_week'] = df.index.dayofweek
    df = df.assign(sales_total=df['sale_amount'] * df['item_price'])
    
    return df

def wrangle_tsa():
  
    df = get_tsa_data()
    df = prep_tsa_data(df)
    return df

#----------------------------------------------wine----------------------------------------------

def new_opsd_data():
    if os.path.isfile('wine.csv'):
            df = pd.read_csv('wine.csv', index_col = 0)
            
    
    else:
    
            df = pd.read_csv("https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv")
            df.to_csv('wine.csv')
            
    return df
    


def prep_opsd_data(df):
    
    df.index = pd.to_datetime(df.index)
    df['month'] = df.index.month
    df['day_of_week'] = df.index.dayofweek
    df = df.fillna(method='ffill')
    df = df.fillna(method='bfill')
    
    return df

def wrangle_opsd():
  
    df = new_opsd_data()
    df = prep_opsd_data(df)
    return df