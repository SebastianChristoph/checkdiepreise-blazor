class PriceChange:
    def __init__(self, product_name, change_date, identifier, priceUnit, unit_name, price_bulk, bulk_unit_name, store, category, trend):
        self.product_name = product_name
        self.change_date = change_date
        self.identifier = identifier
        self.price_unit = priceUnit
        self.unit_name = unit_name
        self.price_bulk = price_bulk
        self.bulk_unit_name = bulk_unit_name
        self.store = store
        self.category = category
        self.trend = trend

