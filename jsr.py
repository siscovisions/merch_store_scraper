import requests
from bs4 import BeautifulSoup
import pandas as pd

# Assign the headers

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://google.com',
        'DNT': '1',
    }

### MAIN COLLECTIONS PAGE ###

baseurl = 'https://jsrdirect.com'

bandlinks = []

r = requests.get('https://jsrdirect.com/collections')
soup = BeautifulSoup(r.content, 'html.parser')
bands = soup.find_all('li', class_='collection-list__item grid__item')

for band in bands:
    for link in band.find_all('a', href=True):
        bandlinks.append(baseurl + link['href'])

### ACCESS INDIVIDUAL BAND PAGES AND GET ITEM LINKS ###

banditemslist = []

for band in bandlinks:
    r = requests.get(band, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all('div', class_='card-wrapper')
    for item in productlist:
        for link in item.find_all('a', href=True):
            banditemslist.append(band + link['href'])


### GET INFO FOR EACH ITEM FROM EACH BAND PAGE ###

individualitems = []

for item in banditemslist:
    r = requests.get(item, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'lxml')
    name = soup.find('h1', class_='product__title').text.strip()
    price = soup.find('span', class_ = 'price-item price-item--regular').text.strip()

    merch_list = {
        'name': name,
        'price': price,
        'link': item
    }

    individualitems.append(merch_list)

# Send the data into an organized dataframe using Pandas and save as a CSV file

df = pd.DataFrame(individualitems)
df.to_csv('jsr_direct.csv', index=False)