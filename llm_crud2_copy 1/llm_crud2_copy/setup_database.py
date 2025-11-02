import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import Config

def create_database():
    """Create the database if it doesn't exist"""
    config = Config()
    
    try:
        # Connect to PostgreSQL server (not to specific database)
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database='postgres'  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{config.DB_NAME}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {config.DB_NAME}")
            print(f"✅ Database '{config.DB_NAME}' created successfully")
        else:
            print(f"ℹ️ Database '{config.DB_NAME}' already exists")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_sample_tables():
    """Create some sample tables for demonstration"""
    config = Config()
    
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                price DECIMAL(10,2),
                category VARCHAR(50),
                in_stock BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert sample data
        cursor.execute("""
            INSERT INTO users (name, email, age) VALUES
            ('John Doe', 'john@example.com', 30),
            ('Jane Smith', 'jane@example.com', 25),
            ('Bob Johnson', 'bob@example.com', 35)
            ON CONFLICT (email) DO NOTHING
        """)
        
        cursor.execute("""
            INSERT INTO products (name, price, category, in_stock) VALUES
            ('Laptop', 999.99, 'Electronics', TRUE),
            ('Mouse', 29.99, 'Electronics', TRUE),
            ('Desk Chair', 199.99, 'Furniture', FALSE)
            ON CONFLICT DO NOTHING
        """)
        
        print("✅ Sample tables and data created successfully")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample tables: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up database...")
    
    if create_database():
        if create_sample_tables():
            print("🎉 Database setup completed successfully!")
        else:
            print("⚠️ Database created but failed to create sample tables")
    else:
        print("❌ Failed to setup database")