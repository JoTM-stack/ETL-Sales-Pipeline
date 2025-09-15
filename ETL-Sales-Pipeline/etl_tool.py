import os
from tabulate import tabulate
import requests
import json
import subprocess

BASE_URL = "http://127.0.0.1:5000/sales"
def print_dashes(count=80):
    for _ in range(count):
        print("=", end="")
    print()

def spacing(count=35):
    for _ in range(count):
        print(" ", end="")


def print_menu():
    print_dashes()
    spacing()
    print("--- ETL Manager Tool ---")
    print_dashes()
    print("1. GET all sales")
    print("2. GET sale by customer_id")
    print("3. POST (add new sale)")
    print("4. PUT (update sale by customer_id)")
    print("5. DELETE sale by customer_id")
    print("6. Export sales (CSV or Excel)")
    print("0. Exit")
    print_dashes()

def get_all_sales():
    resp = requests.get(BASE_URL)
    sales = resp.json()

    if not sales:
        print("No sales found.")
        return

    # Extract keys for headers
    headers = ["id", "customer_id", "date", "product", "quantity", "unit_price", "total_price"]
    table = [[sale[h] for h in headers] for sale in sales]

    print(tabulate(table, headers=headers, tablefmt="grid"))


def get_sale_by_customer():
    cid = input("Enter customer_id: ")
    resp = requests.get(f"{BASE_URL}/{cid}")
    print(resp.json())


def add_sale():
    sale = {}
    sale["date"] = input("Date (YYYY-MM-DD): ")
    sale["customer_id"] = int(input("Customer ID: "))
    sale["product"] = input("Product: ")
    sale["quantity"] = int(input("Quantity: "))
    sale["unit_price"] = float(input("Unit Price: "))
    resp = requests.post(BASE_URL, json=sale)
    print(resp.json())


def update_sale():
    cid = input("Enter customer_id to update: ")
    update = {}
    update["quantity"] = int(input("New quantity: "))
    update["unit_price"] = float(input("New unit price: "))
    resp = requests.put(f"{BASE_URL}/{cid}", json=update)
    print(resp.json())


def delete_sale():
    cid = input("Enter customer_id to delete: ")
    resp = requests.delete(f"{BASE_URL}/{cid}")
    print(resp.json())


def export_sales():
    fmt = input("Format (csv/excel): ").lower()
    resp = requests.get(f"{BASE_URL}/export/{fmt}")
    print(resp.json())


# Main loop
try:
    while True:
        print_menu()
        choice = input("Choose option: ")
        if choice == "1":
            get_all_sales()
        elif choice == "2":
            get_sale_by_customer()
        elif choice == "3":
            add_sale()
        elif choice == "4":
            update_sale()
        elif choice == "5":
            delete_sale()
        elif choice == "6":
            export_sales()
        elif choice == "0":
            break
        else:
            print("Invalid choice! Try again.")

except KeyboardInterrupt:
    print("\nProgram Stopped Running...")




