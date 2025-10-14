SELECT 
c.customer_id, o.order_id, o.order_date, c.city AS customer_city, p.name AS product_name, p.price AS product_price, o.amount
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.id
JOIN dim_products p ON o.product_id = p.id
WHERE c.customer_id = 'C1';