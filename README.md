# ETL-Sales-Pipeline

**ETL Sales Pipeline** is a mini data engineering project that extracts raw sales data from a CSV file, transforms it with cleaning and total calculations, and loads it into a SQLite database. It provides a **REST API** for real-time CRUD operations and a **CLI tool** for easy navigation, updates, exports, and reporting.

This project demonstrates core **Data Engineering** concepts:
✅ Extract → Transform → Load
✅ Database integration
✅ REST API development
✅ CLI-based interaction & automation

---

## ⚙️ Features

### 🔄 ETL Pipeline (Python + Pandas + SQLite)

* Load and clean **CSV sales data**
* Calculate `total_price` = `quantity × unit_price`
* Store transformed data in a **SQLite database**

### 🌐 Flask REST API

* **GET** `/sales` → Fetch all sales
* **GET** `/sales/<customer_id>` → Fetch sales by customer
* **POST** `/sales` → Add a new sale
* **PUT** `/sales/<customer_id>` → Update existing sale
* **DELETE** `/sales/<customer_id>` → Delete sale
* **GET** `/sales/export/<csv|excel>` → Export sales data

### 🖥️ CLI Tool (`etl_tool.py`)

* Interactive menu for API calls:

  1. GET all sales
  2. GET sale by `customer_id`
  3. POST (add new sale)
  4. PUT (update sale by `customer_id`)
  5. DELETE sale by `customer_id`
  6. Export sales (CSV or Excel)

### ⚡ Package Manager (`packager.py`)

* Install Python dependencies
* Manage package collections
* Check outdated packages & update

---

## 🛠️ Tech Stack

**Languages**

* Python 3
* PowerShell
* Batch (CMD)

**Python Packages**

* `pandas` → Data cleaning & transformation
* `flask` → REST API
* `sqlite3` → Database integration
* `requests` → API requests (CLI tool)
* `tabulate` → Pretty table output in CLI
* `colorama` → Colored terminal output

**External Tools**

* `Invoke-WebRequest` (PowerShell) → API client
* `curl` (CMD) → API client

---

## 🚀 Setup & Run

### 1️⃣ Install Dependencies

1. Open **`packager.py`**
2. Run the script:

   ```bash
   python packager.py
   ```
3. In the menu, select **option 2** → Install packages from file
4. Ensure you have a `packages.txt` file listing all required dependencies.

---

### 2️⃣ Run the ETL Pipeline

* Run via PowerShell, CMD, or IDE:

  ```bash
  python etl_pipeline.py
  ```
* The pipeline will:

  * Extract and clean data from `sales.csv`
  * Compute `total_price`
  * Load the data into `sales.db` (SQLite database)
  * Start the **Flask API server** automatically

---

### 3️⃣ Access the Server

* Open in your browser:
  👉 [http://127.0.0.1:5000/sales](http://127.0.0.1:5000/sales)

* Or use the CLI tool (`etl_tool.py`) for interactive management.
  Example:

  ```bash
  python etl_tool.py
  ```

---

### 4️⃣ Manage Sales Data

The CLI tool supports:

* View sales
* Add/update/delete records
* Export data to **CSV** or **Excel**

---

## ⚠️ Important Notes

* The **database cannot be accessed** if the Flask server is **not running**.
* Ensure `sales.csv` exists before starting the ETL pipeline.
* Use `etl_tool.py` or direct API requests for CRUD operations.

---

## 📂 Project Structure

```
ETL-Sales-Pipeline/
│── etl_pipeline.py        # Main ETL pipeline (Extract → Transform → Load + Server trigger)
│── server-sideAPI.py      # Flask REST API
│── etl_tool.py            # CLI manager for sales database
│── packager.py            # Package manager utility
│── sales.csv              # Source data (raw sales)
│── sales.db               # SQLite database (auto-generated)
│── packages.txt           # Required dependencies
```

---

## 📖 Example Workflow

1. Install packages with `packager.py` (option 2 → from file).
2. Run `etl_pipeline.py` to process data and start the API server.
3. Open browser → `http://127.0.0.1:5000/sales` OR run `etl_tool.py`.
4. Manage sales with CRUD + export features.
5. Stop the pipeline with `CTRL + C`.
