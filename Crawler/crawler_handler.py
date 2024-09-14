import db_handler
import datetime

class Crawler_Handler:
    def __init__(self, products):
        self.products = products
        self.price_changes = []
        self.new_products = 0
        self.updates_products = 0
        self.skipped_products = 0

    def post_price_changes_to_db(self):
        for price_change in self.price_changes:
            print(f"     Post <{price_change.product_name}> to DB")
            db_handler.post_price_change_to_local_sqlite_db(price_change)
    
    def clean_up_product(self, product):
        # CleanUp Product
        print("         Clean up Product:", product.product_name)

    def handle(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        print("START CRAWLER HANDLER Handle() for", today)

        # Iterate over Products
        for product in self.products:

            print(f"     Check <{product.product_name}>")
            
            self.clean_up_product(product)

            # Check if Price-Changes
            price_changes_for_product = db_handler.get_latest_price_data_by_identifier_for_product_from_sqlite_db(product.store, product.identifier)

            # WENN priceChange == None : neues Produkt
            if price_changes_for_product == None:
                print("         >>> Neues Produkt mit Preis:", product.price_unit)
                trend = "none"
                db_handler.post_price_change_to_local_sqlite_db(product, trend)
                self.new_products += 1
                
            else:
                if price_changes_for_product["date"] == today:
                    print("         >> Bereits Eintrag für heute:", price_changes_for_product["date"])
                    self.skipped_products += 1
                    print("     _____________________________________________")
                    continue
                print("         >>> Berechne Trend")
                print("         Alter Preis:", price_changes_for_product["price_unit_old"])
                print("         Neuer Preis:", product.price_unit)
                diff =  product.price_unit - price_changes_for_product["price_unit_old"]
                print("         Differenz:", diff)

                if(diff == 0):
                    print("         Kein neuer Preis, continue!")
                    continue

                if diff > 0: 
                    trend = "up"
                else:
                    trend = "down"
                print("         Trend:", trend)

                db_handler.post_price_change_to_local_sqlite_db(product, trend)
                self.updates_products += 1
                
            print("     _____________________________________________")


        print("#################################################################################")
        print("     Neue Produkte:", self.new_products)
        print("     Update Produkte:", self.updates_products)
        print("     Skipped Produkte:", self.skipped_products)

