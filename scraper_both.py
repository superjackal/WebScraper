import requests
from bs4 import BeautifulSoup
import datetime


def FlipkartScraper(search):
    url = "https://www.flipkart.com/search?q="
    url += search

    items = []
    markup = requests.get(url).text
    soup = BeautifulSoup(markup, 'html.parser')

    item_class_list = ["_3pLy-c row","_4ddWXP","_2B099V"]

    # Assigns title class and price class according to the item class
    title_class = {"_3pLy-c row":"_4rR01T", "_4ddWXP":"s1Q9rs", "_2B099V":"IRpwTa"}
    price_class = {"_3pLy-c row":"_30jeq3 _1_WHN1", "_4ddWXP":"_30jeq3", "_2B099V":"_30jeq3"}

    # Finds the correct class for each item present in the page
    for item in item_class_list:
        page = soup.find_all(attrs={'class':item})
        if(page):
            item_class = item
            break

    review_class = "_3LWZlK"
    reviewno_class = "_2_R_DZ"


    for page in range(1,6):
        markup = requests.get(f'https://www.flipkart.com/search?q={search}&page={page}').text
        soup = BeautifulSoup(markup, 'html.parser')
        for row in soup.find_all(attrs={'class':item_class}):
            item = {}
            item['name'] = row.find(attrs={'class':title_class[item_class]}).get_text()
            item['price'] = row.find(attrs={'class':price_class[item_class]}).get_text()
            try:
                item['review'] = row.find(attrs={'class':review_class}).get_text()
                item['review_number'] = row.find(attrs={'class':reviewno_class}).get_text()
            except:
                item['review'] = ""
                item['review_number'] = ""
            item['Timestamp'] = datetime.datetime.now()
            items.append(item)


    from pymongo import MongoClient
    ConnectionString = ""
    client = MongoClient(ConnectionString)
    db = client.flipkart.items
    db.insert_many(items)
    client.close()

    print("Stored")
    print(f'inserted {len(items)} items')
    return items
