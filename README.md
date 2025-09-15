# ETL Sales Pipeline — Full Documentation

This document explains all tools, packages, programming languages, database queries, and step-by-step operation of the ETL-Sales-Pipeline project.

---

## 1. Tools & Technologies Used

### Languages

* **Python** — main language for ETL and API development.
* **SQL** — used for database queries.

### Frameworks & Libraries

* **Flask** — lightweight web framework for building the API.
* **Pandas** — data manipulation and transformation.
* **Requests** — used in client scripts to interact with the API.
* **SQLite/MySQL** — database for storing and managing sales data.

### Package Management

* **pip** — installs dependencies from `requirements.txt`.

### Supporting Tools

* **Postman / curl / PowerShell Invoke-WebRequest** — testing API endpoints.

---

## 2. Database Schema

The database contains a **sales** table:

```sql
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    customer_id INTEGER NOT NULL,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL
);
```

---

## 3. SQL Queries Used & Their Roles

### 1. Insert a new sale

```sql
INSERT INTO sales (date, customer_id, product, quantity, unit_price)
VALUES (?, ?, ?, ?, ?);
```

**Role:** Adds new sales records into the database during the `POST` operation.

### 2. Retrieve all sales

```sql
SELECT * FROM sales;
```

**Role:** Extracts all data from the database for reporting and transformations (`GET all sales`).

### 3. Retrieve sales by customer ID

```sql
SELECT * FROM sales WHERE customer_id = ?;
```

**Role:** Filters sales specific to a customer (`GET by customer_id`).

### 4. Update a sale

```sql
UPDATE sales
SET date = ?, product = ?, quantity = ?, unit_price = ?
WHERE customer_id = ?;
```

**Role:** Updates existing sales records when a customer’s transaction needs correction (`PUT`).

### 5. Delete a sale

```sql
DELETE FROM sales WHERE customer_id = ?;
```

**Role:** Removes data from the system if invalid or requested (`DELETE`).

### 6. Aggregation query (example)

```sql
SELECT product, SUM(quantity) AS total_sold, SUM(quantity * unit_price) AS revenue
FROM sales
GROUP BY product;
```

**Role:** Generates reports on total items sold and revenue per product (used in reporting/analytics phase).

---

## 4. Operating the ETL Tool

### Step 1: Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/JoTM-stack/ETL-Sales-Pipeline.git
   cd ETL-Sales-Pipeline
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:

   ```bash
   python init_db.py
   ```

---

### Step 2: Run API Server

Run the Flask API server:

```bash
python server-sideApi.py
```

This will start the service at `http://127.0.0.1:5000/`.

---

### Step 3: Interact with the API

Use either **PowerShell**, **curl**, or **Postman**.

#### Add a new sale

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/sales" `
  -Method POST `
  -Body '{"date": "2025-09-14", "customer_id": 114, "product": "Furniture", "quantity": 50, "unit_price": 300000}' `
  -ContentType "application/json"
```

#### Fetch all sales

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/sales" -Method GET
```

#### Fetch by customer ID

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/sales/114" -Method GET
```

#### Update sale

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/sales/114" `
  -Method PUT `
  -Body '{"date": "2025-09-15", "product": "Electronics", "quantity": 30, "unit_price": 15000}' `
  -ContentType "application/json"
```

#### Delete sale

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/sales/114" -Method DELETE
```

---

## 5. ETL Workflow Explanation

1. **Extract** — Data is extracted from the API (raw JSON or direct SQL queries).
2. **Transform** — With Pandas, data is cleaned (e.g., convert dates, calculate revenue per sale `quantity * unit_price`).
3. **Load** — Cleaned/processed data is written back into the database or exported into CSV/Excel for analysis.

---

## 6. Example Data Transformation with Pandas

```python
import pandas as pd
import sqlite3

conn = sqlite3.connect("sales.db")
df = pd.read_sql_query("SELECT * FROM sales", conn)

# Add revenue column
df["revenue"] = df["quantity"] * df["unit_price"]

# Save cleaned dataset
df.to_csv("cleaned_sales.csv", index=False)
```

**Role:** This ensures raw sales data is enriched with business metrics.

---

## 7. Conclusion

* **SQL queries** power CRUD + reporting.
* **Python (Flask & Pandas)** automates ETL operations.
* **API layer** makes the pipeline interactive.
* **Transformations** prepare sales data for decision-making.

This makes the ETL-Sales-Pipeline a complete, reusable system for handling business sales data.
