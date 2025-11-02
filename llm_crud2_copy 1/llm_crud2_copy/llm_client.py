# llm_client.py

import re
from typing import Dict, Any
from config import Config
from groq import Groq  # Import Groq instead of openai

class LLMClient:
    def __init__(self):
        self.config = Config()
        # Initialize the Groq client
        self.client = Groq(
            api_key=self.config.GROQ_API_KEY,
        )
    
    def generate_sql(self, user_query: str, schema_info: str = "") -> Dict[str, Any]:
        system_prompt = f"""You are a PostgreSQL SQL generator. Convert natural language to valid SQL.

Schema: {schema_info}

IMPORTANT: Return ONLY the SQL statement, nothing else. No explanations, no formatting, no tags.

Examples:
Input: "show all users"
Output: SELECT * FROM users;

Input: "delete first row from users" 
Output: DELETE FROM users WHERE ctid = (SELECT ctid FROM users LIMIT 1);

Input: "create table products with id and name"
Output: CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(255));

Generate only valid PostgreSQL SQL:"""

        try:
            response = self.client.chat.completions.create(
                # Use the Groq model from config
                model=self.config.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up the response - remove various formatting
            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:]
            if sql_query.startswith("```"):
                sql_query = sql_query[3:]
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]
            
            sql_query = re.sub(r'<[^>]+>', '', sql_query)
            sql_query = sql_query.strip()
            
            lines = sql_query.split('\n')
            sql_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#') and not line.startswith('--')]
            
            if sql_lines:
                sql_query = ' '.join(sql_lines)
            
            if not sql_query or len(sql_query.strip()) < 5:
                return {
                    "success": False,
                    "error": "LLM returned empty or invalid SQL response"
                }
            
            return {
                "success": True,
                "sql": sql_query,
                "explanation": f"Generated SQL for: {user_query}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"LLM Error: {str(e)}"
            }
    
    def explain_query(self, sql_query: str) -> str:
        try:
            response = self.client.chat.completions.create(
                # Use the Groq model from config
                model=self.config.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "Explain this SQL query in simple terms:"},
                    {"role": "user", "content": sql_query}
                ],
                temperature=0.1,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return "Could not generate explanation"