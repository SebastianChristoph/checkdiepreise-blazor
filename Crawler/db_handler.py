
import datetime
import sqlite3
import os

SHOW_PRINTS = False
SQLITE_DB_NAME = "LocalSqliteDb.db"
TABLE_PRICE_CHANGES = "ProductChanges"
TABLE_STORE_PRICE_CHANGES = "StorePriceChanges"
TABLE_DAILY_REPORTS = "DailyReports"

def create_db_with_table():
    cwd = os.getcwd()
    if "LocalSqliteDb.db" not in os.listdir(cwd):
        print("CREATE SQLite DB")
        try:
            sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
            cursor = sqlite_connection.cursor()
            print("     Erfolgreich mit DB verbunden")

            sql_query = f"""CREATE TABLE {TABLE_PRICE_CHANGES} (
                                Id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing primary key
                                Name NVARCHAR(255) NOT NULL,
                                Date DATETIME NOT NULL,
                                Identifier NVARCHAR(50) NOT NULL,
                                Price NUMERIC(18,2) NOT NULL,
                                Baseprice NUMERIC(18,2) NOT NULL,
                                PriceBefore NUMERIC(18,2) NOT NULL,
                                BasepriceBefore NUMERIC(18,2) NOT NULL,
                                Difference NUMERIC(18,2) NOT NULL,
                                DifferenceBaseprice NUMERIC(18,2) NOT NULL,
                                BasepriceUnit NVARCHAR(50) NOT NULL,
                                Store NVARCHAR(255) NOT NULL,
                                Category NVARCHAR(255),
                                Trend NVARCHAR(50) NOT NULL,
                                Url NVARCHAR(255)
                            );
                            """
            
            sql_query2 = f"""CREATE TABLE {TABLE_STORE_PRICE_CHANGES}(
                            Id INTEGER PRIMARY KEY,
                            StoreName NVARCHAR(255) NOT NULL,
                            Date DATETIME NOT NULL,
                            Price DECIMAL(18,2) NOT NULL,
                            Baseprice DECIMAL(18,2) NOT NULL,
                            Category NVARCHAR(255) NOT NULL);"""
            
            sql_query3 = f"""CREATE TABLE {TABLE_DAILY_REPORTS} (
                            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing primary key
                            Name NVARCHAR(255) NOT NULL,
                            Date DATETIME NOT NULL,
                            Identifier NVARCHAR(50) NOT NULL,
                            Price DECIMAL(18,2) NOT NULL,
                            Baseprice DECIMAL(18,2) NOT NULL,
                            BasepriceUnit NVARCHAR(50) NOT NULL,
                            Store NVARCHAR(255) NOT NULL,
                            Category NVARCHAR(255),
                            Url NVARCHAR(255)
                        );"""
            
            cursor.execute(sql_query)
            cursor.execute(sql_query2)
            cursor.execute(sql_query3)
            sqlite_connection.commit()
            cursor.close()

        except:
            print("     Verbindung fehlerhaft")
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("     SQL Verbindung geschlossen")
    else:
        print("Found SQLite DB")
    
