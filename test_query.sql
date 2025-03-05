SELECT 
    u.user_id,
    u.username,
    u.email,
    o.order_id,
    o.product_name,
    o.order_date
FROM 
    `project.dataset.users` u
INNER JOIN 
    `project.dataset.orders` o ON u.user_id = o.user_id
WHERE 
    o.order_date > '2023-01-01';
