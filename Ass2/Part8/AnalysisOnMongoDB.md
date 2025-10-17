Advantages:
    - Using a MongoDB for your analysis queries will result in better performance because it is optimized for reads from the database.
    - MongoDB supports horizontal scaling so if the volume of reads increases it is easy to expand its capacity to handle the reads.
Disadvantages:
    - We are now storing a copy of all the data so our storage costs will be increased
    - We now have to build and maintain an etl pipeline to move the data from the PostgreSQL to MongoDB
    - Since the pipeline will run periodically the data in MongoDB will not necessarily be the most up to date data