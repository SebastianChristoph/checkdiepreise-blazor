class PriceChange:
    def __init__(self, product_name, change_date, identifier, price, price_before, baseprice, baseprice_before, difference, difference_baseprice, baseprice_unit, store, category, trend, url):
        self.product_name = product_name
        self.change_date = change_date
        self.identifier = identifier
        self.price = price
        self.price_before = price_before
        self.baseprice = baseprice
        self.baseprice_before = baseprice_before
        self.difference = difference
        self.difference_baseprice = difference_baseprice
        self.baseprice_unit = baseprice_unit
        self.store = store
        self.category = category
        self.trend = trend
        self.url = url

