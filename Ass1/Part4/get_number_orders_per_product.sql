SELECT product_category, COUNT(product_category) AS number_of_orders
FROM orders
GROUP BY product_category;