-- Insert users into the User table
INSERT INTO shop_user (username, password) VALUES
('John Doe', 'mdp1'),
('Jane Smith', 'mdp2'),
('Alice Johnson', 'mdp3'),
('Bob Brown', 'mdp4'),
('Charlie Davis', 'mdp5');

-- Insert products into the Product table
INSERT INTO shop_product (name, description, price) VALUES
('Smartphone', 'Latest model with 6.5-inch screen and 128GB storage', 700),
('Laptop', 'High performance laptop with 16GB RAM and 512GB SSD', 1000),
('Headphones', 'Noise-canceling over-ear headphones', 150),
('Keyboard', 'Mechanical keyboard with RGB lighting', 80),
('Mouse', 'Wireless gaming mouse', 40);

-- Insert payments into the Payment table
INSERT INTO shop_payment (user_id, product_id, order_date, comment) VALUES
(1, 1, '2025-03-20', 'tsara ilay entana'),
(2, 2, '2025-03-21', 'ratsy izy'),
(3, 3, '2025-03-22', 'tsy ratsy'),
(4, 4, '2025-03-23', 'tena tsara'),
(5, 5, '2025-03-24', 'misy olana');
