import psycopg2 as pg
import pandas as pd
from sqlalchemy import create_engine

df = pd.read_excel(r'C:\temp\backup\test\bot_adpu\sim10.xlsx', sheet_name='Лист1', index_col=0)
print(df)

conn_string = 'postgresql://postgres:1234@localhost:5432/bot_adpu'
  
db = create_engine(conn_string) 
conn = db.connect() 

df.to_sql('simcards', con=conn, if_exists='append', index=False) 
  
conn.commit() 
conn.close() 
