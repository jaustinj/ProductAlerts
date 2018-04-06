import abc
import collections
import re

import pandas as pd

from BaseClasses.Ebayify import add_ebay_link
from BaseClasses.CustomCSS import add_css

class HTMLizer(abc.ABC):
    
    def __init__(self, df):
        self._original_df = df
        self._cols_with_link_text = self._get_convert_dict()
        self.data = self._convert_columns()
        
    def _url_to_link(self, url, link_text):
        return '<a href="{}">{}</a>'.format(url, link_text)
    
    def _convert_columns(self):
        df = self._original_df.copy()
        for col, link_text in self._cols_with_link_text.items():
            df[col] = df[col].apply(lambda x: self._url_to_link(x, link_text))
        return df
    
    def to_html(self, outfile):
        pd.options.display.max_colwidth = 1000
        content_html = self.data.to_html(escape=False, index=False)
        html_with_css = add_css(content=content_html)
        
        with open(outfile, 'w') as file:
            file.write(html_with_css)
        
    
    @abc.abstractmethod
    def _get_convert_dict(self):
        '''Return a dict with:
                key=column name with url to convert
                value=Link text to show up in alert that will take you to URL
                
        return {
            'url': 'See Deal'
        }
        '''