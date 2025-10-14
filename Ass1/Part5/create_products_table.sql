CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_category TEXT,
    product_name TEXT,
    product_amount NUMERIC,
    product_inventory INT
);