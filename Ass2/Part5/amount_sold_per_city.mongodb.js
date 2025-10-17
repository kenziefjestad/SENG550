/* global use, db */
use('sales_db');

db.orders_summary.aggregate([
  {
    $group: {
      _id: "$customer_city",
      total_amount_sold: { $sum: "$amount" }
    }
  },
  {
    $project: {
      _id: 0,
      city: "$_id",
      total_amount_sold: 1
    }
  }
])
