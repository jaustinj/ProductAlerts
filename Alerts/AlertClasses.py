import abc
import collections
import datetime
import functools
import logging
import re
import time

from bs4 import BeautifulSoup
import pandas as pd 
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from AlertingTools import *
from config import *

# SIERRA TRADING POST ALERTS ==================================================
def check_sierra():
    for search in SIERRA_CONFIG['SEARCHES']:
        S = SierraSearch(search, 
                         delay=SIERRA_CONFIG['DELAY_BETWEEN_PAGE_REQUESTS'])
        S.to_postgres('sierra_test_two') # send to posgres table 

        # Uuse SQL to find alerts from table that was just sent to posgres
        alerts_df = CheckDB(table='sierra_test_two',
                            unique_sku='title',
                            threshold_column='perc_off',
                            threshold=SIERRA_CONFIG['THRESHOLD'],
                            eq='>=').alerts


        if len(alerts_df) > 0:

            # Add some special formatting to the alerts and save as html file
            alerts_with_ebay = add_ebay_link(alerts_df, 'title')
            SierraHTMLizer(alerts_with_ebay).to_html('./alert_outputs/sierra_alerts.html')

            # Send email with html file output
            for email in EMAIL_CONFIG['SEND_TO']:
                send_alert(send_from=EMAIL_CONFIG['SEND_FROM'], 
                           send_to=email, 
                           username=EMAIL_CONFIG['USERNAME'], 
                           password=EMAIL_CONFIG['PASSWORD'],
                           subject=EMAIL_CONFIG['SUBJECT'], 
                           message='New Alerts, Download Below', 
                           file='./alert_outputs/sierra_alerts.html' 
                           )

            to_postgres(alerts_df, 'sierra_test_two_alerted')

