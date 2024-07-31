import mysql.connector.pooling

# create a connection pool
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3308,
    'database': 'agriguard',
    'raise_on_warnings': True
}

cnx_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "mypool",
    pool_size = 10,
    **db_config
)