def post_price_change_to_local_sqlite_db(price_change):
    if SHOW_PRINTS == False:
        print(".", end="")
    change_date = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        if SHOW_PRINTS : print("         POST PriceChange to DB")
        sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
        cursor = sqlite_connection.cursor()
        
        if SHOW_PRINTS : print("             Erfolgreich mit DB verbunden", end = " > ")
        sql_query = f"""INSERT INTO {TABLE_PRICE_CHANGES} (Id, Name, Date, Identifier, Price, PriceBefore, Baseprice, BasepriceBefore, Difference, DifferenceBaseprice, BasepriceUnit, Store, Category, Trend, Url)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
        
        cursor.execute(sql_query, (None, price_change.product_name, change_date, price_change.identifier, price_change.price, price_change.price_before, price_change.baseprice, price_change.baseprice_before, price_change.difference, price_change.difference_baseprice, price_change.baseprice_unit, price_change.store, price_change.category, price_change.trend, price_change.url))

        sqlite_connection.commit()
        if SHOW_PRINTS : print("Datenbank-Eintrag erfolgt", end = " > ")
        cursor.close()

    except Exception as e:
        if SHOW_PRINTS : print("Verbindung fehlerhaft:", e, end = " > ")
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            if SHOW_PRINTS : print("SQL Verbindung geschlossen")

def post_random_product_to_daily_report_sqlite(product):
    change_date = datetime.datetime.now().strftime('%Y-%m-%d')

    store_report_for_today = get_daily_report_for_store(product.store)
    if len(store_report_for_today) > 0:
        if SHOW_PRINTS : print("    \nSTORE hat bereits Daily Report")
        return
    else:
        try:
            if SHOW_PRINTS : print("    \nPOST Random PriceChange to Daily Report")
            sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
            cursor = sqlite_connection.cursor()
            
            if SHOW_PRINTS : print("             Erfolgreich mit DB verbunden", end = " > ")
            sql_query = f"""INSERT INTO {TABLE_DAILY_REPORTS} (Id, Name, Date, Identifier, Price, Baseprice, BasepriceUnit, Store, Category, Url)
            VALUES (?,?,?,?,?,?,?,?,?,?);"""
            
            cursor.execute(sql_query, (None, product.name, change_date, product.identifier, product.price, product.baseprice, product.baseprice_unit, product.store, product.category,product.url))

            sqlite_connection.commit()
            if SHOW_PRINTS : print("Datenbank-Eintrag erfolgt", end = " > ")
            cursor.close()

        except Exception as e:
            if SHOW_PRINTS : print("Verbindung fehlerhaft:", e, end = " > ")
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                if SHOW_PRINTS : print("SQL Verbindung geschlossen")

def get_latest_price_data_by_identifier_for_product_from_sqlite_db(store, identifier) -> dict:
    if SHOW_PRINTS : print(f"         Get Price Change for {store} [{identifier}]")

    try:
        sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
        sqlite_connection.row_factory = sqlite3.Row
        cursor = sqlite_connection.cursor()

        sql_query = f"""SELECT * FROM {TABLE_PRICE_CHANGES}
                        WHERE Store=? AND Identifier=?
                        ORDER BY Date ASC"""
        cursor.execute(sql_query, (store, identifier))
        results = cursor.fetchall()
        cursor.close()

        if len(results) > 0:
            last_entry = dict(results[-1])
            data = {
                "date": last_entry["Date"],
                "price_old": last_entry["Price"],
                "baseprice_old": last_entry["Baseprice"]
            }
            return data

        return None
        
    except Exception as e:
        if SHOW_PRINTS : print("Verbindung fehlerhaft:", e)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            
def get_daily_report_for_store(store):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
        cursor = sqlite_connection.cursor()
        sql_query = f"""SELECT * FROM {TABLE_DAILY_REPORTS}
                WHERE Store=? AND Date=?"""
        cursor.execute(sql_query, (store, today))
        results = cursor.fetchall()
        cursor.close()

        return results
    
    except Exception as e:
        if SHOW_PRINTS : print("Verbindung fehlerhaft:", e)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def get_average_store_data_from_sqlite_db():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
        cursor = sqlite_connection.cursor()
        sql_query = f"""
            SELECT Store, Category, AVG(Price) as avg_price, AVG(Baseprice) as avg_baseprice
            FROM {TABLE_PRICE_CHANGES}
            WHERE Date(Date) = ?
            GROUP BY Store, Category"""
        cursor.execute(sql_query, (today,))
        rows = cursor.fetchall()
        cursor.close()

        return rows
    
    except Exception as e:
        if SHOW_PRINTS : print("Verbindung fehlerhaft:", e)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def post_average_store_category_price_to_sqlite_db(store_category_price_change):
    if SHOW_PRINTS == False:
        print(".", end="")
    try:
        if SHOW_PRINTS : print("         POST Average Storages Prices to DB")
        sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
        cursor = sqlite_connection.cursor()
        
        if SHOW_PRINTS : print("             Erfolgreich mit DB verbunden", end = " > ")
        sql_query = f"""INSERT INTO {TABLE_STORE_PRICE_CHANGES} (Id, StoreName, Date, Price, Baseprice, Category)
        VALUES (?,?,?,?,?,?);"""
        cursor.execute(sql_query, (None, store_category_price_change.store_name, store_category_price_change.date, store_category_price_change.price, store_category_price_change.baseprice, store_category_price_change.category))

        sqlite_connection.commit()
        if SHOW_PRINTS : print("Datenbank-Eintrag erfolgt", end = " > ")
        cursor.close()
    except Exception as e:
        if SHOW_PRINTS : print("Verbindung fehlerhaft:", e, end = " > ")
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            if SHOW_PRINTS : print("SQL Verbindung geschlossen")

def main():
    if SHOW_PRINTS: print("\n\nStart DB Handler")
    create_db_with_table()

main()
