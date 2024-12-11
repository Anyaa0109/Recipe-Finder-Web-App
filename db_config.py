import cx_Oracle

def get_connection():
    try:
        connection = cx_Oracle.connect(
            "Ananya",  # Replace with your Oracle username
            "ananya",  # Replace with your Oracle password
            "BT-21051458:1521/XE"  # Replace with your Oracle host and service name
        )
        print("Connection successful!")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args  # Extract the error details
        print(f"Database connection error: {error.message}")
        return None

# Test connection
connection = get_connection()
if connection:
    cursor = connection.cursor()  # This line should now work
else:
    print("Failed to connect to the database.")
