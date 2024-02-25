-- Create the database
CREATE DATABASE tshirts;

-- Connect to the created database
\c tshirts;

-- Create the t_shirts table
CREATE TABLE t_shirts (
  t_shirt_id SERIAL PRIMARY KEY,
  brand VARCHAR(50) CHECK (brand IN ('Van Huesen', 'Levi', 'Nike', 'Adidas')) NOT NULL,
  color VARCHAR(50) CHECK (color IN ('Red', 'Blue', 'Black', 'White')) NOT NULL,
  size VARCHAR(2) CHECK (size IN ('XS', 'S', 'M', 'L', 'XL')) NOT NULL,
  price INT CHECK (price BETWEEN 10 AND 50),
  stock_quantity INT NOT NULL,
  CONSTRAINT brand_color_size UNIQUE (brand, color, size)
);

-- Create the discounts table
CREATE TABLE discounts (
  discount_id SERIAL PRIMARY KEY,
  t_shirt_id INT NOT NULL,
  pct_discount DECIMAL(5,2) CHECK (pct_discount BETWEEN 0 AND 100),
  FOREIGN KEY (t_shirt_id) REFERENCES t_shirts(t_shirt_id)
);

-- Data insertion in t_shirts table
INSERT INTO t_shirts (brand, color, size, price, stock_quantity)
VALUES 
  ('Van Huesen', 'Red', 'XS', 20, 50),
  ('Levi', 'Blue', 'S', 25, 40),
  ('Nike', 'Black', 'M', 30, 60),
  ('Adidas', 'White', 'L', 35, 45),
  ('Van Huesen', 'Red', 'XL', 40, 55),
  ('Levi', 'Blue', 'XS', 20, 50),
  ('Nike', 'Black', 'S', 25, 40),
  ('Adidas', 'White', 'M', 30, 60),
  ('Van Huesen', 'Red', 'L', 35, 45),
  ('Levi', 'Blue', 'XL', 40, 55);

-- Data insertion in discounts table
INSERT INTO discounts (t_shirt_id, pct_discount)
VALUES
  (1, 10.00),
  (2, 15.00),
  (3, 20.00),
  (4, 5.00),
  (5, 25.00),
  (6, 10.00),
  (7, 30.00),
  (8, 35.00),
  (9, 40.00),
  (10, 45.00);
