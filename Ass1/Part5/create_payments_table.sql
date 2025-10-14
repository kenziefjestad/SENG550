CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    payment_amount NUMERIC,
    payment_type TEXT,
    payment_status TEXT NOT NULL,
    payment_date DATE
);