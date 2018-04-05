import re

def add_ebay_link(df, title):

    def ebay_ify(title):
        ebay_url = 'https://www.ebay.com/sch/i.html?_nkw={search}&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&_samilow=&_samihi=&_sadis=15&_stpos=95051&_sargn=-1%26saslc%3D1&_salic=1&_sop=12&_dmd=1&_ipg=50&LH_Complete=1'
        
        title1 = title.replace('-', '')
        title2 = re.sub('\s+', ' ', title1)
        title3 = title2.replace(' ', '+')
        title4 = title3.replace('®', '')
        
        return ebay_url.format(search=title4)

    new_df = df.copy()
    new_df['ebay'] = new_df[title].apply(lambda x: ebay_ify(x))

    return new_df