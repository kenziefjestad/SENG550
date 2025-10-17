import psycopg2
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

def connect_to_db(db_name, user, password):
    try:
        conn = psycopg2.connect(dbname=db_name, user=user, password=password)
        print("Connection to database established.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_cursor(conn):
    try:
        cursor = conn.cursor()
        print("Cursor created.")
        return cursor
    except Exception as e:
        print(f"Error creating cursor: {e}")
        return None
    
def join_data(conn):
    query = """
    SELECT 
        o.order_id, o.order_date, 
        c.customer_id, c.name AS customer_name, c.city AS customer_city, 
        p.product_id, p.name AS product_name, p.price AS product_price, 
        o.amount
    FROM fact_orders o
    JOIN dim_customers c ON o.customer_id = c.id
    JOIN dim_products p ON o.product_id = p.id;
    """
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                print("Data joined successfully.")
                return rows
            except Exception as e:
                print(f"Error joining data: {e}")
            finally:
                cursor.close()

def insert_into_mongodb(data):
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client['sales_db']
    collection = db['orders_summary']
    
    documents = []
    for row in data:
        document = {
            "order_id": row[0],
            "order_date": row[1],
            "customer_id": row[2],
            "customer_name": row[3],
            "customer_city": row[4],
            "product_id": row[5],
            "product_name": row[6],
            "product_price": float(row[7]),
            "amount": float(row[8])
        }
        documents.append(document)

    # print(documents)
    
    if documents:
        try:
            collection.insert_many(documents)
            print("Data inserted into MongoDB successfully.")
        except Exception as e:
            print(f"Error inserting data into MongoDB: {e}")
    client.close()

if __name__ == "__main__":
    db_name = "assignment2"
    user = "postgres"
    password = os.environ.get("DB_PASSWORD")
    
    conn = connect_to_db(db_name, user, password)
    if conn:
        joined_data = join_data(conn)
        insert_into_mongodb(joined_data)
        conn.close()
        print("Connection closed.")