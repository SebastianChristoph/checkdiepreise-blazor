from bs4 import BeautifulSoup
import requests
import re
import crawler_handler
import Product
import json

URL = "https://www.shop-apotheke.com/hautallergie/?pageNumber=1&hitsPerPage=50"
URL2 = "https://www.shop-apotheke.com/allergie/"
headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

categories = []
used_ids = []
list_of_found_products = []

SHOW_PRINTS = True
ONLY_ITERATE_3_TIMES = False
ONY_FIND_3_PRODUCTS = False

def extract_numbers_from_string(input_string):
    # Verwendet reguläre Ausdrücke, um alle Zahlen im String zu finden
    numbers = re.findall(r'\d+', input_string)
    return [int(number) for number in numbers]

def get_first_categories():
    global categories
    url_for_first_categories = "https://www.shop-apotheke.com/asthma/"
    source = requests.get(url_for_first_categories, headers=headers).text
    soup = BeautifulSoup(source, "lxml")

    script_tag = soup.find_all('script', class_='preloaded-state-template')
    script_content = script_tag[-1].string.strip()
    start = script_content.find("publicRuntimeConfig")

    last_brace_index = script_content.rfind("}")
    if last_brace_index != -1:
        remaining_string = script_content[:last_brace_index]
        second_last_brace_index = remaining_string.rfind("}")

    dicti = json.loads(script_content[start-2:second_last_brace_index+1])
    counter_main = 0
    for main_category in dicti["publicRuntimeConfig"]["publicConfig"]["safeFooterCategories"]:
        counter_main += 1
        main_category_name = main_category["title"]

        print(f"+++++ MAIN: {main_category_name} ({counter_main} of {len(dicti["publicRuntimeConfig"]["publicConfig"]["safeFooterCategories"])})")
        counter_second = 0
        for first_category in main_category["links"]:
            counter_second += 1
            url = "https://www.shop-apotheke.com" + first_category["href"]
            get_second_categories(url, main_category_name)
            if ONY_FIND_3_PRODUCTS:
                if counter_second == 3: 
                    break
        if ONY_FIND_3_PRODUCTS:
            if counter_main == 1: 
                break

def get_second_categories(url_first_category, main_category_name):
    global categories
    source = requests.get(url_first_category, headers=headers).text
    soup = BeautifulSoup(source, "lxml")

    subcategories = soup.find_all("li", class_="o-CmsNavigationList__item")

    if SHOW_PRINTS:
        print("  ", url_first_category)
        print("            get seconds & thirds")
    
    counter_second = 0
    for subcategory in subcategories:
        counter_second += 1
        url = "https://www.shop-apotheke.com" + subcategory.find("a").get("href")
        if SHOW_PRINTS: print(f"            {url}")
        get_third_categories(url, main_category_name)
        if ONY_FIND_3_PRODUCTS:
            if counter_second == 3: 
                break

def get_third_categories(url_second_category, main_category_name):
    global categories

    source = requests.get(url_second_category, headers=headers).text
    soup = BeautifulSoup(source, "lxml")
    third_subcategories = soup.find_all(
        "ul", class_="o-CmsNavigationList__secondaryNavTree__list")

    if len(third_subcategories) > 0:
        counter_third = 0
        for third_subcategory_list in third_subcategories:
            counter_third += 1
            third_categories_lis = third_subcategory_list.find_all(
                "li", class_="o-CmsNavigationList__item")

            for third_category_li in third_categories_lis:
                if SHOW_PRINTS: print(f'                     {third_category_li.find("a").get("href")}')
                categories.append({"url": "https://www.shop-apotheke.com" +
                                  third_category_li.find("a").get("href"), "category": main_category_name})
            
            if ONY_FIND_3_PRODUCTS:
                if counter_third == 3:
                    break
    else:
        categories.append({"url": url_second_category,
                          "category": main_category_name})

def get_products_from_sub(url_to_scrawl, category):
    global used_ids, list_of_found_products

    try:
        source = requests.get(url_to_scrawl, headers=headers).text
        soup = BeautifulSoup(source, "lxml")

        # get total products
        total_products = soup.find(
            "p", class_="o-FilterBox__total-products").text.split("von")[-1]
        total = extract_numbers_from_string(total_products)[-1]
        pages = total//30
        if total % 30 != 0:
            pages += 1

    except:
        print("no response")
        pages = 1

    page_counter = 0
    for page in range(1, pages+1):
        page_counter += 1
        if SHOW_PRINTS:
            print("         ", page, "von", pages)
        url_page = f"{url_to_scrawl}?pageNumber={page}"

        try:
            source = requests.get(url_page, headers=headers).text
            soup = BeautifulSoup(source, "lxml")
            product_wrappers = soup.find_all(
                "div", class_="o-SearchProductListItem__link")

            for product_wrapper in product_wrappers:

                original_link = "https://www.shop-apotheke.com" + \
                    product_wrapper.find("a").get("href")
                price = product_wrapper.find(
                    "span", class_="a-Price").text.replace("€", "").strip()
                price = price.replace(",",".")
                basepricesplit = product_wrapper.find(
                    "p", class_="o-SearchProductListItem__prices__unitPricing")
                if basepricesplit != None:
                    basepricesplit = basepricesplit.text.split("/")
                    baseprice = basepricesplit[0].replace("€", "").strip()
                    baseprice = baseprice.replace(",",".")
                    unit = basepricesplit[1]
                else:
                    baseprice = price
                    unit = "Stk"
                id = ""
                link_split = original_link
                link_split = original_link.split("/")
                id = link_split[-2]
                name = product_wrapper.find("img").get("alt")

                product = Product.Product(name, id, float(price), float(baseprice), unit, "ShopApotheke", category, original_link)
                # if product not in list_of_found_products:
                #     if SHOW_PRINTS:
                #         print(id, name, category)
                #         list_of_found_products.append(product)

                # new_product = {
                #     "name": name,
                #     "price": price,
                #     "baseprice": baseprice,
                #     "id": id,
                #     "imageURL": imageURL,
                #     "original_link": original_link,
                #     "unit": unit,
                #     "category": category
                # }

                if id not in used_ids:
                    list_of_found_products.append(product)
                    used_ids.append(id)

        except Exception as e:
            #print("                  ", e)
            continue
        
        if ONY_FIND_3_PRODUCTS:
            if page_counter == 3:
                break

def get_products_from_shop():
    global list_found_products
    current = 1
    print("Get Categories")
    get_first_categories()
    print("Done")

    for product_page in categories:
        if SHOW_PRINTS:
            print(product_page, "[", current, "of", len(categories), "]")
        get_products_from_sub(product_page["url"], product_page["category"])
        current += 1

        if ONLY_ITERATE_3_TIMES:
            if current == 3:
                break

get_products_from_shop()

CrawlerHandler = crawler_handler.Crawler_Handler(list_of_found_products)
CrawlerHandler.handle()
