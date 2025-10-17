/* global use, db */
use('sales_db');

db.orders_summary.find({"customer_id": "C1"})
