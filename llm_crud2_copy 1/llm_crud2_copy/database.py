import psycopg2
import pandas as pd
from typing import List, Dict, Any, Optional
from config import Config

class DatabaseManager:
    def __init__(self):
        self.config = Config()
        self.connection = None
        
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD
            )
            self.connection.autocommit = True
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        if not self.connection:
            if not self.connect():
                return {"success": False, "error": "Failed to connect to database"}
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            
            if query.strip().upper().startswith(('SELECT', 'WITH')):
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                df = pd.DataFrame(rows, columns=columns)
                return {"success": True, "data": df, "rows_affected": len(rows)}
            else:
                rows_affected = cursor.rowcount
                return {"success": True, "rows_affected": rows_affected}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            if cursor:
                cursor.close()
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        query = """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position;
        """
        return self.execute_query(query, (table_name,))
    
    def get_all_tables(self) -> Dict[str, Any]:
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
        return self.execute_query(query)
    
    def test_connection(self) -> bool:
        try:
            result = self.execute_query("SELECT 1 as test")
            return result["success"]
        except:
            return False