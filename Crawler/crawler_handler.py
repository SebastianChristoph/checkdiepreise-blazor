import db_handler
import datetime
import re

SHOW_PRINTS = True
TO_AZURE = True

class Crawler_Handler:
    def __init__(self, products):
        self.products = products
        self.price_changes = []
        self.new_products = 0
        self.updates_products = 0
        self.skipped_products = 0

    def post_price_changes_to_db(self):
        for price_change in self.price_changes:
            if SHOW_PRINTS: print(f"     Post <{price_change.product_name}> to DB")
            db_handler.post_price_change_to_local_sqlite_db(price_change)
    
    def clean_price_text(self, price):

        #print("             Price in:", price, type(price))
        try:

            cleaned_price = str(price)
            cleaned_price = cleaned_price.replace(",", ".")

            if "=" in cleaned_price:
                cleaned_price = cleaned_price.split("=")[-1]

            match = re.search(r'\d+(\.\d*)?', cleaned_price)

            if match:
                cleaned_price = match.group()
                cleaned_price = float(cleaned_price)
                cleaned_price = round(cleaned_price, 2)
                cleaned_price = format(cleaned_price, '.2f')
                if (cleaned_price[-1] == "."):
                    cleaned_price = cleaned_price[:-1]
                
                #print("             Price out:", float(cleaned_price), type(price))
                return float(cleaned_price)
            else:
                if SHOW_PRINTS: print("No cleaning possible for:", price)
                return 0

        except Exception as e:
            if self.show_prints:
                if SHOW_PRINTS: print("ERROR IN CLEANING")
                if SHOW_PRINTS: print(e)
                if SHOW_PRINTS: print("PRICE IN:", price,
                      " / PRICE IN TYPE:", type(price))
                if SHOW_PRINTS: print("----------------")
            return "0"

    def clean_name(self, name):

        forbidden_characters = ["|", '"', "\\", "/"]

        for char in forbidden_characters:
            name = name.replace(char, "")

        name = name.replace("  ", " ")

        return name

    def clean_unit_text(self, unittext):
        return unittext.upper()

    def handle(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        print("\n\n\nSTART CRAWLER HANDLER Handle() for", today)

        for product in self.products:

            if SHOW_PRINTS: print(f"     Check <{product.product_name}>")
            
            # CLEAN UP
            product.price_unit = self.clean_price_text(product.price_unit)
            product.product_name = self.clean_name(product.product_name)
            product.baseprice_name = self.clean_unit_text(product.baseprice_name)

            # Check if Price-Changes
            price_changes_for_product = db_handler.get_latest_price_data_by_identifier_for_product_from_sqlite_db(product.store, product.identifier)

            # WENN priceChange == None : neues Produkt
            if price_changes_for_product == None:
                if SHOW_PRINTS: print("         >>> Neues Produkt mit Preis:", product.price_unit)
                trend = "none"
                db_handler.post_price_change_to_local_sqlite_db(product, trend)
                if TO_AZURE:
                    db_handler.post_price_change_to_azure(product, trend)
                
                self.new_products += 1
                
            else:
                if price_changes_for_product["date"] == today:
                    if SHOW_PRINTS: print("         >> Bereits Eintrag für heute:", price_changes_for_product["date"])
                    self.skipped_products += 1
                    if SHOW_PRINTS: print("     _____________________________________________")
                    continue
                if SHOW_PRINTS: print("         >>> Berechne Trend")
                if SHOW_PRINTS: print("         Alter Preis:", price_changes_for_product["price_unit_old"])
                if SHOW_PRINTS: print("         Neuer Preis:", product.price_unit)
                diff =  product.price_unit - price_changes_for_product["price_unit_old"]
                if SHOW_PRINTS: print("         Differenz:", diff)

                if(diff == 0):
                    if SHOW_PRINTS: print("         Kein neuer Preis, continue!")
                    continue

                if diff > 0: 
                    trend = "up"
                else:
                    trend = "down"
                if SHOW_PRINTS: print("         Trend:", trend)

                db_handler.post_price_change_to_local_sqlite_db(product, trend)
                self.updates_products += 1
                
            if SHOW_PRINTS: print("     _____________________________________________")


        print("#################################################################################")
        print("     Neue Produkte:", self.new_products)
        print("     Update Produkte:", self.updates_products)
        print("     Skipped Produkte:", self.skipped_products)

