
WITH user_data AS (
    SELECT 
        user_id,
        username,
        email
    FROM 
        `project.dataset.users`
),
order_data AS (
    SELECT 
        order_id,
        user_id,
        product_name,
        order_date
    FROM 
        `project.dataset.orders`
),
product_data AS (
    SELECT 
        product_id,
        product_name,
        category
    FROM 
        `project.dataset.products`
),
category_data AS (
    SELECT 
        category_id,
        category_name
    FROM 
        `project.dataset.categories`
)
SELECT 
    u.user_id,
    u.username,
    u.email,
    o.order_id,
    o.product_name,
    o.order_date,
    p.category,
    c.category_name
FROM 
    user_data u
INNER JOIN 
    order_data o ON u.user_id = o.user_id
INNER JOIN 
    product_data p ON o.product_name = p.product_name
INNER JOIN 
    category_data c ON p.category = c.category_id
WHERE 
    o.order_date > '2023-01-01';
