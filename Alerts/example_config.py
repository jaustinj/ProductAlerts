# Config for email
EMAIL_CONFIG = {
    'SEND_FROM': '',
    'SEND_TO': [''],
    'USERNAME': '',
    'PASSWORD': '',
}

# Scraper config for Sierra Trading Post
SIERRA_CONFIG = {
    'SEARCHES': [
                 'oakley sunglasses',
                 'smith optics eyewear',
                 'costa eyewear'
                 ],
    'DELAY_BETWEEN_PAGE_REQUESTS': 5,
    'POSTGRES_BASE_TABLE': 'sierra',
    'POSTGRES_ALERT_TABLE': 'sierra_alerted',
    'POSTGRES_SKU_COLUMN': 'title',
    'THRESHOLD_COLUMN': 'perc_off',
    'THRESHOLD_TYPE': '>=',
    'THRESHOLD': '0.60',
    'OUTPUT_FILE_NAME': 'sierra_alerts',
    'SEARCH_EBAY_COLUMN': 'title',
    'EMAIL_SUBJECT': 'Sierra Deal Alert!'

}

# Scraper config for Backcountry alerts
BACKCOUNTRY_CONFIG = {
    'SEARCHES': [
                 'oakley sunglasses',
                 'smith optics eyewear',
                 'costa eyewear'
                 ],
    'DELAY_BETWEEN_PAGE_REQUESTS': 5,
    'POSTGRES_BASE_TABLE': 'backcountry',
    'POSTGRES_ALERT_TABLE': 'backcountry_alerted',
    'POSTGRES_SKU_COLUMN': 'url',
    'THRESHOLD_COLUMN': 'perc_off',
    'THRESHOLD_TYPE': '>=',
    'THRESHOLD': '60',
    'OUTPUT_FILE_NAME': 'backcountry_alerts',
    'SEARCH_EBAY_COLUMN': 'title',
    'EMAIL_SUBJECT': 'Backcountry Deal Alert!'

}

ALERT_CONFIG = {
    'TIME_BETWEEN_CHECKS': 60*15
}