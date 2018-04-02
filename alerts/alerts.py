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

from AlertingTools import SierraSearch, CheckDB

SierraSearch('womens coats').to_postgres('womens_coats_test')
alerts_df = CheckDB(table='womens_coats_test',
                    unique_sku='title',
                    threshold_column='perc_off',
                    threshold='0.60',
                    eq='>=').alerts

print(alerts_df)

