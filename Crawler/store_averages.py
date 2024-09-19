import db_handler
import StoreCategoryAveragePrice
import datetime 
from collections import defaultdict

def calculate_store_category_averages(products):

    print("\n#######################################")
    print("\nCalculate Store Category Averages")

    store_category_data = defaultdict(lambda: defaultdict(lambda: {'price_sum': 0, 'baseprice_sum': 0, 'count': 0}))
    
    # Aggregate data
    for product in products:
        store = product.store
        category = product.category
        store_category_data[store][category]['price_sum'] += product.price
        store_category_data[store][category]['baseprice_sum'] += product.baseprice
        store_category_data[store][category]['count'] += 1
    
    result = {}
    for store, categories in store_category_data.items():
        result[store] = {}
        for category, stats in categories.items():
            count = stats['count']
            if count > 0:
                avg_price = round(stats['price_sum'] / count , 2)
                avg_baseprice = round(stats['baseprice_sum'] / count, 2)
                result[store][category] = {
                    'Price': avg_price,
                    'Baseprice': avg_baseprice
                }

    date = datetime.datetime.now().strftime('%Y-%m-%d')

    for store, data in result.items():
        for category, prices in data.items():
            store_category_price_change = StoreCategoryAveragePrice.StoreCategoryPriceChange(store, date, prices['Price'], prices['Baseprice'], category)

            db_handler.post_average_store_category_price_to_sqlite_db(store_category_price_change)

    print("\nDONE")