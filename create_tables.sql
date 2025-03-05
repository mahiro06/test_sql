CREATE TABLE `project.dataset.users` (
    user_id INT64,
    username STRING,
    email STRING,
    PRIMARY KEY(user_id)
);

CREATE TABLE `project.dataset.orders` (
    order_id INT64,
    user_id INT64,
    product_name STRING,
    order_date DATE,
    FOREIGN KEY (user_id) REFERENCES `project.dataset.users`(user_id)
);
