from bs4 import BeautifulSoup
import requests
import re
import crawler_handler
import Product


URL = "https://www.hellweg.de"
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

list_of_found_products = []
categories = {}
ONLY_ITERATE_3_TIMES = False
ONLY_ITERATE_3_PRODUCTS = False

def clean_price(price) -> float:

    cleaned_str = re.sub(r'[^0-9.]', '', price)
    return float(cleaned_str)

def get_products_from_shop():
    source = requests.get(URL, headers = headers).text
    soup = BeautifulSoup(source, "lxml")
    # with open("testi.html", "w", encoding="UTF-8") as file:
    #         file.write(soup.prettify())
    #         print("testi.html")
    category_urls = soup.find_all("a", class_ = "js-navigation-offcanvas-link")

    # Main Categories
    for category in category_urls:
        category_url = category.get("href")
        category_name = category.text.strip()
        print(category_url)

        #Get Max Page
        source = requests.get(category_url, headers = headers).text
        soup = BeautifulSoup(source, "lxml")
        last_page_li = soup.find_all("li", class_ = "page-item page-last")
        last_page = 1
        if len(last_page_li)> 0:
            input_tag = last_page_li[0].find("input", type="radio")
            last_page = int(input_tag.get('value'))
            #print("     Last Page: ", last_page)

        for page in range(1, last_page):
            # print(f"    Page {page} of {last_page}")
            url_for_page = f"{category_url}?order=relevance&p={page}"
            print(f"{url_for_page} | {last_page}")

            source = requests.get(url_for_page, headers = headers).text
            soup = BeautifulSoup(source, "lxml")
            # with open("testi1.html", "w", encoding="UTF-8") as file:
            #     file.write(soup.prettify())
            #     print("testi1.html")

            product_wrappers = soup.find_all("div", class_="cms-listing-col")
            iteration = 0
            for product_wrapper in product_wrappers:
                # with open("testi2.html", "w", encoding="UTF-8") as file:
                #     file.write(product_wrapper.prettify())
                #     print("testi2.html")
                url = ""
                identifier = ""
                name = ""
                
                # url & identifier
                try:
                    url_wrapper = product_wrapper.find("a", class_="product-link")
                    if url_wrapper: 
                        url = url_wrapper.get("href")
                    else:
                        url_wrapper = product_wrapper.find("a", class_="product-name")
                        if url_wrapper: 
                            url = url_wrapper.get("href")
                    

                    identifier = url.split("-")[-1]

                except Exception as e: 
                    print("no id or url, skip: ", e)
                    continue
                    
                # name
                try:
                    name = product_wrapper.find("a", class_="product-name").text
                    name = name.strip()
                except Exception as e: 
                    print("no name, skip", e)
                    continue

                # price
                try:
                    price_discount = product_wrapper.find("span", class_="highlight-price")

                    if price_discount != None:
                        price = price_discount.text
                        price = clean_price(price)
                    else:
                        price = product_wrapper.find("span", class_="default-price").text
                        price = clean_price(price)


                except Exception as e: 
                    print("no name, skip", e)
                    continue

                try:
                    baseprice_info = product_wrapper.find("span", class_="price-unit-reference")

                    if baseprice_info:
                        baseprice_info_text = baseprice_info.text
                        baseprice_info_data = baseprice_info_text.split("/")
                        baseprice = baseprice_info_data[0]
                        baseprice = clean_price(baseprice)
                        baseprice_unit = baseprice_info_data[1]

                        baseprice_unit = baseprice_unit.strip()
                        baseprice_unit = baseprice_unit.replace("\n", "")

                    else:
                        baseprice_unit = product_wrapper.find("span", class_="price-unit-content").text
                        baseprice_unit = baseprice_unit.strip()
                        baseprice_unit = baseprice_unit.replace("\n", "")
                        baseprice = price

                except Exception as e: 
                    print("no baseprice_unit", e)
                    baseprice = price
                    baseprice_unit = "Stk"

                product_to_add = Product.Product(name, identifier, price, baseprice, baseprice_unit, "Hellweg", category_name, url)

                if product_to_add not in list_of_found_products:
                    list_of_found_products.append(product_to_add)
                
                if ONLY_ITERATE_3_PRODUCTS:
                    iteration += 1

                    if iteration == 3:
                        break

            
            if ONLY_ITERATE_3_TIMES or ONLY_ITERATE_3_PRODUCTS:
                break
        if ONLY_ITERATE_3_TIMES:
            break

get_products_from_shop()
if ONLY_ITERATE_3_TIMES == False:
    CrawlerHandler = crawler_handler.Crawler_Handler(list_of_found_products)
    CrawlerHandler.handle()