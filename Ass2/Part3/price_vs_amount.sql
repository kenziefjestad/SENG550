-- Active: 1757967526180@@127.0.0.1@5432@assignment2
SELECT SUM(p.price - o.amount) AS total_price_difference
FROM fact_orders o
JOIN dim_products p
    ON o.product_id = p.id
    AND o.order_date BETWEEN p.start_date AND p.end_date