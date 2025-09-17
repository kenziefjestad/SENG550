import psycopg2
import csv
import os
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
    
def get_csv_data(data_list):
    data = []
    for file_name in data_list:
        try:
            with open(file_name, mode='r') as file:
                reader = csv.reader(file)
                file_data = [row for row in reader]
                data.append({file_name: file_data})
        except FileNotFoundError:
            print(f"File {file_name} not found.")
    return data

def generate_table_insert_query(table_name, columns, data: list):
    values = ""
    for row in data:
        if row:
            values += "(" + ", ".join(f"'{str(item)}'" for item in row) + "), "
    values = values.rstrip(", ")
    columns_joined = ', '.join(columns)
    query = f"INSERT INTO {table_name} ({columns_joined}) VALUES {values};"
    return query

def insert_given_date(conn):
    list_of_csv = ["customers.csv", "deliveries.csv", "orders.csv"]

    data = get_csv_data(list_of_csv)
    customer_query = generate_table_insert_query("customers", data[0]["customers.csv"][0], data[0]["customers.csv"][1:])
    deliviries_query = generate_table_insert_query("deliveries", data[1]["deliveries.csv"][0], data[1]["deliveries.csv"][1:])
    orders_query = generate_table_insert_query("orders", data[2]["orders.csv"][0], data[2]["orders.csv"][1:])

    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(customer_query)
                cursor.execute(orders_query)
                cursor.execute(deliviries_query)
                conn.commit()
                print("Data inserted successfully.")
            except Exception as e:
                print(f"Error executing queries: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
                print("Cursor and connection closed.")


if __name__ == "__main__":
    db_name = "storedb"
    user = "postgres"
    password = os.environ.get("DB_PASSWORD")
    
    conn = connect_to_db(db_name, user, password)
    if conn:
        # insert_given_date(conn)
        conn.close()
        print("Connection closed.")