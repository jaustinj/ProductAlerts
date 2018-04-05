from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
import pandas as pd

engine = create_engine('postgresql://docker:docker@postgres:5432/docker')


check_for_alerts_table = '''
                            SELECT EXISTS (
                                SELECT 
                                    1
                                FROM
                                    testdb
                            );
                        '''
                

try:
    df = pd.read_sql_query(check_for_alerts_table, con=engine)
    print(df)
except ProgrammingError:
    print('Disaster Averted')



# df = pd.DataFrame({'Col1': [1,2,3,4,5], 'Col2': [1,2,3,4,5]})
# df.to_sql('test', engine, if_exists='append')