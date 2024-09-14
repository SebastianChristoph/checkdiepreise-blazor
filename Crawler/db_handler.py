
import random
import datetime
import secrets
import pypyodbc as odbc
import sqlite3
import os

SHOW_PRINTS = False

connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{secrets.server},1433;Database={secrets.db_name};Uid={secrets.username};Pwd={secrets.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
SQLITE_DB_NAME = "LocalSqliteDb.db"
TABLE_PRICE_CHANGES = "ProductChanges"
TABLE_STORE_PRICE_CHANGES = "StorePriceChanges"
TABLE_DAILY_STATS = "DailyStats"


############### LOCAL SQLITE ##########
def create_db_with_table():
    cwd = os.getcwd()
    if "LocalSqliteDb.db" not in os.listdir(cwd):
        print("CREATE SQLite DB")
        try:
            sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
            cursor = sqlite_connection.cursor()
            print("     Erfolgreich mit DB verbunden")

            # CREATE TABLE PRICE CHANGES
            sql_query = f"""CREATE TABLE {TABLE_PRICE_CHANGES} (
                                Id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing primary key
                                Name NVARCHAR(255) NOT NULL,
                                Date DATETIME NOT NULL,
                                Identifier NVARCHAR(50) NOT NULL,
                                PriceUnit NUMERIC(18,2) NOT NULL,
                                UnitName NVARCHAR(50) NOT NULL,
                                Baseprice NUMERIC(18,2) NOT NULL,
                                BasepriceName NVARCHAR(50) NOT NULL,
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
                            PriceUnit DECIMAL(18,2) NOT NULL,
                            Baseprice DECIMAL(18,2) NOT NULL,
                            Category NVARCHAR(255) NOT NULL);"""
            
            sql_query3 = f"""CREATE TABLE {TABLE_DAILY_STATS} (
                            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing primary key
                            Date DATETIME NOT NULL,
                            MaxIdentifier TEXT NOT NULL,
                            MaxName TEXT NOT NULL,
                            MaxPrice DECIMAL(18, 2) NOT NULL,
                            MaxPriceBefore DECIMAL(18, 2) NOT NULL,
                            MaxStore TEXT NOT NULL,
                            MaxCategory TEXT, -- Optional field
                            MinIdentifier TEXT NOT NULL,
                            MinName TEXT NOT NULL,
                            MinPrice DECIMAL(18, 2) NOT NULL,
                            MinPriceBefore DECIMAL(18, 2) NOT NULL,
                            MinStore TEXT NOT NULL,
                            MinCategory TEXT -- Optional field
                        );
                        """
            
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
    
def post_price_change_to_local_sqlite_db(product, trend):
    change_date = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        if SHOW_PRINTS : print("         POST PriceChange to DB")
        sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
        cursor = sqlite_connection.cursor()
        
        if SHOW_PRINTS : print("             Erfolgreich mit DB verbunden", end = " > ")
        sql_query = f"""INSERT INTO {TABLE_PRICE_CHANGES} (Id, Name, Date, Identifier, PriceUnit, UnitName, Baseprice, BasepriceName, Store, Category, Trend, Url)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"""
        
        # Verwende den Decimal-Wert direkt im SQL-Query
        cursor.execute(sql_query, (None, product.product_name, change_date, product.identifier, product.price_unit, product.unit_name, product.baseprice, product.baseprice_name,product.store, product.category, trend, product.url))

        sqlite_connection.commit()
        if SHOW_PRINTS : print("Datenbank-Eintrag erfolgt", end = " > ")
        cursor.close()

    except Exception as e:
        if SHOW_PRINTS : print("Verbindung fehlerhaft:", e, end = " > ")
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            if SHOW_PRINTS : print("SQL Verbindung geschlossen")

def post_random_price_change_to_local_sqlite_db():
    names = ['Product A', 'Product B', 'Product C', 'Product D']
    stores = ["LIDL", "REWE", "ALDI"]
    categories = ['Electronics', 'Books', 'Clothing', 'Food']
    trends = ['up', 'down']

    if SHOW_PRINTS : print("POST Random Price Change")
    product_name = random.choice(names)
    change_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    identifier = random.randint(100000, 999999999999999999)
    price_unit = round(random.uniform(10.0, 500.0), 2)  # zufälliger Preis zwischen 10 und 500
    unit_name ="Stk"
    baseprice = round(random.uniform(10.0, 500.0), 2)  # zufälliger Preis zwischen 10 und 500
    baseprice_name ="Liter"
    store = random.choice(stores)
    category = random.choice(categories)
    trend = random.choice(trends)

    post_price_change_to_local_sqlite_db(product_name, change_date, identifier, price_unit, unit_name, baseprice, baseprice_name, store, category, trend)

def get_latest_price_data_by_identifier_for_product_from_sqlite_db(store, identifier) -> dict:
    if SHOW_PRINTS : print(f"         Get Price Change for {store} [{identifier}]")

    try:
        sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
        cursor = sqlite_connection.cursor()
        sql_query = f"""SELECT * FROM {TABLE_PRICE_CHANGES}
                WHERE Store=? AND Identifier=?
                ORDER BY Date ASC"""
        cursor.execute(sql_query, (store, identifier))

        # Ergebnisse abrufen
        results = cursor.fetchall()
        cursor.close()

        if len(results) > 0:        
            data = {
                "date" : results[-1][2],
                "price_unit_old" : results[-1][4],
                "price_unit_bulk_old" : results[-1][6],
            }
            return data

        return None
        
    except Exception as e:
        if SHOW_PRINTS : print("Verbindung fehlerhaft:", e)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            

################ AZURE #################
def get_conn():
    conn = odbc.connect(connection_string)
    return conn

def post_price_change_to_azure(product, trend):
    change_date = datetime.datetime.now().strftime('%Y-%m-%d')
    sql_query = f"""
    INSERT INTO [dbo].[ProductChanges] (Name, Date, Identifier, PriceUnit, UnitName, Baseprice, BasepriceName, Store, Category, Trend, Url)
    VALUES ('{product.product_name}', '{change_date}', '{product.identifier}', {product.price_unit},'{product.unit_name}', {product.baseprice},'{product.baseprice_name}', '{product.store}', '{product.category}', '{trend}', '{product.url}');
    """
    retries = 3
    tries = 0
    skip = False
    while skip == False:
        try:
            with get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                if SHOW_PRINTS: print("             >>> POSTED TO AZURE!")
                skip = True
        except Exception as e:
            tries += 1
            print("                 >>> FEHLER UPLOAD AZURE!", e)
            if tries == retries:
                skip = True
                if SHOW_PRINTS: print("                 >>> SKIP!")
            else:
                if SHOW_PRINTS: print("                 >>> RETRY:", tries)


def post_random_price_change_to_azure():

    names = ['Product A', 'Product B', 'Product C', 'Product D']
    stores = ["LIDL", "REWE", "ALDI"]
    categories = ['Electronics', 'Books', 'Clothing', 'Food']
    trends = ['up', 'down']

    if SHOW_PRINTS: print("Start POST random")
    product_name = random.choice(names)
    change_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    identifier = random.randint(100000, 999999999999999999)
    price_unit = round(random.uniform(10.0, 500.0), 2)  # zufälliger Preis zwischen 10 und 500
    unit_name ="Stk"
    price_bulk = round(random.uniform(10.0, 500.0), 2)  # zufälliger Preis zwischen 10 und 500
    bulk_unit_name ="Liter"
    store = random.choice(stores)
    category = random.choice(categories)
    trend = random.choice(trends)

    post_price_change_to_azure(product_name, change_date, identifier, price_unit, unit_name, price_bulk, bulk_unit_name, store, category, trend)


def main():
    if SHOW_PRINTS: print("\n\nStart DB Handler")
    create_db_with_table()

main()
