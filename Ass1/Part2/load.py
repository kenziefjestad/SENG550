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

def insert_new_customer(name, email, phone, address, conn):
    query = f"INSERT INTO customers (name, email, phone, address) VALUES ('{name}', '{email}', '{phone}', '{address}');"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                # print(cursor.fetchone())
                conn.commit()
                print("New customer inserted successfully.")
            except Exception as e:
                print(f"Error inserting new customer: {e}")
                conn.rollback()
            finally:
                # print(cursor.fetchone())
                # id = cursor.fetchone()["id"]
                cursor.close()
                if id:
                    return id

def insert_new_order(customerID, orderDate, totalAmount, productID, productCategory, productName, conn):
    query = f"INSERT INTO orders (customer_id, order_date, total_amount, product_id, product_category, product_name) VALUES ({customerID}, '{orderDate}', {totalAmount}, {productID}, '{productCategory}', '{productName}');"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                conn.commit()
                print("New order inserted successfully.")
            except Exception as e:
                print(f"Error inserting new order: {e}")
                conn.rollback()
            finally:
                cursor.close()
                # id = cursor.fetchone()["id"]
                if id:
                    return id

def insert_new_delivery(orderID, deliveryDate, deliveryStatus, conn):
    query = f"INSERT INTO deliveries (order_id, delivery_date, status) VALUES ({orderID}, '{deliveryDate}', '{deliveryStatus}');"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                conn.commit()
                print("New delivery inserted successfully.")
            except Exception as e:
                print(f"Error inserting new delivery: {e}")
                conn.rollback()
            finally:
                # id = cursor.fetchone()["id"]
                cursor.close()
                if id:
                    return id

def update_delivery_status(orderID, new_status, conn):
    query = f"UPDATE deliveries SET status = '{new_status}' WHERE delivery_id = {orderID};"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                conn.commit()
                print("Delivery status updated successfully.")
            except Exception as e:
                print(f"Error updating delivery status: {e}")
                conn.rollback()
            finally:
                # id = cursor.fetchone()["id"]
                cursor.close()
                if id:
                    return id

if __name__ == "__main__":
    db_name = "storedb"
    user = "postgres"
    password = os.environ.get("DB_PASSWORD")
    
    conn = connect_to_db(db_name, user, password)
    if conn:
        # part 2
        # insert_given_date(conn)

        # part 3
        # insert_new_customer('Liam Nelson', 'liam.nelson@example.com', '555-2468', '111 Elm Street', conn)
        # insert_new_order(11, '2025-06-01', '180.00', '116', 'Electronics', 'Bluetooth Speaker', conn)
        # insert_new_delivery(16, '2025-06-03', 'Pending', conn)
        # update_delivery_status(16, 'Shipped', conn)
        # insert_new_customer('John Cena', 'john.cena@example.com', '555-0000', '123 Main St', conn)
        # update_delivery_status(3, 'Delivered', conn)

        conn.close()
        print("Connection closed.")