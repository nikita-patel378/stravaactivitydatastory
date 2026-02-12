from baml_client import b
from baml_client.types import ShoeMileageQuery, RunSummaryQuery
import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    return psycopg.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

def handle_shoe_mileage(query: ShoeMileageQuery):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            sql = "SELECT * FROM shoe_mileage"
            conditions = []
            
            if query.active_only:
                conditions.append("isretired = false")
            if query.shoe_id:
                conditions.append(f"shoeid = {query.shoe_id}")
            
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            
            cur.execute(sql)
            results = cur.fetchall()
            
            output = "Shoe Mileage:\n"
            for row in results:
                output += f"- {row[1]} {row[2]}: {row[4]:.1f} miles\n"
            return output

def handle_run_summary(query: RunSummaryQuery):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            sql = """
                SELECT withdog, dogname, 
                       COUNT(*) as total_runs,
                       SUM(distance) as total_miles,
                       AVG(distance) as avg_distance,
                       AVG(EXTRACT(EPOCH FROM time) / 60 / distance) as avg_pace
                FROM activities
                WHERE type = 'Run'
                  AND distance > 0
                  AND date >= %s 
                  AND date < %s
                  AND withdog = %s
                GROUP BY withdog, dogname
            """
            params = [query.start_date, query.end_date, query.with_dog]
            
            cur.execute(sql, params)
            results = cur.fetchall()
            
            output = f"Run Summary ({query.start_date} to {query.end_date}):\n"
            for row in results:
                label = "With Laika" if row[0] else "Solo"
                output += f"{label}: {row[2]} runs, {row[3]:.1f} miles, avg pace: {row[5]:.2f} min/mi\n"
            return output

def main():
    print("Strava Agent started! Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # BAML extracts intent and parameters
        tool_response = b.SelectTool(user_input)

        # Route to appropriate handler
        if isinstance(tool_response, ShoeMileageQuery):
            result = handle_shoe_mileage(tool_response)
            print(f"Agent: {result}")
        
        elif isinstance(tool_response, RunSummaryQuery):
            result = handle_run_summary(tool_response)
            print(f"Agent: {result}")

if __name__ == "__main__":
    main()