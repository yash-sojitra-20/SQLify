few_shots = [
    {'Question' : "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer' : ''},
    
    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': '[(2000,)]'},
    
    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer': "[(Decimal('2960.00000000000000000000'),)]"} ,
    
     {'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
      'SQLResult': "Result of the SQL query",
      'Answer' : '[(4200,)]'},
    
    {'Question': "How many white color Levi's shirt I have?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : '[(None,)]'},

    {'Question': "show price of blue tshirt of levis with after applying discount.",
     'SQLQuery' : "SELECT price - (price * pct_discount / 100) AS discounted_price FROM t_shirts JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id WHERE brand = 'Levi' AND color = 'Blue'",
     'SQLResult': "Result of the SQL query",
     'Answer' : '[(21.2500000000000000,),(18.0000000000000000,),(22.0000000000000000,)]'},

    {
    'Question': "What is the original price of a red Adidas T-shirt in S size?",
    'SQLQuery': "SELECT price FROM t_shirts WHERE brand = 'Adidas' AND color = 'Red' AND size = 'S'",
    'SQLResult': "Result of the SQL query",
    'Answer': "[(35,)]"
    },

    {
    'Question': "How many black Nike T-shirts are currently in stock?",
    'SQLQuery': "SELECT stock_quantity FROM t_shirts WHERE brand = 'Nike' AND color = 'Black'",
    'SQLResult': "Result of the SQL query",
    'Answer': "[(60,)]"
    },

    {
    'Question': "What is the total discounted amount for all blue Levi's T-shirts in the current stock?",
    'SQLQuery': "SELECT SUM(price - (price * pct_discount / 100)) AS total_discounted_amount FROM t_shirts JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id WHERE brand = 'Levi' AND color = 'Blue'",
    'SQLResult': "Result of the SQL query",
    'Answer': "[(61.25,)]"
    },

    {
    'Question': "Show the brand, color, size, and total discounted amount for T-shirts with a stock quantity above 40 and a discount percentage greater than 15%.",
    'SQLQuery': "SELECT t.brand, t.color, t.size, SUM(t.price - (t.price * d.pct_discount / 100)) AS total_discounted_amount FROM t_shirts t JOIN discounts d ON t.t_shirt_id = d.t_shirt_id WHERE t.stock_quantity > 40 AND d.pct_discount > 15 GROUP BY t.brand, t.color, t.size",
    'SQLResult': "Result of the SQL query",
    'Answer': "[('Van Huesen', 'Red', 'XL', 68.00), ('Levi', 'Blue', 'S', 21.25), ('Adidas', 'White', 'M', 54.00)]"
    },

    {
    'Question': "What are the available sizes for black Nike T-shirts?",
    'SQLQuery': "SELECT DISTINCT size FROM t_shirts WHERE brand = 'Nike' AND color = 'Black'",
    'SQLResult': "Result of the SQL query",
    'Answer': "[('M',)]"
    },

    {
    'Question': "How many T-shirts do we have in total?",
    'SQLQuery': "SELECT SUM(stock_quantity) AS total_tshirts FROM t_shirts",
    'SQLResult': "Result of the SQL query",
    'Answer': "[(430,)]"
    },

    {
    'Question': "List the top 3 brands with the highest total discounted amount across all sizes and colors.",
    'SQLQuery': "SELECT t.brand, SUM(t.price - (t.price * d.pct_discount / 100)) AS total_discounted_amount FROM t_shirts t JOIN discounts d ON t.t_shirt_id = d.t_shirt_id GROUP BY t.brand ORDER BY total_discounted_amount DESC LIMIT 3",
    'SQLResult': "Result of the SQL query",
    'Answer': "[('Levi', 136.25), ('Adidas', 119.00), ('Van Huesen', 68.00)]"
    },

    {
    'Question': "What is the average stock quantity for each brand and color combination?",
    'SQLQuery': "SELECT t.brand, t.color, AVG(t.stock_quantity) AS average_stock_quantity FROM t_shirts t GROUP BY t.brand, t.color",
    'SQLResult': "Result of the SQL query",
    'Answer': "[('Van Huesen', 'Red', 48.333333333333336), ('Levi', 'Blue', 48.333333333333336), ('Nike', 'Black', 50.0), ('Adidas', 'White', 50.0)]"
    },

    {
    'Question': "Provide the brand, color, size, and total discounted amount for T-shirts with a stock quantity above 40 and a discount percentage greater than 15%, sorted by total discounted amount in descending order.",
    'SQLQuery': "SELECT t.brand, t.color, t.size, SUM(t.price - (t.price * d.pct_discount / 100)) AS total_discounted_amount FROM t_shirts t JOIN discounts d ON t.t_shirt_id = d.t_shirt_id WHERE t.stock_quantity > 40 AND d.pct_discount > 15 GROUP BY t.brand, t.color, t.size ORDER BY total_discounted_amount DESC",
    'SQLResult': "Result of the SQL query",
    'Answer': "[('Adidas', 'White', 'M', 54.00), ('Levi', 'Blue', 'S', 21.25), ('Van Huesen', 'Red', 'XL', 68.00)]"
    },

    {
    'Question': "What is the total stock quantity for each size and color of Nike T-shirts?",
    'SQLQuery': "SELECT t.color, t.size, SUM(t.stock_quantity) AS total_stock_quantity FROM t_shirts t WHERE t.brand = 'Nike' GROUP BY t.color, t.size",
    'SQLResult': "Result of the SQL query",
    'Answer': "[('Black', 'M', 90), ('Red', 'XL', 60)]"
    },

    {
    'Question': "What is the average price of Adidas T-shirts in each size?",
    'SQLQuery': "SELECT t.size, AVG(t.price) AS average_price FROM t_shirts t WHERE t.brand = 'Adidas' GROUP BY t.size",
    'SQLResult': "Result of the SQL query",
    'Answer': "[('L', 35.0), ('M', 30.0)]"
    },

    {
    'Question': "List the brands that have T-shirts available in all colors and sizes.",
    'SQLQuery': "SELECT t.brand FROM t_shirts t WHERE NOT EXISTS (SELECT DISTINCT color, size FROM t_shirts WHERE brand = t.brand EXCEPT SELECT t.color, t.size FROM t_shirts t WHERE t.brand = t.brand)",
    'SQLResult': "Result of the SQL query",
    'Answer': "[('Levi',)]"
    },

    {
    'Question': "Find the brand with the highest total discounted amount for T-shirts in the 'Black' color.",
    'SQLQuery': "SELECT t.brand, SUM(t.price - (t.price * d.pct_discount / 100)) AS total_discounted_amount FROM t_shirts t JOIN discounts d ON t.t_shirt_id = d.t_shirt_id WHERE t.color = 'Black' GROUP BY t.brand ORDER BY total_discounted_amount DESC LIMIT 1",
    'SQLResult': "Result of the SQL query",
    'Answer': "[('Nike', 90.0)]"
    },

    {
    'Question': "What is the maximum stock quantity for each brand of T-shirts?",
    'SQLQuery': "SELECT t.brand, MAX(t.stock_quantity) AS max_stock_quantity FROM t_shirts t GROUP BY t.brand",
    'SQLResult': "Result of the SQL query",
    'Answer': "[('Van Huesen', 55), ('Levi', 55), ('Nike', 60), ('Adidas', 60)]"
    }
]
