import abc
import collections
import datetime
import functools
import logging
from pprint import pprint
import re
import time

from bs4 import BeautifulSoup
import requests

from SierraClasses import SierraSearch

logging.basicConfig(filename='log.log',level=logging.INFO)

S = SierraSearch('oakley sunglasses')
pprint(S)

S = SierraSearch('cargo pants')
pprint(S)

S = SierraSearch('jumper')
pprint(S)

S = SierraSearch('ekalekjaf')
pprint(S)