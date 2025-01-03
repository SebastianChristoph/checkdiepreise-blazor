import db_handler
import datetime
import re
import PriceChange
import random 
import store_averages
#import ftp_uploader

start_time = datetime.datetime.now()
SHOW_PRINTS = False

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

        forbidden_characters = ["|", '"', "\\", "/", "'", "™", "®"]

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
            if SHOW_PRINTS: print(f"     Check <{product.name}>")

            # CLEAN UP
            product.price = self.clean_price_text(product.price)
            product.name = self.clean_name(product.name)
            product.baseprice_unit = self.clean_unit_text(product.baseprice_unit)

            # Check if Price-Changes
            price_changes_for_product = db_handler.get_latest_price_data_by_identifier_for_product_from_sqlite_db(product.store, product.identifier)

            if price_changes_for_product is None:
                # Neues Produkt
                if SHOW_PRINTS: print(f"         >>> Neues Produkt mit Preis: {product.price} [{product.baseprice}] ({today})")
                new_product_price_change = PriceChange.PriceChange(product.name, today, product.identifier, product.price, product.price, product.baseprice, product.baseprice, 0, 0, 0, 0, product.baseprice_unit, product.store, product.category, "none", product.url)

                self.price_changes.append(new_product_price_change)  # Sammele die Price Changes
                db_handler.post_price_change_to_local_sqlite_db(new_product_price_change)
                self.new_products += 1
                
            else:
                # Bestehendes Produkt
                if price_changes_for_product["date"] == today:
                    if SHOW_PRINTS: print("         >> Bereits Eintrag für TODAY:", price_changes_for_product["date"])
                    self.skipped_products += 1
                    continue

                difference = product.price - price_changes_for_product["price_old"]
                difference_baseprice = product.baseprice - price_changes_for_product["baseprice_old"]

                try:
                    # Berechnung des prozentualen Unterschieds (Vermeidung von Division durch Null)
                    if price_changes_for_product["price_old"] != 0:
                        price_difference_percent = (difference / price_changes_for_product["price_old"]) * 100
                    else:
                        price_difference_percent = None  # oder setze es auf 0, wenn du das bevorzugst

                    if price_changes_for_product["baseprice_old"] != 0:
                        baseprice_difference_percent = (difference_baseprice / price_changes_for_product["baseprice_old"]) * 100
                    else:
                        baseprice_difference_percent = None  # oder setze es auf 0, wenn du das bevorzugst
                except:
                    price_difference_percent = None
                    baseprice_difference_percent = None


                if difference == 0 and difference_baseprice == 0:
                    self.skipped_products += 1
                    continue

                trend = "up" if (difference > 0 or difference_baseprice > 0) else "down"
                if SHOW_PRINTS: print(f"         >>> Neuer PriceChange {product.name} ({today})")
                new_price_change = PriceChange.PriceChange(
                    product.name, today, product.identifier, product.price, price_changes_for_product["price_old"],
                    product.baseprice, price_changes_for_product["baseprice_old"], difference, difference_baseprice, price_difference_percent, baseprice_difference_percent, product.baseprice_unit, product.store, product.category, trend, product.url
                )

                self.price_changes.append(new_price_change)
                db_handler.post_price_change_to_local_sqlite_db(new_price_change)
                self.updates_products += 1

            if SHOW_PRINTS: print("     _____________________________________________")

        if len(self.products) > 0:
            random_product_for_report = random.choice(self.products)
            if random_product_for_report:
                db_handler.post_random_product_to_daily_report_sqlite(random_product_for_report)
        else:
            if SHOW_PRINTS: print("NO PRODUCTS TO CHOSE RANDOM REPORT")
        
        store_averages.calculate_store_category_averages(self.products)

        print("\n#################################################################################")
        print("     Info für", today)
        print("     Neue Produkte:", self.new_products)
        print("     Update Produkte:", self.updates_products)
        print("     Skipped Produkte:", self.skipped_products)

        #ftp_uploader.upload_sqlitedb_to_azure()

        end_time = datetime.datetime.now()
        time_difference = end_time - start_time
        print(f"\n\nDauer: {time_difference} [hh:mm:ss:ms]")