import pandas as pd
import os
from database import DatabaseManager
from typing import Dict, Any, List

class CSVImporter:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.data_folder = "data"
    
    def get_csv_files(self) -> List[str]:
        """Get list of CSV files in data folder"""
        if not os.path.exists(self.data_folder):
            return []
        
        csv_files = []
        for file in os.listdir(self.data_folder):
            if file.endswith('.csv'):
                csv_files.append(file)
        return csv_files
    
    def analyze_csv(self, filename: str) -> Dict[str, Any]:
        """Analyze CSV file structure"""
        filepath = os.path.join(self.data_folder, filename)
        
        try:
            # Read first few rows to analyze structure
            df = pd.read_csv(filepath, nrows=5)
            
            # Infer PostgreSQL data types
            column_info = []
            for col in df.columns:
                dtype = df[col].dtype
                sample_values = df[col].dropna().head(3).tolist()
                
                # Map pandas dtypes to PostgreSQL types
                if dtype == 'int64':
                    pg_type = 'INTEGER'
                elif dtype == 'float64':
                    pg_type = 'DECIMAL(10,2)'
                elif dtype == 'bool':
                    pg_type = 'BOOLEAN'
                elif dtype == 'datetime64[ns]':
                    pg_type = 'TIMESTAMP'
                else:
                    # For strings, estimate length
                    max_len = df[col].astype(str).str.len().max()
                    if max_len <= 50:
                        pg_type = 'VARCHAR(100)'
                    elif max_len <= 255:
                        pg_type = 'VARCHAR(255)'
                    else:
                        pg_type = 'TEXT'
                
                column_info.append({
                    'name': col,
                    'type': pg_type,
                    'sample_values': sample_values
                })
            
            # Get total row count
            total_rows = len(pd.read_csv(filepath))
            
            return {
                'success': True,
                'filename': filename,
                'columns': column_info,
                'total_rows': total_rows,
                'sample_data': df.to_dict('records')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_table_from_csv(self, filename: str, table_name: str = None) -> Dict[str, Any]:
        """Create PostgreSQL table from CSV structure"""
        if not table_name:
            table_name = filename.replace('.csv', '').lower()
        
        analysis = self.analyze_csv(filename)
        if not analysis['success']:
            return analysis
        
        # Generate CREATE TABLE SQL
        columns_sql = []
        for col in analysis['columns']:
            col_name = col['name'].lower().replace(' ', '_')
            col_type = col['type']
            columns_sql.append(f"{col_name} {col_type}")
        
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(columns_sql)}
        );
        """
        
        # Execute CREATE TABLE
        result = self.db_manager.execute_query(create_sql)
        
        if result['success']:
            return {
                'success': True,
                'table_name': table_name,
                'sql': create_sql,
                'columns': analysis['columns']
            }
        else:
            return result
    
    def import_csv_to_table(self, filename: str, table_name: str = None) -> Dict[str, Any]:
        """Import CSV data into PostgreSQL table"""
        if not table_name:
            table_name = filename.replace('.csv', '').lower()
        
        filepath = os.path.join(self.data_folder, filename)
        
        try:
            # Read CSV file
            df = pd.read_csv(filepath)
            
            # Clean column names
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            
            # Create table first
            create_result = self.create_table_from_csv(filename, table_name)
            if not create_result['success']:
                return create_result
            
            # Import data in batches
            batch_size = 1000
            total_imported = 0
            
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                
                # Generate INSERT SQL
                columns = ', '.join(batch.columns)
                placeholders = ', '.join(['%s'] * len(batch.columns))
                insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                # Convert batch to list of tuples
                values = [tuple(row) for row in batch.values]
                
                # Execute batch insert
                for row_values in values:
                    result = self.db_manager.execute_query(insert_sql, row_values)
                    if result['success']:
                        total_imported += 1
                    else:
                        print(f"Error importing row: {result['error']}")
            
            return {
                'success': True,
                'table_name': table_name,
                'total_rows': len(df),
                'imported_rows': total_imported,
                'message': f"Successfully imported {total_imported} rows into {table_name}"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_imported_tables(self) -> Dict[str, Any]:
        """List all tables that were imported from CSV"""
        return self.db_manager.get_all_tables()

def main():
    """Interactive CSV importer"""
    importer = CSVImporter()
    
    print("🗃️ CSV to PostgreSQL Importer")
    print("=" * 40)
    
    # List available CSV files
    csv_files = importer.get_csv_files()
    if not csv_files:
        print("❌ No CSV files found in 'data' folder")
        return
    
    print("📁 Available CSV files:")
    for i, file in enumerate(csv_files, 1):
        print(f"  {i}. {file}")
    
    try:
        choice = int(input("\nSelect file number: ")) - 1
        if choice < 0 or choice >= len(csv_files):
            print("❌ Invalid selection")
            return
        
        selected_file = csv_files[choice]
        print(f"\n📊 Analyzing {selected_file}...")
        
        # Analyze CSV
        analysis = importer.analyze_csv(selected_file)
        if not analysis['success']:
            print(f"❌ Error analyzing CSV: {analysis['error']}")
            return
        
        print(f"✅ Found {analysis['total_rows']} rows with {len(analysis['columns'])} columns:")
        for col in analysis['columns']:
            print(f"  - {col['name']}: {col['type']}")
        
        # Ask for table name
        default_table = selected_file.replace('.csv', '').lower()
        table_name = input(f"\nTable name (default: {default_table}): ").strip()
        if not table_name:
            table_name = default_table
        
        # Import data
        print(f"\n🚀 Importing data into '{table_name}' table...")
        result = importer.import_csv_to_table(selected_file, table_name)
        
        if result['success']:
            print(f"✅ {result['message']}")
            print(f"📊 Table '{table_name}' is ready for queries!")
        else:
            print(f"❌ Import failed: {result['error']}")
    
    except KeyboardInterrupt:
        print("\n👋 Import cancelled")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()