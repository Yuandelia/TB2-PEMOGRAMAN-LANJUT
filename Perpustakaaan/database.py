import MySQLdb

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '6Belastahun!',
    'db': 'Perpustakaaan',
}

# Create a connection to the database``
conn = MySQLdb.connect(**db_config)