import pandas as pd 
from sqlalchemy import create_engine

def to_postgres(df, table):  
    engine = create_engine('postgresql://docker:docker@postgres:5432/docker')
    df.to_sql(table, engine, if_exists='append')