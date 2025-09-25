SELECT order_id, orders.customer_id, customers.name AS customer_name, order_date, total_amount, product_id, product_category, product_name
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
WHERE customers.name = 'Alice Johnson';