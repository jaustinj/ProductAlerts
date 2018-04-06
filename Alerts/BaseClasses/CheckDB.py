import abc

import pandas as pd 
from sqlalchemy import create_engine 
from sqlalchemy.exc import ProgrammingError


class CheckDB():

    ENGINE = create_engine('postgresql://docker:docker@postgres:5432/docker')

    def __init__(self, table, alert_table, unique_sku, threshold_column, threshold, eq='>='):
        self._table = table
        self._alert_table = alert_table
        self._sku = unique_sku # column name that is unique to product
        self._col = threshold_column
        self._eq = eq
        self._threshold = threshold
        self.alerts = self._find_alerts()


    def _check_for_alerts_table(self):
        check_for_alerts_table = '''
            SELECT EXISTS (
                SELECT 
                    1
                FROM
                    {alert_table}
            );
            '''.format(alert_table=self._alert_table)

        try:
            df = pd.read_sql_query(check_for_alerts_table, con=CheckDB.ENGINE)
            return True

        except ProgrammingError:
            return False

    def _alerts_query(self):

        previous_alerts = self._check_for_alerts_table()
        if previous_alerts:
            # Query to make sure we don't send more than one alert per day
            query = '''
                SELECT
                    above_threshold.*
                FROM (
                    SELECT 
                        *
                    FROM 
                        {table}
                    WHERE 
                        {col} {equality} {threshold}
                        AND ts = (SELECT MAX(ts) FROM {table})
                ) above_threshold

                LEFT OUTER JOIN (
                    SELECT
                        *
                    FROM 
                        {alert_table}
                    WHERE
                        ds = (SELECT MAX(ds) FROM {table})
                ) already_alerted_today

                ON above_threshold.{unique_sku} = already_alerted_today.{unique_sku}
                AND above_threshold.ds = already_alerted_today.ds

                WHERE
                    already_alerted_today.{unique_sku} IS NULL ;
            '''.format(
                    table=self._table,
                    alert_table=self._alert_table,
                    col=self._col,
                    equality=self._eq,
                    threshold=self._threshold,
                    unique_sku=self._sku
                )
        else:
            # If no alerts table, don't have to worry about previous alerts
            query = '''
                SELECT 
                    *
                FROM 
                    {table}
                WHERE 
                    {col} {equality} {threshold}
                    AND ts = (SELECT MAX(ts) FROM {table})
            '''.format(
                    table=self._table,
                    col=self._col,
                    equality=self._eq,
                    threshold=self._threshold
                )

        return query 

    def _find_alerts(self):
        query = self._alerts_query()
        df = pd.read_sql_query(query, con=CheckDB.ENGINE)

        return df


                    