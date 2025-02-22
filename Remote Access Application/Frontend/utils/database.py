import mariadb

# Database connection parameters
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "ztna"
}

def get_connection():
    """Establish and return a MariaDB connection."""
    try:
        conn = mariadb.connect(**DB_CONFIG)
        cursor= conn.cursor
        return conn,cursor
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

def test_connection():
    """Test database connection and fetch users."""
    conn = get_connection()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        print("Connected to MariaDB successfully!")
        cursor.execute("SELECT * FROM users;")
        for row in cursor.fetchall():
            print(row)
    except mariadb.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
        print("Connection closed.")
