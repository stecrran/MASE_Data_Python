from sqlalchemy import create_engine, inspect, text
import logging


def test_db_connection():
    # Enable SQLAlchemy logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # Database connection details
    host = "db.relational-data.org"
    user = "guest"
    password = "relational"
    port = 3306
    database = "financial"

    # Create the connection string
    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    # Connect to the database
    try:
        engine = create_engine(connection_string)
        connection = engine.connect()
        print("Connection successful!")

        # Inspect the database
        inspector = inspect(engine)

        # Print the default schema
        current_schema = connection.execute(text("SELECT DATABASE();")).fetchone()
        print(f"Current database/schema: {current_schema[0]}")

        # List all schemas
        schemas = inspector.get_schema_names()
        print("\nAvailable schemas:")
        for schema in schemas:
            print(f" - {schema}")

        # List tables in the current schema
        tables = inspector.get_table_names(schema=current_schema[0])
        print(f"\nTables in the current schema ({current_schema[0]}):")
        for table in tables:
            print(f" - {table}")

        # List tables in all schemas (optional)
        print("\nTables in all schemas:")
        for schema in schemas:
            tables = inspector.get_table_names(schema=schema)
            print(f"\nSchema: {schema}")
            for table in tables:
                print(f"  - {table}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Dispose of the connection
        if 'connection' in locals():
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    test_db_connection()
