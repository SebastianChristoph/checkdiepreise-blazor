
import random
import datetime
import secrets
import pypyodbc as odbc

connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{secrets.server},1433;Database={secrets.db_name};Uid={secrets.username};Pwd={secrets.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

names = ['Product A', 'Product B', 'Product C', 'Product D']
stores = ["LIDL", "REWE", "ALDI"]
categories = ['Electronics', 'Books', 'Clothing', 'Food']
trends = ['up', 'down']

def get_conn():
    conn = odbc.connect(connection_string)
    return conn

def post_random():
    name = random.choice(names)
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    identifier = random.randint(100000, 999999999999999999)
    price = round(random.uniform(10.0, 500.0), 2)  # zufälliger Preis zwischen 10 und 500
    store = random.choice(stores)
    category = random.choice(categories)
    trend = random.choice(trends)

    sql_query = f"""
    INSERT INTO [dbo].[ProductChanges] (Name, Date, Identifier, Price, Store, Category, Trend)
    VALUES ('{name}', '{date}', '{identifier}', {price}, '{store}', '{category}', '{trend}');
    """
    
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query)

post_random()