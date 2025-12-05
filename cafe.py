import hashlib
import json
from datetime import datetime
import main

# To hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users(): # Load users
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return an empty list if file is missing/not found...
    except json.JSONDecodeError: # Return empty list if JSON code has an error ...
        print("Error reading users file. It might be corrupted.")
        return []

def save_orders(orders):
    try:
        with open("orders.json", "w") as f:
            json.dump(orders, f, indent=4)
    except FileNotFoundError:
        print("Error: orders.txt not found.")
    except json.JSONDecodeError:
        print("Error writing to orders.txt.")

def load_orders():
    try:
        with open("orders.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def add_user(username, password, role="user"): # To add the user
    users = load_users()
    hashed_password = hash_password(password)
    new_user = {"username": username, "password": hashed_password, "role": role}
    
    users.append(new_user)

    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)
    print("User added successfully!")

def authenticate_user(): # To authenticate the user
    users = load_users()
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    for user in users:
        if user['username'] == username and user['password'] == hashed_password:
            print("Authentication successful!")
            return username

    print("Invalid username or password.")
    return None

def is_admin(username):
    """Checks if the user has admin privileges."""
    users = load_users()
    for user in users:
        if user['username'] == username and user.get('role') == 'admin':
            return True
    return False

def order(item, username):
    """Function to handle orders."""
    orders = load_orders()
    new_order = {"item": item, "user": username, "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    orders.append(new_order)
    save_orders(orders)
    print(f"{item} ordered successfully!")

def view_orders(username):
    """Function to view user's orders."""
    orders = load_orders()
    user_orders = [order for order in orders if order['user'] == username]
    if not user_orders:
        print("No orders found.")
        return

    for i, order in enumerate(user_orders, 1):
        print(f"{i}. {order['item']} - Date: {order['date']}")

def edit_order(username, is_admin=False):
    """Function to edit orders."""
    orders = load_orders()
    user_orders = [order for order in orders if order['user'] == username]
    
    for i, order in enumerate(user_orders, 1):
        print(f"{i}. {order['item']} - Date: {order['date']}")

    try:
        index = int(input("Enter the order number to edit (or 0 to cancel): ")) - 1
        if index == -1:
            print("Editing canceled.")
        elif 0 <= index < len(user_orders):
            if is_admin or user_orders[index]['user'] == username:
                new_item = input("Enter the new item: ")
                user_orders[index]['item'] = new_item
                user_orders[index]['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_orders(orders)
                print("Order edited successfully.")
            else:
                print("You can only edit your own orders.")
        else:
            print("Invalid order number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def delete_order(username, is_admin=False):
    """Function to delete orders."""
    orders = load_orders()
    user_orders = [order for order in orders if order['user'] == username]
    
    for i, order in enumerate(user_orders, 1):
        print(f"{i}. {order['item']} - Date: {order['date']}")

    try:
        index = int(input("Enter the order number to delete (or 0 to cancel): ")) - 1
        if index == -1:
            print("Deletion canceled.")
        elif 0 <= index < len(user_orders):
            if is_admin or user_orders[index]['user'] == username:
                orders.remove(user_orders[index])
                save_orders(orders)
                print("Order deleted.")
            else:
                print("You can only delete your own orders.")
        else:
            print("Invalid order number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def create_account():
    """Function to create a new user account."""
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")
    role = input("Enter role(user or admin): ").lower()
    add_user(username, password, role)
    print("Account created successfully!")
