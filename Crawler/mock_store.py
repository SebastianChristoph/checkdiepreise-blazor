import crawler_handler
import random 
import Product


RANDOM_PRODUCTS = 20

def get_random_product():
    names = [['Product A', 1], ['Product B', 2], ['Product C', 3], ['Product D', 4]]
    stores = ["MOCKSTORE"]
    categories = ['Electronics', 'Books', 'Clothing', 'Food']
    units = ['Liter', 'ml', 'Kilo', 'kg']

    random_product = random.choice(names)
    product_name = random_product[0]
    identifier = random_product[1]
    price = round(random.uniform(10.0, 500.0), 2)  # zufälliger Preis zwischen 10 und 500
    baseprice = round(random.uniform(10.0, 20.0), 2)  # zufälliger Preis zwischen 10 und 500
    baseprice_unit = random.choice(units)
    store = random.choice(stores)
    category = random.choice(categories)
    url ="www.google.com"

    random_product = Product.Product(product_name, identifier, price, baseprice, baseprice_unit, store, category, url)

    return random_product


list_products = []
for i in range(0, RANDOM_PRODUCTS):
    list_products.append(get_random_product())


CrawlerHandler = crawler_handler.Crawler_Handler(list_products)
CrawlerHandler.handle()

