Payments Table
Payment_id - Primary Key for the Payments Table with unique ID
Order_id - Foreign Key to link a Payment to an Order
Payment_amount - Total amount that is going to be charged. Could include additional fees not seen in the order cost
Payment_type - Type of payment used for transaction(Credit Card, Paypal)
Payment_status - Current status of the payment(Paid, Outstanding, Failed, Refunded)
Payment_date - Timestamp of when Payment was issued

Products Table
Product_id - Primary Key for the Products Table with unique ID
Product_category - Category of the product that it belongs to
Product_name - Name of the product
Product_amount - Base price of the product. Allows order to have a different price for sales and discounts.
Product_inventory - Amount of the product is currently in inventory

Changes to Current Tables
Orders:
Move product_category and product_name to the Products table
Make product_id a foreign key reference to the product_id PK in Products table
