import requests
import json
import mappings
import time
import Product
import crawler_handler

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

list_of_found_products = []
SHOW_PRINTS = True
ITERATE_ONLY_3_TIMES = True

def getting_articles_from_shop(searchterm, page, category): 
    collecting = True
    while collecting:
        URL2 =  f"https://product-search.services.dmtech.com/de/search?query={searchterm}&searchType=product&currentPage={page}&type=search"
        s = requests.Session()
        s.headers = headers
        
        try:
            source = s.get(URL2, headers = headers).text
            response_dict = json.loads(source)

            if SHOW_PRINTS: print("\tfound", len(response_dict["products"]), "products")
            product_count = 0
            
            for product in response_dict["products"]:
                product_count += 1
                try:

                    #price
                    price = product["priceLocalized"].replace("€", "").replace(",",".").strip()
                    price = float(price)


                    # base price
                    if product.get("basePrice") != None:
                        baseprice = product["basePrice"]["formattedValue"].replace("€", "").replace(",",".").strip()
                    else:
                        baseprice = product["priceLocalized"].replace("€", "").replace(",",".").strip()

                    baseprice = float(baseprice)

                    # unit
                    if product.get("basePriceUnit") != None:
                        unit = product["basePriceUnit"]
                    else:
                        unit = "Stk"
                except:
                    if SHOW_PRINTS: 
                        print("******************")
                        print(product)
                        print("*************************")
                        print("error getting price")
                    continue
                    
                product_to_add = Product.Product(product["brandName"] + " - " + product["title"], product["gtin"], price, baseprice, unit, "dm", category, "https://www.dm.de" + product["relativeProductUrl"])

                if product_to_add not in list_of_found_products:
                    list_of_found_products.append(product_to_add)
                
                if ITERATE_ONLY_3_TIMES:
                    if product_count == 3: 
                        collecting = False
            collecting = False
         
        except Exception as e:
            collecting = False
            if SHOW_PRINTS:
                print(source)
                print("error", e)

def main():
    break_seconds = 45
    number_of_requests = 3
    break_counter = 0
    iterations_of_pages = 5        

    for product_to_find, category in mappings.mapping_drogerie.items():
        iteration = 0
        if SHOW_PRINTS:
            print("______________________________________________")
            print(f"Searching products for: {product_to_find} [{category}] [{iteration}/{iterations_of_pages}]")
           
        getting_articles_from_shop(product_to_find, iteration, category)

        if ITERATE_ONLY_3_TIMES:
            break
        else:
            time.sleep(20)
            break_counter += 1

        if break_counter == number_of_requests:
            print("\n******************** Cool down for", break_seconds, "seconds\n")
            time.sleep(break_seconds)
            break_counter = 0

    print("\n\nWait", break_seconds, "seconds...\n")
    CrawlerHandler = crawler_handler.Crawler_Handler(list_of_found_products)
    CrawlerHandler.handle()

main()
