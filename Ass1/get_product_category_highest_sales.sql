SELECT product_category, SUM(total_amount) AS total_sales
FROM orders
GROUP BY product_category
ORDER BY total_sales DESC
LIMIT 1;