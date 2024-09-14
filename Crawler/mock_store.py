import crawler_handler
import random 
import Product

RANDOM_PRODUCTS = 100

def get_random_product():
    names = [['Product A', 1], ['Product B', 2], ['Product C', 3], ['Product D', 4]]
    stores = ["LIDL", "ALDI"]
    categories = ['Electronics', 'Books', 'Clothing', 'Food']

    random_product = random.choice(names)
    product_name = random_product[0]
    identifier = random_product[1]
    price_unit = round(random.uniform(10.0, 500.0), 2)  # zufälliger Preis zwischen 10 und 500
    unit_name ="Stk"
    price_bulk = round(random.uniform(10.0, 500.0), 2)  # zufälliger Preis zwischen 10 und 500
    bulk_unit_name ="Liter"
    store = random.choice(stores)
    category = random.choice(categories)
    url ="www.cool.com"

    random_product = Product.Product(product_name, identifier, price_unit, unit_name, price_bulk, bulk_unit_name, store, category, url)

    return random_product


list_products = []
for i in range(0, RANDOM_PRODUCTS):
    list_products.append(get_random_product())


CrawlerHandler = crawler_handler.Crawler_Handler(list_products)
CrawlerHandler.handle()

