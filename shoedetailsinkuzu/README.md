# Kùzu Graph Model for Shoe Data

## 🎯 Purpose
This section models running shoes in a **graph database** to highlight their biomechanical properties beyond brand marketing.  
Instead of grouping shoes by brand, the graph connects **Shoe** nodes with **Offset** and **Cushioning** nodes to show patterns across all brands.

---

## 🕸️ Graph Model

### Nodes
- **Shoe**
  - Properties: `shoe_id`, `brand`, `model`, `color`, `purpose`, `weight`
- **Offset**
  - Properties: `value` (e.g., `8mm`, `4mm`)
- **Cushioning**
  - Properties: `level` (e.g., `Light`, `Balanced`, `Max`)

### Relationships
- `(Shoe)-[:HAS_OFFSET]->(Offset)`  
  Connects a shoe to its heel-to-toe drop value.
  
- `(Shoe)-[:HAS_CUSHIONING]->(Cushioning)`  
  Connects a shoe to its cushioning level.


