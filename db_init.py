import mysql.connector
from getpass import getpass
import os

def initialize_database():
    # Get database connection details
    host = input("Enter MySQL host (default: localhost): ") or "127.0.0.1"
    user = input("Enter MySQL username (default: root): ") or "root"
    password = getpass("Enter MySQL password: ") or "Venkat2834.p"
    db_name = input("Enter database name (default: pet_connect): ") or "pet_connect"
    
    try:
        # Connect to MySQL (without database)
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")
        
        # Switch to the database
        cursor.execute(f"USE {db_name}")
        
        # Read the SQL file
        with open('schema.sql', 'r') as file:
            sql_script = file.read()
        
        # Execute each statement in the SQL file
        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    conn.commit()
                except mysql.connector.Error as err:
                    print(f"Error executing statement: {err}")
                    print(f"Statement: {statement}")
        
        print("Database schema and data initialized successfully!")
        
        # Generate a random secret key
        import secrets
        secret_key = secrets.token_hex(16)
        
        # Save connection details to a configuration file
        with open('.env', 'w') as env_file:
            env_file.write(f"MYSQL_HOST={host}\n")
            env_file.write(f"MYSQL_USER={user}\n")
            env_file.write(f"MYSQL_PASSWORD={password}\n")
            env_file.write(f"MYSQL_DB={db_name}\n")
            env_file.write(f"SECRET_KEY={secret_key}\n")
        
        print("Connection details saved to .env file")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    # Rename PetConnect_Group2.sql to schema.sql if it exists
    if os.path.exists('PetConnect_Group2.sql') and not os.path.exists('schema.sql'):
        os.rename('PetConnect_Group2.sql', 'schema.sql')
        print("Renamed PetConnect_Group2.sql to schema.sql")
    
    # Check if schema.sql exists
    if not os.path.exists('schema.sql'):
        print("Error: schema.sql file not found!")
        exit(1)
    
    initialize_database()