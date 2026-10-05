-- Query 1: Monthly Category Revenue
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    category;

-- Query 2: Region Revenue
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;

-- Query 3: Top 5 Resellers by Total Spend
SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING SUM(o.quantity * o.unit_price) > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- Query 4: Zero-Order Resellers
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region,
    COUNT(o.order_id) AS order_count
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name, r.region
HAVING COUNT(o.order_id) = 0;

-- Query 4B: COUNT(*) vs COUNT(order_id)
SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id, r.reseller_name;

-- Query 5: June Delivered Average Order Value (AOV)
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';