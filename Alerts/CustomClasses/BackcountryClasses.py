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

class BackcountryProduct(Product):
    
    @ScraperMixIn.log(before_text='Parsing Product HTML', 
                      after_text='Product HTML finished Parsing')
    def _parse_html(self, tag):
        '''Parses values out of tag, one function for each
        value parsed'''
        
        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _brand(tag):
            return tag.find('span',
                           {'class': 'ui-pl-name-brand'}
                           ).text.strip()

        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _url(tag):
            url_end = tag.find('a',
                               {'class': 'ui-pl-link'}
                               )['href']
            return 'https://www.backcountry.com' + url_end
        
        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _title(tag):
            return tag.find('span', {'class': 'ui-pl-name-title'}).text.strip()
        
        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _low_price(tag):
            if tag.find('span', {'class': 'ui-pl-pricing-low-price'}):
                price_str = tag.find('span', {'class': 'ui-pl-pricing-low-price'}).text.strip()
            else:
                price_str = tag.find('span', {'class': 'ui-pl-pricing-high-price'}).text.strip()
            return float(price_str.replace('$', '').replace(',',''))
        
        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _high_price(tag):
            price_str = price_str = tag.find('span', {'class': 'ui-pl-pricing-high-price'}).text.strip()
            return float(price_str.replace('$', '').replace(',',''))

        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _sale(tag):
            if tag.find('div', {'class': 'ui-pl-offers--discounted'}):
                return 'Sale'
            else:
                return 'Price Range'
            
        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _price_text(tag):
            return tag.find('div', {'class': 'ui-pl-offers'}).text.strip()

        @ScraperMixIn.log(log_return=True)
        @ScraperMixIn.default_value(None)
        def _perc_off(tag):
            perc_off = tag.find('span', {'class': 'discount-amount-text'}).text.strip()
            return float(perc_off.replace('%', ''))

        
        data = {}
        
        data['brand'] = _brand(tag)
        data['url'] = _url(tag)
        data['title'] = _title(tag)
        data['low_price'] = _low_price(tag)
        data['high_price'] = _high_price(tag)
        data['price_text'] = _price_text(tag)
        data['type'] = _sale(tag)
        data['perc_off'] = _perc_off(tag)
        
        return data


class BackcountryPage(Page):
    
    @ScraperMixIn.log(before_text='Selecting ProductClass for Page to use')
    def _select_product_class(self):
        return BackcountryProduct
    
    @ScraperMixIn.log(before_text='Finding List of Product HTMLs in PageObject',
                      after_text='List of Product HTMLs Found')
    def _parse_html(self, tag):
        return tag.findAll('div', {'class': 'product'})


class BackcountrySearch(Search):

    @ScraperMixIn.log(log_call=True, log_return=True)
    def _search_url(self, search_string):
        '''Takes a search string and returns the url for
        the search on the website.
        
        Example:
        'oakley sunglasses' -> https://www.6pm.com/q?=oakley-sunglasses
        '''
        base_url = 'https://www.backcountry.com/Store/catalog/search.jsp?s=u&q={}'
        ammended_string = search_string.lower().replace(' ', '+')
        
        return base_url.format(ammended_string)
    
    @ScraperMixIn.log(before_text='Selecting PageClass for Search to use')
    def _select_page_class(self):
        '''Return the Page Class used to parse pages.
        i.e.: return MyPageParser'''
        return BackcountryPage

    @ScraperMixIn.log(log_return=True)
    def _find_next_page_url(self, soup):
        '''Given a search result page of html, find if there 
        is pagination (more results on other pages), and if so, return the 
        url of the next page, if not, return Null. Can also return a list
        of all urls in pagination.'''
        
        last_page = soup.find('a', {'rel': 'nofollow'}, text='Next Page')
        
        if last_page:
            return 'https://www.backcountry.com{}'.format(last_page['href'])
        
        else:
            return None


# SETUP HTML ALERT FILE =======================================================
class BackcountryHTMLizer(HTMLizer):
    def _get_convert_dict(self):
        return {
            'url': 'See Deal',
            'ebay': 'See Sold on Ebay'
        }