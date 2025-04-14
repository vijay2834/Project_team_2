# routes/__init__.py
import MySQLdb.cursors
import traceback

# Global MySQL instance
mysql_instance = None

def init_app(mysql):
    """Initialize the module with the MySQL instance"""
    global mysql_instance
    mysql_instance = mysql

def get_db_cursor():
    """Get a database cursor with dictionary results"""
    global mysql_instance
    
    try:
        if mysql_instance is None:
            raise RuntimeError("MySQL not initialized. Call init_app first.")
        
        return mysql_instance.connection.cursor(MySQLdb.cursors.DictCursor)
    except Exception as e:
        error_msg = f"Database connection error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise RuntimeError(f"Failed to connect to database: {str(e)}") from e

def execute_query(query, params=None):
    """Execute a query and commit changes"""
    cursor = get_db_cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        mysql_instance.connection.commit()
        last_id = cursor.lastrowid
        return last_id
    except Exception as e:
        mysql_instance.connection.rollback()
        print(f"Query execution error: {str(e)}\nQuery: {query}\nParams: {params}")
        raise
    finally:
        cursor.close()

def fetch_one(query, params=None):
    """Execute a query and fetch one result"""
    cursor = get_db_cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        return cursor.fetchone()
    except Exception as e:
        print(f"Query fetch error: {str(e)}\nQuery: {query}\nParams: {params}")
        raise
    finally:
        cursor.close()

def fetch_all(query, params=None):
    """Execute a query and fetch all results"""
    cursor = get_db_cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        return cursor.fetchall()
    except Exception as e:
        print(f"Query fetch error: {str(e)}\nQuery: {query}\nParams: {params}")
        raise
    finally:
        cursor.close()