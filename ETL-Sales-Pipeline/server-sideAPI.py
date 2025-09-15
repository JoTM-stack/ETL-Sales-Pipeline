#ETL SERVER + API
import pandas as pd
import sqlite3
from flask import Flask, jsonify, request
import os
import datetime

app = Flask(__name__)

DB_FILE = "sales.db"
CSV_FILE = "sales.csv"


# ------------------------ #
# 1. Extract & Transform
# ------------------------ #
def load_and_transform(csv_file):
    # Load CSV
    df = pd.read_csv(csv_file)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Drop rows with missing customer_id
    df.dropna(subset=["customer_id"], inplace=True)

    # Ensure correct data types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # Calculate total_price
    df["total_price"] = df["quantity"] * df["unit_price"]

    # Add unique ID
    df.reset_index(drop=True, inplace=True)
    df.insert(0, "id", df.index + 1)

    return df


# ------------------ #
# 2. Load into SQLite
# ------------------ #
def init_db(df, db_file=DB_FILE):
    with sqlite3.connect(db_file) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)


# ------------------ #
# Initialize DB
# ------------------ #
if os.path.exists(CSV_FILE):
    sales_df = load_and_transform(CSV_FILE)
    init_db(sales_df)
else:
    sales_df = pd.DataFrame()
    print(f"{CSV_FILE} not found! Start with empty database.")


# ------------------ #
# 3. Flask API Routes
# ------------------ #

# Home
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the ETL Sales API. Use /sales endpoints."})


# Get all sales
@app.route("/sales", methods=["GET"])
def get_sales():
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql("SELECT * FROM sales", conn)
    return jsonify(df.to_dict(orient="records"))


# Get sale by id
@app.route("/sales/<int:sale_id>", methods=["GET"])
def get_sale_by_id(sale_id):
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql("SELECT * FROM sales WHERE id=?", conn, params=(sale_id,))
    if df.empty:
        return jsonify({"error": "Sale not found"}), 404
    return jsonify(df.to_dict(orient="records"))


# Add new sale
@app.route("/sales", methods=["POST"])
def add_sale():
    new_sale = request.get_json()
    if not new_sale:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Validate required fields
    required = ["date", "customer_id", "product", "quantity", "unit_price"]
    for field in required:
        if field not in new_sale:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    # Calculate total_price
    new_sale["total_price"] = new_sale["quantity"] * new_sale["unit_price"]

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # Assign next id
        cursor.execute("SELECT MAX(id) FROM sales")
        max_id = cursor.fetchone()[0] or 0
        new_sale["id"] = max_id + 1

        keys = ", ".join(new_sale.keys())
        question_marks = ", ".join(["?"] * len(new_sale))
        values = tuple(new_sale.values())
        cursor.execute(f"INSERT INTO sales ({keys}) VALUES ({question_marks})", values)
        conn.commit()

    return jsonify({"message": "Sale Added Successfully", "data": new_sale}), 201


# Update sale by id
@app.route("/sales/<int:sale_id>", methods=["PUT"])
def update_sale(sale_id):
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Recalculate total_price if quantity/unit_price are updated
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        df = pd.read_sql("SELECT * FROM sales WHERE id=?", conn, params=(sale_id,))
        if df.empty:
            return jsonify({"error": "Sale not found"}), 404

        if "quantity" in update_data or "unit_price" in update_data:
            quantity = update_data.get("quantity", df.at[0, "quantity"])
            unit_price = update_data.get("unit_price", df.at[0, "unit_price"])
            update_data["total_price"] = quantity * unit_price

        columns = [f"{k}=?" for k in update_data.keys()]
        values = tuple(update_data.values()) + (sale_id,)
        cursor.execute(f"UPDATE sales SET {', '.join(columns)} WHERE id=?", values)
        conn.commit()

    return jsonify({"message": "Sale Updated Successfully", "data": update_data})


# Delete sale by id
@app.route("/sales/<int:sale_id>", methods=["DELETE"])
def delete_sale(sale_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales WHERE id=?", (sale_id,))
        deleted = cursor.rowcount
        conn.commit()

    if deleted == 0:
        return jsonify({"error": "Sale not found"}), 404
    return jsonify({"message": "Sale Deleted Successfully"})


# Export sales to CSV or Excel
@app.route("/sales/export/<string:format>", methods=["GET"])
def export_sales(format):
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql("SELECT * FROM sales", conn)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if format.lower() == "csv":
        filename = f"sales_export_{timestamp}.csv"
        df.to_csv(filename, index=False)
        return jsonify({"message": f"Exported to {filename}"})
    elif format.lower() == "excel":
        filename = f"sales_export_{timestamp}.xlsx"
        df.to_excel(filename, index=False)
        return jsonify({"message": f"Exported to {filename}"})
    else:
        return jsonify({"error": "Invalid format. Use 'csv' or 'excel'"}), 400


# ------------------ #
# Run App
# ------------------ #
if __name__ == "__main__":
    app.run(debug=True)
