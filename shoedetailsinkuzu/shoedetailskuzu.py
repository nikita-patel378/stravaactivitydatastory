import kuzu

def main():
    # Create database
    db = kuzu.Database("shoes.kuzu")
    conn = kuzu.Connection(db)

    # Create schema
    conn.execute("CREATE NODE TABLE Shoe(Shoeid INT64 PRIMARY KEY, Brand STRING, Model STRING, Color STRING, Purpose STRING, Weight FLOAT)")
    conn.execute("CREATE NODE TABLE Offset(Value FLOAT PRIMARY KEY)")
    conn.execute("CREATE NODE TABLE Cushioning(Level STRING PRIMARY KEY)")
    conn.execute("CREATE REL TABLE Has_Offset(FROM Shoe TO Offset, Stackheight STRING)")
    conn.execute("CREATE REL TABLE Has_Cushioning(FROM Shoe TO Cushioning)")

    # Insert nodes
    conn.execute('COPY Shoe FROM "shoe.csv"')
    conn.execute('COPY Offset FROM "offset.csv"')
    conn.execute('COPY Cushioning FROM "cushioning.csv"')

    # Insert relationships
    conn.execute('COPY Has_Offset FROM "has_offset.csv"')
    conn.execute('COPY Has_Cushioning FROM "has_cushioning.csv"')

   # Query 
    print(conn.execute("""
    MATCH (s:Shoe)-[r:Has_Offset]->(o:Offset),
      (s)-[:Has_Cushioning]->(c:Cushioning)
    RETURN s.Shoeid AS Shoeid, s.Brand AS Brand, s.Model AS Model,
       o.Value AS OffsetValue, r.Stackheight,
       c.Level AS CushioningLevel
    ORDER BY Shoeid
    LIMIT 20;
    """).get_as_df())

if __name__ == "__main__":
    main()
