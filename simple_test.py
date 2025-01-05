import psycopg2

DATABASE_URL = "postgres://u14vkm48spnk8:p79ebb9c9258caa7fbbffbd789ce4afe43efcdd6500bbe85b93175c76cdf4eb32@ccpa7stkruda3o.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/de10rh74n4gdtm"

try:
    connection = psycopg2.connect(DATABASE_URL)
    print("Connection to the database was successful!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
