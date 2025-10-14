SELECT customers.customer_id, customers.name, SUM(orders.total_amount) AS total_spent
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.customer_id
ORDER BY total_spent DESC;