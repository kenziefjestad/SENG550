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
                
def add_product(product_id, name, category, price, conn):
    query = f"INSERT INTO dim_products (product_id, name, category, price) VALUES ('{product_id}', '{name}', '{category}', {price}) RETURNING id;"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                id = cursor.fetchone()[0]
                conn.commit()
                print("New product inserted successfully.")
            except Exception as e:
                print(f"Error inserting new product: {e}")
                conn.rollback()
            finally:
                cursor.close()
                if id:
                    return id
                
def add_customer(customer_id, name, email, city, conn):
    query = f"INSERT INTO dim_customers (customer_id, name, email, city) VALUES ('{customer_id}', '{name}', '{email}', '{city}') RETURNING id;"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                id = cursor.fetchone()[0]
                conn.commit()
                print("New customer inserted successfully.")
            except Exception as e:
                print(f"Error inserting new customer: {e}")
                conn.rollback()
            finally:
                cursor.close()
                if id:
                    return id

def update_customer_city(customer_id, new_city, conn):
    query = f"SELECT (id, customer_id, name, email, city) FROM dim_customers WHERE customer_id = '{customer_id}' AND end_date = '9999-12-31 23:59:59';"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                row = cursor.fetchone()
                # conn.commit()
                print("Customer found successfully.")
            except Exception as e:
                print(f"Error finding customer: {e}")
                # conn.rollback()
            finally:
                cursor.close()
                if row:
                    # Set the end_date of the current record to today
                    # print(row[0])
                    row = row[0].strip("()").split(",")
                    id = row[0]
                    customer_id = row[1]
                    name = row[2].strip().strip("'").strip("\"")
                    email = row[3].strip().strip("'").strip("\"")
                    city = row[4].strip().strip("'").strip("\"")
                    # print(f"id: {id}, customer_id: {customer_id}, name: {name}, email: {email}, city: {city}")
                    update_query = f"UPDATE dim_customers SET end_date = CURRENT_TIMESTAMP WHERE id = {id};"
                    try:
                        cursor = create_cursor(conn)
                        if cursor:
                            cursor.execute(update_query)
                            conn.commit()
                            print("Customer end_date updated successfully.")
                    except Exception as e:
                        print(f"Error updating customer end_date: {e}")
                        conn.rollback()
                    finally:
                        cursor.close()

    query = f"INSERT INTO dim_customers (customer_id, name, email, city) VALUES ('{customer_id}', '{name}', '{email}', '{new_city}');"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                conn.commit()
                print("Customer city updated successfully.")
            except Exception as e:
                print(f"Error updating customer city: {e}")
                conn.rollback()
            finally:
                cursor.close()

def update_product_price(product_id, new_price, conn):
    query = f"SELECT (id, product_id, name, category, price) FROM dim_products WHERE product_id = '{product_id}' AND end_date = '9999-12-31 23:59:59';"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                row = cursor.fetchone()
                # conn.commit()
                print("Product found successfully.")
            except Exception as e:
                print(f"Error finding product: {e}")
                # conn.rollback()
            finally:
                cursor.close()
                if row:
                    # Set the end_date of the current record to today
                    print(row[0])
                    row = row[0].strip("()").split(",")
                    id = row[0]
                    product_id = row[1]
                    name = row[2].strip().strip("'").strip("\"")
                    category = row[3].strip().strip("'").strip("\"")
                    price = row[4].strip().strip("'").strip("\"")
                    print(f"id: {id}, product_id: {product_id}, name: {name}, category: {category}, price: {price}")
                    update_query = f"UPDATE dim_products SET end_date = CURRENT_TIMESTAMP WHERE id = {id};"
                    try:
                        cursor = create_cursor(conn)
                        if cursor:
                            cursor.execute(update_query)
                            conn.commit()
                            print("Product end_date updated successfully.")
                    except Exception as e:
                        print(f"Error updating product end_date: {e}")
                        conn.rollback()
                    finally:
                        cursor.close()

    query = f"INSERT INTO dim_products (product_id, name, category, price) VALUES ('{product_id}', '{name}', '{category}', {new_price});"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                conn.commit()
                print("Product price updated successfully.")
            except Exception as e:
                print(f"Error updating product price: {e}")
                conn.rollback()
            finally:
                cursor.close()

def add_order(order_id, product_id, customer_id, amount, conn):
    query = f"SELECT id FROM dim_products WHERE product_id = '{product_id}' AND end_date = '9999-12-31 23:59:59';"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                product_row = cursor.fetchone()
                print("Product found successfully.")
            except Exception as e:
                print(f"Error finding product: {e}")
            finally:
                cursor.close()
                if product_row:
                    product_id = product_row[0]
                else:
                    print(f"Product with product_id {product_id} not found.")
                    return
    query = f"SELECT id FROM dim_customers WHERE customer_id = '{customer_id}' AND end_date = '9999-12-31 23:59:59';"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                customer_row = cursor.fetchone()
                print("Customer found successfully.")
            except Exception as e:
                print(f"Error finding customer: {e}")
            finally:
                cursor.close()
                if customer_row:
                    customer_id = customer_row[0]
                else:
                    print(f"Customer with customer_id {customer_id} not found.")
                    return
    query = f"INSERT INTO fact_orders (order_id, product_id, customer_id, amount) VALUES ('{order_id}', {product_id}, {customer_id}, {amount});"
    if conn:
        cursor = create_cursor(conn)
        if cursor:
            try:
                cursor.execute(query)
                conn.commit()
                print("Order added successfully.")
            except Exception as e:
                print(f"Error adding order: {e}")
                conn.rollback()
            finally:
                cursor.close()


if __name__ == "__main__":
    db_name = "assignment2"
    user = "postgres"
    password = os.environ.get("DB_PASSWORD")
    
    conn = connect_to_db(db_name, user, password)
    if conn:
        # part 2
        # add_product("P1", "Laptop", "Electronics", 1000.00, conn)
        # add_product("P2", "Phone", "Electronics", 500.00, conn)
        # add_customer("C1", "Alice", "", "New York", conn)
        # add_customer("C2", "Bob", "", "Boston", conn)
        # add_order("O1", "P1", "C1", 1000.00, conn)
        # update_customer_city("C1", "Chicago", conn)
        # update_product_price("P1", 900.00, conn)
        # add_order("O2", "P1", "C2", 850.00, conn)
        # update_customer_city("C2", "Calgary", conn)
        # add_order("O3", "P2", "C2", 500.00, conn)
        # add_order("O4", "P1", "C1", 900.00, conn)
        # update_customer_city("C1", "San Francisco", conn)
        # add_order("O5", "P2", "C1", 450.00, conn)
        # add_order("O6", "P1", "C2", 900.00, conn)

        conn.close()
        print("Connection closed.")