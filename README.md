# Strava Activity Data Tracking

## 📌 Motivation
After adopting my dog, I realized I needed to keep track of my shoe mileage to prevent unintended foot injuries.  

What started as simple shoe tracking became much more:
- Monitoring activities I do with my dog (walks, hikes, runs).
- Tracking my training as a marathoner, including race paces and split analysis.
- Adding shoe details into a **graph database** to visualize patterns in my shoe choices.

This project combines storytelling and data: it helps me understand my own training while capturing the journey I’ve shared with my dog. 🐶🏃‍♀️

---

## ⚙️ Tech Stack
- **Python**
- **Strava API**
- **PostgreSQL**
- **Kùzu (Graph Database)** (Archived)
- **Neo4j (Graph Database)**
- **BAML**

---

## 🚀 Features
- **Data Extraction**: Pulls activity data from the Strava API.
- **ETL Pipeline**: Cleans and loads structured data into PostgreSQL.
- **Shoe Mileage Tracking**: Tracks mileage per shoe to prevent overuse injuries.
- **Activity Insights**: Separates activities with my dog vs. solo marathon training.
- **Graph Visualization**: Stores shoe details in Kùzu to analyze shoe usage patterns.
- **Tool Calling: Uses BAML to use natural language for postgres queries for run summaries and shoe mileage.
 

---

## 🛠️ Requirements
- Python 3.x  
- PostgreSQL  
- [Strava API credentials](https://developers.strava.com/docs/getting-started/)
- Neo4j
- BAML by BoundaryML

---

## 💡 Why This Project Matters
- **Prevent injuries** by retiring shoes at the right mileage.  
- **Training insights** for marathon prep (track pace trends, splits, and race progress).  
- **Dog vs. solo activities** (quickly filter and compare my adventures with my dog vs. personal training).  
- **Graph insights** to see patterns in brands, models, and how I choose shoes over time.  

---

## ❤️ Acknowledgments
- [Strava API](https://developers.strava.com/) for providing activity data.  
- My dog, Laika, for inspiring this project. 🐾

