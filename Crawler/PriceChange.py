class PriceChange:
    def __init__(self, product_name, change_date, identifier, price, price_before, baseprice, baseprice_before, difference, difference_baseprice, difference_percentage, difference_baseprice_percentage, baseprice_unit, store, category, trend, url):
        self.product_name = product_name
        self.change_date = change_date
        self.identifier = identifier
        self.price = price
        self.price_before = price_before
        self.baseprice = baseprice
        self.baseprice_before = baseprice_before
        self.difference = difference
        self.difference_baseprice = difference_baseprice
        self.difference_percentage = difference_percentage
        self.difference_baseprice_percentage = difference_baseprice_percentage
        self.baseprice_unit = baseprice_unit
        self.store = store
        self.category = category
        self.trend = trend
        self.url = url