import crawler_handler
from bs4 import BeautifulSoup
import requests
import Product

SHOW_PRINTS = True

categories = {}
list_of_found_products = []

URL = "https://www.lego.com/de-de"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}


def get_category_sites():
    s = requests.Session()
    s.headers = headers
    source = s.get(URL, headers = headers).text
    soup = BeautifulSoup(source, "lxml")

    anchors = soup.find_all("a", class_ = "Linksstyles__Anchor-sc-684acv-0")
    for anchor in anchors:
        if "themes" not in anchor.get("href"):
            continue
        else:
            categories[anchor.text] = {"url" : "https://www.lego.com" +anchor.get("href"), "category" :  anchor.get("href").split("/")[-1].replace("-", " ").title()}

def get_site_pages(url):
    s = requests.Session()
    s.headers = headers
    source = s.get(url, headers = headers).text
    soup = BeautifulSoup(source, "lxml")

    max_products = 0
    product_amount = soup.find_all("span", class_ = "Text__BaseText-sc-13i1y3k-0")
    for span in product_amount:
        if span.get("data-test") == "result-count":
            max_products = int(span.get("data-value"))
            break

    pages = max_products // 18
    if max_products % 18 != 0:
        pages += 1

    return pages

def get_products_from_site(url, category):

    if SHOW_PRINTS:
        print("#####################################################################")
        print("Get product infos for", category)
    pages = get_site_pages(url)

    if pages == None:
        return


    for i in range(1, pages+1):
        if SHOW_PRINTS:
            print(f"_______________page {i}_______________________")
        url_to_scrape = f"{url}?page={i}"
        if SHOW_PRINTS:
            print(url_to_scrape)

        try:
            s = requests.Session()
            s.headers = headers
            source = s.get(url_to_scrape, headers = headers).text
            soup = BeautifulSoup(source, "lxml")
            product_wrappers = soup.find_all("li", class_ = "Grid_grid-item__FLJlN")


            for product_wrapper in product_wrappers:
                if product_wrapper.get("data-test") != "product-item":
                    continue

                # name, identifier and link
                possible_titles = product_wrapper.find_all("a", class_="ds-body-md-medium")
                identifier = None

                for possible_title in possible_titles:
                    if possible_title.get("data-test") == "product-leaf-title":
                        try:
                                title = possible_title.text
                                original_link = "https://www.lego.com" +possible_title.get("href")
                                identifier = original_link.split("-")[-1]
                                break
                        except:
                            continue
                if identifier == None:
                    continue

                #price_unit
                price_unit = product_wrapper.find("span", class_ ="price-sm-bold")
                if price_unit != None:
                    price_unit = price_unit.text.replace("€", "").replace(",", ".")
                else:
                    continue

                # baseprice
                pieces = 0
                possible_baseprices = product_wrapper.find_all("span", class_= "ds-label-sm-medium")
                for possible_baseprice in possible_baseprices:
                    if possible_baseprice.get("data-test") == "product-leaf-piece-count-label":
                        pieces = possible_baseprice.text
                        break
                
                if pieces == 0:
                    baseprice = price_unit
                    unit_name = "€ pro Artikel"
                else:
                    baseprice = round(float(price_unit) / float(pieces), 2)
                    unit_name = "€ pro Artikel"

                
                product = Product.Product(title, identifier, price_unit, unit_name, baseprice, "€ pro Stein", "LEGO", category, original_link)
          
                if product not in list_of_found_products:
                        if SHOW_PRINTS:
                            print(identifier, title, category)
                        list_of_found_products.append(product)
        except Exception as e:
            print("error getting page products", e)
    
def get_products_from_shop():
    current = 1
    get_category_sites()
    iteration = 0
    for category_site in categories:
        current += 1
        if "?" in categories[category_site]["url"]:
            continue

        get_products_from_site(categories[category_site]["url"], categories[category_site]["category"])

        iteration += 1
        if iteration == 3:
            break
    


get_products_from_shop()
CrawlerHandler = crawler_handler.Crawler_Handler(list_of_found_products)
CrawlerHandler.handle()