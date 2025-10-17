/* global use, db */
use('sales_db');

db.orders_summary.aggregate([
  {
    $group: {
      _id: "$customer_id",
      cities: { $addToSet: "$customer_city" }
    }
  },
  {
    $project: {
      _id: 0,
      customer_id: "$_id",
      number_of_cities: { $size: "$cities" }
    }
  }
])


