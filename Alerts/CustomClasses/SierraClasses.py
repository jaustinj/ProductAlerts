import abc
import collections
import datetime
import logging
import re
import time

from bs4 import BeautifulSoup
import requests

from BaseClasses.AbstractScrapingClasses import *
from BaseClasses.Alerts2HTML import HTMLizer

# SCRAPER CLASSES =============================================================

class SierraProduct(Product):
    
    @ScraperMixIn.log(before_text='Parsing Product HTML', 
                      after_text='Product HTML finished Parsing')
    def _parse_html(self, tag):
        '''Parses values out of tag, one function for each
        value parsed'''
        
        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _brand(tag):
            return tag.find('a',
                           {'class': re.compile('^productCard-title.*')}
                           ).text.strip()

        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _url(tag):
            url_end = tag.find('a',
                               {'class': re.compile('^productCard-title.*')}
                               )['href']
            return 'https://www.sierratradingpost.com' + url_end
        
        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _title(tag):
            return tag.find('a',
                           {'class': re.compile('^display-block.*')}
                           ).text.strip()
        
        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _price(tag):
            price_str = tag.find('span', {'class': 'ourPrice'}).text.strip()
            return float(price_str.replace('$', '').replace(',',''))
        
        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _msrp(tag):
            msrp_str = tag.find('span', 
                                 {'class': re.compile('^retailPrice.*')}
                                ).text.strip()
            msrp = re.search('\d{0,3},?\d{1,3}\.\d{2}', msrp_str).group()
            return float(msrp.replace(',',''))

        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _colors(tag):
            # Find the list of swatches
            swatches = tag.find(
                'ul', {'class': 'swatches'}
            ).findAll(
                'li', {'class': 'swatch'}
            )

            # Get the color out of the data-colorchip-name attribute in swatches
            colors = [
                s.find('div', {'class': 'colorChipLinkContainer'})['data-colorchip-name'] 
                for s in swatches
            ]

            # Clean up the color names
            c = [re.sub('\(\d{1,3}\)', '', color).strip() for color in colors]

            return ', '.join(c)

        @ScraperMixIn.log(after_text='Deriving Percent Off', log_return=True)
        def _perc_off(data):
            if data['msrp']:
                perc_off = (data['msrp'] - data['price']) / data['msrp']
                perc_off = round(perc_off, 2)
            else:
                perc_off = None

            return perc_off 

        
        data = {}
        
        data['brand'] = _brand(tag)
        data['url'] = _url(tag)
        data['title'] = _title(tag)
        data['price'] = _price(tag)
        data['msrp'] = _msrp(tag)
        data['colors'] = _colors(tag)
        data['perc_off'] = _perc_off(data)
        
        return data


class SierraPage(Page):
    
    @ScraperMixIn.log(before_text='Selecting ProductClass for Page to use')
    def _select_product_class(self):
        return SierraProduct
    
    @ScraperMixIn.log(before_text='Finding List of Product HTMLs in PageObject',
                      after_text='List of Product HTMLs Found')
    def _parse_html(self, tag):
        return tag.findAll('div', {'class': re.compile('^productThumbnailContainer.*')})


class SierraSearch(Search):

    @ScraperMixIn.log(log_call=True, log_return=True)
    def _search_url(self, search_string):
        '''Takes a search string and returns the url for
        the search on the website.
        
        Example:
        'oakley sunglasses' -> https://www.6pm.com/q?=oakley-sunglasses
        '''
        base_url = 'https://www.sierratradingpost.com/s~{}/'
        ammended_string = search_string.lower().replace(' ', '-')
        
        return base_url.format(ammended_string)
    
    @ScraperMixIn.log(before_text='Selecting PageClass for Search to use')
    def _select_page_class(self):
        '''Return the Page Class used to parse pages.
        i.e.: return MyPageParser'''
        return SierraPage

    @ScraperMixIn.log(log_return=True)
    def _find_next_page_url(self, soup):
        '''Given a search result page of html, find if there 
        is pagination (more results on other pages), and if so, return the 
        url of the next page, if not, return Null. Can also return a list
        of all urls in pagination.'''
        
        last_page = soup.findAll('a', 
                                 {'class': re.compile('^pageLink.*'), 
                                  'class': 'lastPage'}
                                )
        
        if last_page:
            href = last_page[0]['href']
            last_page_number = int(re.search('\d{1,3}', href).group())
            urls = [self.url + str(i) + '/' for i in range(2, last_page_number + 1)]
        
            return urls
        
        else:
            return None


# SETUP HTML ALERT FILE =======================================================
class SierraHTMLizer(HTMLizer):
    def _get_convert_dict(self):
        return {
            'url': 'See Deal',
            'ebay': 'See Sold on Ebay'
        }