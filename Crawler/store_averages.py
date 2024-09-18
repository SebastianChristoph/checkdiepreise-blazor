import json
import db_handler
import StoreCategoryPriceChange
import datetime 
rows = db_handler.get_average_store_data_from_sqlite_db()
result = {}

for row in rows:
    store, category, avg_price, avg_baseprice = row
    if store not in result:
        result[store] = {}
    result[store][category] = {
        'Price': round(avg_price, 2),
        'Baseprice': round(avg_baseprice, 2)
    }

# Ergebnis anzeigen

result_json = json.dumps(result, indent=4)

# Ergebnis anzeigen
print(result_json)


date = datetime.datetime.now().strftime('%Y-%m-%d')

for store, data in result.items():
    for category, prices in data.items():
        store_category_price_change = StoreCategoryPriceChange.StoreCategoryPriceChange(store, date, prices['Price'], prices['Baseprice'], category)

        db_handler.post_average_store_category_price_to_sqlite_db(store_category_price_change)
