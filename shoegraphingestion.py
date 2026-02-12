"""
Shoe Knowledge Graph - Data Ingestion Script
=============================================
This script loads shoe data from CSV into Neo4j with automatic deduplication.

Requirements:
    pip install neo4j pandas

Usage:
    python shoe_graph_ingestion.py

Configuration:
    Update the NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD variables below
"""

import csv
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# ============================================
# CONFIGURATION
# ============================================
load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')                 
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')         
CSV_FILE = os.getenv('CSV_FILE') 


class ShoeGraphLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def create_constraints(self):
        """Create constraints to ensure data quality and performance"""
        constraints = [
            "CREATE CONSTRAINT shoe_id_unique IF NOT EXISTS FOR (s:Shoe) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT offset_value_unique IF NOT EXISTS FOR (o:Offset) REQUIRE o.value IS UNIQUE",
            "CREATE CONSTRAINT cushioning_level_unique IF NOT EXISTS FOR (c:Cushioning) REQUIRE c.level IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                session.run(constraint)
                print(f"✓ Created constraint: {constraint.split()[1]}")
    
    def load_shoes(self, csv_file):
        """Load shoe data from CSV"""
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            shoes = list(reader)
        
        with self.driver.session() as session:
            # Load Shoe nodes
            for shoe in shoes:
                shoe_id = f"{shoe['brand']}_{shoe['model'].replace(' ', '_')}"
                session.run("""
                    MERGE (s:Shoe {id: $id})
                    SET s.brand = $brand,
                        s.model = $model,
                        s.stackheight = $stackheight,
                        s.weight = $weight,
                        s.purpose = $purpose
                """, 
                id=shoe_id,
                brand=shoe['brand'],
                model=shoe['model'],
                stackheight=shoe['stackheight'],
                weight=float(shoe['weight']) if shoe['weight'] != '0' else 0.0,
                purpose=shoe['purpose']
                )
            print(f"✓ Loaded {len(shoes)} shoe nodes")
            
            # Load Offset nodes
            offsets = set(int(shoe['offset']) for shoe in shoes)
            for offset in offsets:
                session.run("MERGE (o:Offset {value: $value})", value=offset)
            print(f"✓ Created {len(offsets)} offset nodes")
            
            # Load Cushioning nodes
            cushioning_levels = set(shoe['cushioning'] for shoe in shoes)
            for level in cushioning_levels:
                session.run("MERGE (c:Cushioning {level: $level})", level=level)
            print(f"✓ Created {len(cushioning_levels)} cushioning nodes")
            
            # Create HAS_OFFSET relationships
            for shoe in shoes:
                shoe_id = f"{shoe['brand']}_{shoe['model'].replace(' ', '_')}"
                session.run("""
                    MATCH (s:Shoe {id: $shoe_id})
                    MATCH (o:Offset {value: $offset})
                    MERGE (s)-[:HAS_OFFSET]->(o)
                """, 
                shoe_id=shoe_id,
                offset=int(shoe['offset'])
                )
            print(f"✓ Created HAS_OFFSET relationships")
            
            # Create HAS_CUSHIONING relationships
            for shoe in shoes:
                shoe_id = f"{shoe['brand']}_{shoe['model'].replace(' ', '_')}"
                session.run("""
                    MATCH (s:Shoe {id: $shoe_id})
                    MATCH (c:Cushioning {level: $level})
                    MERGE (s)-[:HAS_CUSHIONING]->(c)
                """, 
                shoe_id=shoe_id,
                level=shoe['cushioning']
                )
            print(f"✓ Created HAS_CUSHIONING relationships")
    
    def verify_data(self):
        """Verify the loaded data"""
        with self.driver.session() as session:
            # Count nodes
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY label
            """)
            print("\n📊 Node Counts:")
            for record in result:
                print(f"   {record['label']}: {record['count']}")
            
            # Count relationships
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(r) as count
                ORDER BY type
            """)
            print("\n🔗 Relationship Counts:")
            for record in result:
                print(f"   {record['type']}: {record['count']}")
            
            # Sample query
            result = session.run("""
                MATCH (s:Shoe)-[:HAS_OFFSET]->(o:Offset {value: 8})
                RETURN s.brand + ' ' + s.model as shoe
                ORDER BY shoe
                LIMIT 5
            """)
            print("\n🔍 Sample Query - Shoes with 8mm offset:")
            for record in result:
                print(f"   • {record['shoe']}")


def main():
    """Main execution function"""
    print("=" * 60)
    print("Shoe Knowledge Graph - Data Ingestion")
    print("=" * 60)
    
    # Check if CSV exists
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: CSV file not found: {CSV_FILE}")
        return
    
    # Initialize loader
    loader = ShoeGraphLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        print("\n1️⃣ Creating constraints...")
        loader.create_constraints()
        
        print(f"\n2️⃣ Loading data from {CSV_FILE}...")
        loader.load_shoes(CSV_FILE)
        
        print("\n3️⃣ Verifying data...")
        loader.verify_data()
        
        print("\n✅ Data ingestion completed successfully!")
        print("\nYou can now query your graph using Cypher or the Neo4j Browser.")
        
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
    finally:
        loader.close()


if __name__ == "__main__":
    main()
