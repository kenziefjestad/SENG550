SELECT city, SUM(amount) AS total_amount_sold
FROM fact_orders
JOIN dim_customers ON fact_orders.customer_id = dim_customers.id
GROUP BY city;