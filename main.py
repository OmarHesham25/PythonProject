import resturant
import os

PRODUCTS = ["Burger", "Pizza", "Beans"]  # <-- list of available products
file_path = ("orders.json")
def main():
    while True:
        print("""
        ==== Welcome to Task Manager ====
        1. Sign In
        2. Create Account
        3. Quit
        """)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            username = resturant.authenticate_user()
            if username:
                print(f"Welcome, {username}!")
                is_user_admin = resturant.is_admin(username)
                while True:
                    print("""
                    1. Menu
                    2. View Orders
                    3. Edit Order
                    4. Delete Order
                    5. Sign Out
                    """)
                    if is_user_admin:
                        print("                    6. View All Orders (Admin Only)")
                        print("                    7. Edit Any Order (Admin Only)")
                        print("                    8. Delete All  Orders (Admin Only)")
                        print("                    9. Add new order to menu (Admin Only)")
                    choice = input("Enter your choice: ").strip()
                    if choice == "1":
                        # Display menu dynamically from PRODUCTS list
                        print("\nAvailable Products:")
                        for index, product in enumerate(PRODUCTS, start=1):
                            print(f"{index}. {product}")
                        order_choice = input("Enter the number of the order: ").strip()
                        if order_choice.isdigit():
                            order_index = int(order_choice)
                            if 0 <= order_index < len(PRODUCTS):
                                selected_product = PRODUCTS[order_index]
                                resturant.order(selected_product, username)
                            else:
                                print("Invalid choice. Please try again.")
                        else:
                            print("Invalid input. Please enter a number.")

                    elif choice == "2":
                        resturant.view_orders(username)

                    elif choice == "3":
                        resturant.edit_order(username, is_user_admin)
                    elif choice == "4":
                        resturant.delete_order(username, is_user_admin)
                    elif choice == "5":
                        print("Signing out...")
                        break
                    elif choice == "6" and is_user_admin:
                        # view all orders functionality
                        print("All Orders:")
                    elif choice == "7" and is_user_admin:
                        # edit any order functionality
                        print("Editing any order...")
                        pass
                    elif choice == "8" and is_user_admin:
                        print("Deleting any order...")
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print("file deleted")
                    elif choice == "9" and is_user_admin:
                        x  = input("Enter A product to add to the menu: ")
                        PRODUCTS.append(x)
                        print("item added")
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == "2":
            resturant.create_account()
        elif choice == "3":
            print("Quitting....")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
