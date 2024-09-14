class Product:
    def __init__(self, product_name, identifier, priceUnit, unit_name, price_bulk, bulk_unit_name, store, category, url):
        self.product_name = product_name
        self.identifier = identifier
        self.price_unit = priceUnit
        self.unit_name = unit_name
        self.baseprice = price_bulk
        self.baseprice_name = bulk_unit_name
        self.store = store
        self.category = category
        self.url = url
