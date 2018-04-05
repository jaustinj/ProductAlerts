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

logging.basicConfig(filename='./logs/alerts.log',level=logging.DEBUG)

SierraSearch('womens coats').to_postgres('womens_coats_test')
alerts_df = CheckDB(table='womens_coats_test',
                    unique_sku='title',
                    threshold_column='perc_off',
                    threshold='0.60',
                    eq='>=').alerts

alerts_with_ebay = add_ebay_link(alerts_df)
SierraHTMLizer(alerts_with_ebay).to_html('./alert_outputs/sierra_alerts.html')
send_alert(send_from, 
           send_to, 
           username, 
           password,
           subject='Sierra Alert!', 
           message='New Alerts, Download Below', 
           file='./alert_outputs/sierra_alerts.html' 
           )

