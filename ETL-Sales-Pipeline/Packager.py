import sys
import subprocess
import json
import os
from colorama import init, Fore
from tStyle import BillingStyle

# Initialize colorama
init(autoreset=True)
style = BillingStyle()
PACKAGES_FILE = "new_packages.json"
COLLECTIONS_FILE = "package_collections.json"

# -----------------------------
# Visual Helpers
# -----------------------------
def print_dashes(count=80):
    for _ in range(count):
        print("-", end="")
    print()

def color_msg(msg, color="green"):
    if color == "green":
        return Fore.GREEN + msg
    elif color == "yellow":
        return Fore.YELLOW + msg
    elif color == "red":
        return Fore.RED + msg
    return msg

# -----------------------------
# Utility Functions
# -----------------------------
def run_pip_command(args):
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip"] + args,
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(color_msg(f"Error: {e.stderr}", "red"))
        return None

def is_installed(package):
    output = run_pip_command(["list", "--format=json"])
    if not output:
        return False
    installed_packages = {pkg["name"].lower() for pkg in json.loads(output)}
    return package.lower() in installed_packages

def store_new_package(package):
    try:
        if os.path.exists(PACKAGES_FILE):
            with open(PACKAGES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        if package not in data:
            data.append(package)
            with open(PACKAGES_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
    except Exception as e:
        print(color_msg(f"Could not store package: {e}", "red"))

# -----------------------------
# Collections Functions
# -----------------------------
def load_collections():
    if not os.path.exists(COLLECTIONS_FILE):
        print(color_msg(f"Collections file not found: {COLLECTIONS_FILE}", "red"))
        return {}
    try:
        with open(COLLECTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(color_msg(f"Error loading collections: {e}", "red"))
        return {}

def save_collections(collections):
    try:
        with open(COLLECTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(collections, f, indent=2)
    except Exception as e:
        print(color_msg(f"Error saving collections: {e}", "red"))

def add_to_other_packages(package):
    collections = load_collections()
    if not collections:
        return
    other = collections.get("OTHER PACKAGES", [])
    if package not in other:
        other.append(package)
        collections["OTHER PACKAGES"] = other
        save_collections(collections)
        print(color_msg(f"{package} added to OTHER PACKAGES collection.", "yellow"))

# -----------------------------
# Package Management
# -----------------------------
def install_packages(packages):
    for package in packages:
        if is_installed(package):
            print(color_msg(f"{package} is already installed.", "yellow"))
        else:
            print(color_msg(f"Installing {package}...", "green"))
            run_pip_command(["install", package])
            store_new_package(package)
            add_to_other_packages(package)

def read_packages_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(color_msg(f"File not found: {filename}", "red"))
        return []

def show_installed_packages():
    output = run_pip_command(["list"])
    if output:
        print_dashes()
        print(output)
        print_dashes()

def check_outdated_packages():
    output = run_pip_command(["list", "--outdated", "--format=json"])
    if not output:
        return
    outdated = json.loads(output)
    if not outdated:
        print(color_msg("All packages are up to date.", "green"))
        return

    print(color_msg("Outdated packages found:", "yellow"))
    for idx, pkg in enumerate(outdated, 1):
        print(f"{idx}. {pkg['name']} {pkg['version']} -> {pkg['latest_version']}")

    choice = input("\nUpdate (a)ll, (s)elect, or (n)one? ").lower()
    if choice == "a":
        for pkg in outdated:
            run_pip_command(["install", "--upgrade", pkg["name"]])
    elif choice == "s":
        nums = input("Enter numbers separated by commas: ").split(",")
        for num in nums:
            try:
                pkg = outdated[int(num) - 1]
                run_pip_command(["install", "--upgrade", pkg["name"]])
            except (ValueError, IndexError):
                print(color_msg(f"Invalid selection: {num}", "red"))
    else:
        print(color_msg("No updates performed.", "yellow"))

# -----------------------------
# Collection Submenu
# -----------------------------
def show_package_collections():
    collections = load_collections()
    style.print_header("Package Collections")
    roles = list(collections.keys())
    while True:

        for i, role in enumerate(roles, 1):
            print(f"{i}. {role} ({len(collections[role])} packages)")
        print(f"{len(roles) + 1}. Return to Main Menu")
        print_dashes()
        choice = style.get_formatted_input("Select a role to view/manage", "int")
        if 1 <= choice <= len(roles):
            role_name = roles[choice - 1]
            manage_role(role_name, collections)
        else:
            break

def manage_role(role, collections):
    packages = collections[role]
    while True:
        print_dashes()
        print(f"[{role}] Packages:")
        for idx, pkg in enumerate(packages, 1):
            print(f"{idx}. {pkg}")
        print_dashes()
        print("Options: [i]nstall all, [a]dd package, [r]emove package, [b]ack")
        opt = input("Choice: ").lower()
        if opt == "i":
            install_packages(packages)
        elif opt == "a":
            new_pkg = input("Enter package name to add: ").strip()
            if new_pkg and new_pkg not in packages:
                packages.append(new_pkg)
                collections[role] = packages
                save_collections(collections)
                print(color_msg(f"{new_pkg} added to {role}.", "yellow"))
        elif opt == "r":
            rem_idx = input("Enter package number to remove: ").strip()
            try:
                rem_idx = int(rem_idx) - 1
                removed = packages.pop(rem_idx)
                collections[role] = packages
                save_collections(collections)
                print(color_msg(f"{removed} removed from {role}.", "yellow"))
            except:
                print(color_msg("Invalid selection.", "red"))
        elif opt == "b":
            break
        else:
            print(color_msg("Invalid choice.", "red"))

# -----------------------------
# Main Menu
# -----------------------------
def main():
    while True:
        style.print_header("Python Package Manager")
        style.print_menu([
            "Input package names to install",
            "Read package names from a file",
            "Show/manage packages by role",
            "Show installed packages",
            "Check for outdated packages & update",
            "Install all predefined packages (caution!)",
            "Exit"
        ])
        choice = style.get_formatted_input("Choose an option (1-7)", "int")
        if choice == 1:
            style.print_info_message("Enter package names one per line. Press ENTER twice to finish.")
            packages = []
            while True:
                pkg = input("> ").strip()
                if not pkg:
                    break
                packages.append(pkg)
            install_packages(packages)
        elif choice == 2:
            filename = input("Enter filename: ").strip()
            packages = read_packages_from_file(filename)
            install_packages(packages)
        elif choice == 3:
            show_package_collections()
        elif choice == 4:
            show_installed_packages()
        elif choice == 5:
            print("Loading...")
            check_outdated_packages()
        elif choice == 6:
            collections = load_collections()
            all_packages = sum(collections.values(), [])
            style.print_warning_message("This will install ALL predefined packages!")
            if input("Continue? (y/n): ").lower() == "y":
                install_packages(all_packages)
        elif choice == 7:
            style.print_info_message("Exiting program. Goodbye!")
            break
        else:
            print(color_msg("Invalid choice. Please try again.", "red"))

if __name__ == "__main__":
    main()
