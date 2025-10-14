SELECT
    o.order_id, SUM(p.price - o.amount) AS total_price_difference
FROM fact_orders o
JOIN dim_products p
    ON o.product_id = p.id
    AND o.order_date BETWEEN p.start_date AND p.end_date
GROUP BY o.order_id;