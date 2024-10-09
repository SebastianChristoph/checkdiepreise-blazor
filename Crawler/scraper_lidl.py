
import requests
import json
import random
import crawler_handler
import Product

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
list_of_found_products = []

def get_products_from_shop(hits_max = 30000):
    global list_of_found_products
    hits = int(hits_max + random.random() * 2000)

    URL = "https://www.lidl.de/p/api/gridboxes/DE/de/?max="+str(hits)
    s = requests.Session()
    s.headers = headers
    source = s.get(URL, headers = headers).text
    responsedict = json.loads(source)
    
    print("Found", len(responsedict), "products")

    for product in responsedict:
        try:
            identifier = product["productId"]
            name = product["fullTitle"]

            try:
                price = product["price"]["price"]
            except:
                continue

            try:
                if product.get("category") != None:
                    if "/" in product["category"]:
                        category = product["category"].split("/")[1]
                    else:
                        category = product["category"]
                else:
                    category = "Ohne Katgorie"
            except:
                raise Exception("Fehler in Kategorie")
           
            url = "https://www.lidl.de/" + product["canonicalUrl"]

            try:
                if product["price"].get("basePrice") != None:
                    if "=" in product["price"]["basePrice"]:
                        baseprice_split = product["price"]["basePrice"]["text"].split("=")
                        baseprice_unit = baseprice_split[0]
                        baseprice = baseprice_split[1]
                    else:
                        baseprice_unit = product["price"]["basePrice"]["text"]
                        baseprice = price
                else:
                    baseprice_unit = "pro Artikel"
                    baseprice = price
            except Exception as ex:
                raise Exception("Fehler in Baseprice:", ex)

            product_to_add = Product.Product(name, identifier, float(price), float(baseprice), baseprice_unit, "LIDL", category, url)

            if product_to_add not in list_of_found_products:                
                list_of_found_products.append(product_to_add)

        except Exception as e:
            print("error:", e)
            print(product)
            print("_______________________________")
            continue
    
get_products_from_shop()
CrawlerHandler = crawler_handler.Crawler_Handler(list_of_found_products)
CrawlerHandler.handle()