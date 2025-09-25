SELECT orders.order_id, order_date, total_amount, customer_id, product_category, product_name, deliveries.status
FROM orders
JOIN deliveries ON orders.order_id = deliveries.order_id
WHERE deliveries.status != 'Delivered';