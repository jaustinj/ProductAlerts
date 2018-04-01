from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://docker:docker@postgres:5432/docker')

df = pd.DataFrame({'Col1': [1,2,3,4,5], 'Col2': [1,2,3,4,5]})
df.to_sql('test', engine, if_exists='append')