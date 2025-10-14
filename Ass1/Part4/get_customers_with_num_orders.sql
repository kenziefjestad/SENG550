SELECT customers.customer_id, customers.name, COUNT(orders.order_id) AS number_of_orders
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.customer_id, customers.name
HAVING COUNT(orders.order_id) >= 0;