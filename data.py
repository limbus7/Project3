import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.offline import plot
import psycopg2

def connection():
    port = '5432'
    username = 'postgres'
    password = '12345678'
    host = 'database-1.chueoayw4q5g.ca-central-1.rds.amazonaws.com'
    database = 'Crypto20_db'

    con = psycopg2.connect(
        user = username,
        password = password,
        host = host,
        port = port,
        database = database
    )

    cursor = con.cursor()
    return cursor

def get_data():
    cursor = connection()

    query = """select * from information_schema.tables where table_schema = 'public'"""
    cursor.execute(query)
    information = pd.DataFrame(cursor.fetchall(),columns=[i[0] for i in cursor.description])
    table_names = information['table_name'].iloc[:5]

    flag = True
    for j in table_names:
        query = f'SELECT * FROM public."{j}" ORDER BY "Date"'
        cursor.execute(query)
        if flag == True:
            cols = ['Date'] + [i[0]+'_'+j for i in cursor.description if 'date' not in i[0].lower()]
            df = pd.DataFrame(cursor.fetchall(),columns=cols)
            flag = False
        else:
            cols = ['Date'] + [i[0]+'_'+j for i in cursor.description if 'date' not in i[0].lower()]
            temp_df = pd.DataFrame(cursor.fetchall(),columns=cols)
            df = df.merge(right=temp_df,on = 'Date')

    return df

def market_cap(df):
    open_df = df[["Date"]+[i for i in list(df.columns) if 'Open' in i]]
    vol_df = df[["Date"]+[i for i in list(df.columns) if 'Vol' in i]]

    market_cap = pd.DataFrame([])
    market_cap['Date'] = open_df['Date']
    for i in table_names:
        open_col = 'Open_' + i
        vol_col = 'Volume_' + i
        market_cap[i] = open_df[open_col] * vol_df[vol_col]

    market_cap['total'] = market_cap.iloc[:,1:].sum(axis=1)

    fig1 = px.line(x=market_cap['Date'],y=market_cap['total'],title='Market Cap',labels={'x':'Date','y':'Value'})
    html_fig1 = plot(fig1,output_type='div', include_plotlyjs=False)

    return fig1,html_fig1