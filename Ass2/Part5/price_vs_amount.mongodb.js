/* global use, db */
use('sales_db');

db.orders_summary.aggregate([
  {
    $project: {
      difference: { $subtract: ["$product_price", "$amount"] }
    }
  },
  {
    $group: {
      _id: null,
      total_difference: { $sum: "$difference" }
    }
  },
  {
    $project: { _id: 0 }
  }
])
