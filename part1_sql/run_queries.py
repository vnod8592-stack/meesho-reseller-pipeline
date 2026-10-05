import sqlite3
import csv
import os

DB_PATH = "data/meesho_reseller.db"
OUTPUT_DIR = "part1_sql/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Query 1
query1 = """
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
"""

# Query 2
query2 = """
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;
"""

# Query 3
query3 = """
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
"""

# Query 4
query4 = """
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
"""

# Query 5
query5 = """
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""


def save_query(query, output_file):
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    output_path = os.path.join(OUTPUT_DIR, output_file)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"Created: {output_path}")


save_query(query1, "monthly_category_revenue.csv")
save_query(query2, "region_revenue.csv")
save_query(query3, "top_resellers.csv")
save_query(query4, "zero_order_resellers.csv")
save_query(query5, "aov_june.csv")

conn.close()

print("\nAll Part 1 outputs created successfully.")