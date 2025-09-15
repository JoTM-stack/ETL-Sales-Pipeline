#ETL Pipeline
import pandas as pd
import sqlite3
import subprocess
import time


from sympy.codegen.ast import break_

def print_dashes(count=80):
    for _ in range(count):
        print("=", end="")
    print()

limit = 10000000



# ------------------ #
# 1. Extract
# ------------------ #
# Read data from a CSV file (simulate source system)
sales_data = pd.read_csv("sales.csv")
print_dashes()
print("                              Mini ETL Pipeline")
print_dashes()
print("Raw Data:")
print(sales_data.head(limit))



# ------------------ #
# 2. Transform
# ------------------ #
# Clean & process data
# Example transformations:
# - Handle missing values
# - Calculate new column
# - Convert date to datetime format
sales_data.dropna(subset=["customer_id"], inplace=True) # drop rows with missing customer_id
try:
    sales_data["total_price"] = sales_data["quantity"] * sales_data["unit_price"]
except KeyError:
    print_dashes()

sales_data["date"] = pd.to_datetime(sales_data["date"], errors="coerce")
print("Transformed Data:")
print(sales_data.head(limit))
print_dashes()


# ------------------ #
# 3. Load
# ------------------
# Store into SQLite (local database)
conn = sqlite3.connect("sales.db")
sales_data.to_sql("sales", conn, if_exists="replace", index=False)

print("Data loaded into 'sales.db' SQLite database successfully!")
print_dashes()
# Optional: Query back to check

result = pd.read_sql(f"SELECT * FROM sales LIMIT {limit};", conn)
print("Loaded Data Preview:")
print(result)

def run_server():
    # Start server_sideapi.py
    return subprocess.Popen(["python", "server-sideAPI.py"])

if __name__ == "__main__":
    server = run_server()
    print_dashes()
    print("Data logged into the database Successfully.\nStarting The Server...\n----------------------[The Server Is Running!]-------------------")

    try:
        # Keep script alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server.terminate()