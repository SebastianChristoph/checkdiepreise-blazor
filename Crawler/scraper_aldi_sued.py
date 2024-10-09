from bs4 import BeautifulSoup
import requests
import re
import crawler_handler
import Product

URL = "https://www.aldi-sued.de/de/produkte/produktsortiment/kuehlung-und-tiefkuehlkost.html?sort=recommended"
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

list_of_found_products = []
categories = {}
current = 0

SHOW_PRINTS = True
ONLY_ITERATE_3_TIMES = False

def clean_category_name(input_string):
    input_string = input_string.replace("-", " ")
    words = input_string.split()

    for i, word in enumerate(words):
        if word.lower() != "und":
            words[i] = word.capitalize()

    output_string = " ".join(words)

    return output_string

def get_categories_produktsortiment():
    global categories
    URL = "https://www.aldi-sued.de/de/produkte/produktsortiment.html"
    source = requests.get(URL, headers = headers).text
    soup = BeautifulSoup(source, "lxml")

    sub_categories_wrappers = soup.find_all("div", class_ = "E05-basic-text")
 
    for sub_category_wrapper in sub_categories_wrappers:
        sub_categories = sub_category_wrapper.find_all("a", class_ ="btn-secondary")

        for sub_category in sub_categories:

            try:
                cat = sub_category.text.strip()
                url = sub_category.get("href")
                main_category = url.split("/")[-2]

                main_category = clean_category_name(main_category)
                categories[cat] = {
                    "url" : url,
                    "main_category" : main_category
                }

            except:
                continue
    
def get_categories_eigenmarken():
    if SHOW_PRINTS: print("Get Eigenmarken")
    global categories
    eigenmarken_url = "https://www.aldi-sued.de/de/produkte/eigenmarken.html"
    source = requests.get(eigenmarken_url, headers = headers).text
    soup = BeautifulSoup(source, "lxml")

    marken_liste = soup.find_all("div", class_ ="E02-text-html")

    for eigenmarke in marken_liste:
       
        try:
            markenlink = eigenmarke.find("a", class_ ="btn").get("href")

            if "#" in markenlink:
                continue
            markenname = eigenmarke.text.strip()
            categories[markenname] = {
                "url" : markenlink,
                "main_category" : "Eigenmarke"
            }
        except:
            continue

def get_category_links():
    get_categories_eigenmarken()
    get_categories_produktsortiment()
    
def clean_baseprice(input_string):

    match = re.search(r'\((.*?)\)', input_string)
    if match:
        extracted_text = match.group(1)
        return extracted_text.strip()

    return input_string

def getting_articles_from_shop(category, cat_url, cat_main_name, show_product_to_search = False): 
    amount_products = 0
    global list_of_found_products 
    source = requests.get(URL, headers = headers).text
    soup = BeautifulSoup(source, "lxml")

    # max products
    product_amount_wrapper = soup.find("span", class_ = "plp_count").text.strip()
    product_amounts = re.findall(r'\d+', product_amount_wrapper)
    if product_amounts:
        amount_products = int(product_amounts[0])
        max_pages = amount_products // 18
        if amount_products % 18 != 0:
            max_pages += 1

    #maxPages auf 1, weil noch keine Möglichkeit "load more" zu aktivieren
    if SHOW_PRINTS: print("Crawl for category:", category, "[", current, "of", len(categories), "]")
    
    max_pages = 1
    for page in range(1, max_pages+1):
       
        if "www.aldi" in cat_url:
            url = f"{cat_url}"
        else:
            url = f"https://www.aldi-sued.de{cat_url}?sort=name-asc&page={page}"
        if SHOW_PRINTS:
            print(cat_url)
            print("********************")
        source = requests.get(url, headers = headers).text
        soup = BeautifulSoup(source, "lxml")
        list_products = soup.find_all("article", class_ = "wrapper")

        try:
            for product in list_products:

                # original_link
                original_link_wrapper = product.find("a")
                url = "https://www.aldi-sued.de" + original_link_wrapper.get("href").strip()


                ##price 
                price = product.find("span", class_ = "price").text.replace("€", "").replace(",", ".").strip()
                baseprice_unit = "Stk"

                baseprice = product.find("span", class_ ="additional-product-info").text.strip()

                if baseprice != None:
                    baseprice =  re.sub(r'\s+', ' ', baseprice)
                    baseprice = clean_baseprice(baseprice)
                    if "=" in baseprice:
                        baseprice_split = baseprice.split("=")
                        baseprice_unit = baseprice_split[0].replace("(","")
                        baseprice = baseprice_split[1].replace(")", "").replace("€", "").replace(",",".").strip()
                    else:
                        baseprice_unit = baseprice
                        baseprice_unit = clean_baseprice(baseprice_unit)
                        baseprice = price
                
                if "1 je" in baseprice_unit:
                    baseprice_unit = "Stk"

                # name
                name = product.find("h2", class_ ="product-title").text.strip()  

                try:
                   #ID
                    image_wrapper = product.find("img", class_ = "at-product-images_img")
                    imageURL = image_wrapper.get("data-src")
                    identifier = imageURL.split("/")[-1]
                except:
                    continue   
                
                if SHOW_PRINTS == False:
                    print(".", end="")
                product_to_add = Product.Product(name, identifier, float(price), float(baseprice), baseprice_unit, "ALDI SUED", cat_main_name, url)
               
                if product_to_add not in list_of_found_products:
                    list_of_found_products.append(product_to_add)
        except Exception as e:
            print(e)
            continue

  
def get_products_from_shop():
    global categories, current
    get_category_links()
    iteration = 0
    for category in categories:
        if SHOW_PRINTS: print("Getting products for", category)
        current += 1
        getting_articles_from_shop(category, categories[category]["url"], categories[category]["main_category"])

        if ONLY_ITERATE_3_TIMES:
            iteration += 1
            if iteration == 3:
                break

    print("Finished")
    
get_products_from_shop()
CrawlerHandler = crawler_handler.Crawler_Handler(list_of_found_products)
CrawlerHandler.handle()