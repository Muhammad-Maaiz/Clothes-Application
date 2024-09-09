import datetime
import sqlite3

# Database class handles all database connections and operations
class Database:
    def __init__(self):
        # Establish connection to the SQLite3 database
        self.conn = sqlite3.connect('clothes_verve.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    # Method to create the necessary tables for the application
    def create_table(self):
        # Enable foreign key constraints in SQLite
        self.conn.execute('PRAGMA foreign_keys = ON;')

        # Create clothes table to store clothes details
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clothes (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                category TEXT NOT NULL,
                                brand_name TEXT NOT NULL,
                                price REAL NOT NULL,
                                selling_price REAL NOT NULL,
                                quantity INTEGER NOT NULL,
                                image BLOB NOT NULL)''')

        # Create Users table to store user details
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                            (id INTEGER PRIMARY KEY,
                            full_name TEXT NOT NULL,
                            username TEXT NOT NULL UNIQUE,
                            email TEXT NOT NULL,
                            password TEXT NOT NULL)''')

        # Create add_to_cart_history table to track user's cart history
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS add_to_cart_history
                    (id INTEGER PRIMARY KEY,
                    clothes_name TEXT NOT NULL,
                    clothes_category TEXT NOT NULL,
                    clothes_brand TEXT NOT NULL,
                    clothes_size TEXT NOT NULL,
                    clothes_price REAL NOT NULL,
                    clothes_quantity INTEGER NOT NULL,
                    clothes_id INTEGER NOT NULL,
                    userId INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    day TEXT NOT NULL,
                    time TEXT NOT NULL,
                    FOREIGN KEY (userId) REFERENCES Users(id),
                    FOREIGN KEY (clothes_id) REFERENCES clothes(id))''')

        # Save (commit) changes to the database
        self.conn.commit()

    # Close the database connection
    def close(self):
        self.conn.close()

# Admin class contains functionalities for the admin to manage clothes
class Admin:
    def __init__(self, db):
        self.db = db

    # Add a new item of clothing to the database
    def add_clothes(self, clothes_name, category, brand_name, price, selling_price, quantity, image_bytes):
        self.db.cursor.execute('''INSERT INTO clothes (name, category, brand_name, price, selling_price, quantity, image) VALUES (?, ?, ?, ?, ?, ?, ?)''', (clothes_name, category, brand_name, price, selling_price, quantity, image_bytes))
        self.db.conn.commit()

    # Retrieve all clothes from the database
    def get_all_clothes(self):
        self.db.cursor.execute('''SELECT id, name, category, brand_name, price, selling_price, quantity, image FROM clothes''')
        clothes = self.db.cursor.fetchall()
        return [{'id': row[0], 'name': row[1], 'category': row[2], 'brand_name': row[3], 'price': row[4], 'selling_price': row[5], 'quantity': row[6], 'image': row[7]} for row in clothes]

    # Update clothes details in the database
    def update_clothes(self, clothes_id, clothes_name, category, brand_name, price, selling_price, quantity, image_bytes):
        self.db.cursor.execute('''UPDATE clothes SET name = ?, category = ?, brand_name = ?, price = ?, selling_price = ?, quantity = ?, image = ? WHERE id = ?''', (clothes_name, category, brand_name, price, selling_price, quantity, image_bytes, clothes_id))
        self.db.conn.commit()

    # Delete a specific item of clothing from the database
    def delete_clothes(self, clothes_id):
        self.db.cursor.execute('''DELETE FROM clothes WHERE id = ?''', (clothes_id,))
        self.db.conn.commit()

# User class contains functionalities for user registration, login, and cart management
class User:
    def __init__(self, db):
        self.db = db
        self.cart = []  # Initialize the cart list

    # User signup function with validation
    def signup(self, full_name, username, email, password):
        # Check if the email already exists
        self.db.cursor.execute('''SELECT * FROM Users WHERE email = ?''', (email,))
        if self.db.cursor.fetchone() is not None:
            return "email_exists"

        # Check if the password already exists
        self.db.cursor.execute('''SELECT * FROM Users WHERE password = ?''', (password,))
        if self.db.cursor.fetchone() is not None:
            return "password_exists"

        # Insert new user if email and password are unique
        try:
            self.db.cursor.execute('''INSERT INTO Users (full_name, username, email, password) VALUES (?, ?, ?, ?)''',(full_name, username, email, password))
            self.db.conn.commit()
            return "success"
        except sqlite3.IntegrityError:
            return "username_exists"

    # User login function to verify credentials
    def login(self, username, password):
        self.db.cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
        return self.db.cursor.fetchone() is not None

    # Handle forgotten passwords
    def forget_password(self, email):
        # Check if the email exists in the database
        self.db.cursor.execute('''SELECT * FROM Users WHERE email = ?''', (email,))
        user = self.db.cursor.fetchone()
        if user:
            return "email_exists"
        else:
            return "email_not_found"

    # Reset password function with confirmation checks
    def reset_password(self, email, new_password, confirm_password):
        # Check if the email exists in the database
        self.db.cursor.execute('''SELECT * FROM Users WHERE email = ?''', (email,))
        user = self.db.cursor.fetchone()
        if not user:
            return "email_not_found"

        # Check if both new password fields are filled
        if not new_password or not confirm_password:
            return "empty_fields"

        # Check if both new password fields match
        if new_password != confirm_password:
            return "password_mismatch"

        # Update the password in the database
        self.db.cursor.execute('''UPDATE Users SET password = ? WHERE email = ?''', (new_password, email))
        self.db.conn.commit()
        return "password_updated"

    # Retrieve user information by username
    def get_user_by_username(self, username):
        self.db.cursor.execute('''SELECT id, full_name FROM Users WHERE username = ?''', (username,))
        result = self.db.cursor.fetchone()
        return {'user_id': result[0], 'full_name': result[1]} if result else None

    # Add a clothing item to the user's cart with size check
    def add_to_cart(self, clothes_img, clothes_id, clothes_name, clothes_price, clothes_category, clothes_brand, clothes_size, clothes_quantity):
        # Check if the item is already in the cart with the same size
        for item in self.cart:
            if (item['clothes_id'] == clothes_id and
                item['clothes_size'] == clothes_size):
                return False  # Return False if item is already in the cart

        # Add new item to the cart if not present
        self.cart.append({
            'clothes_id': clothes_id,
            'clothes_img': clothes_img,
            'clothes_name': clothes_name,
            'clothes_price': clothes_price,
            'clothes_category': clothes_category,
            'clothes_brand': clothes_brand,
            'clothes_size': clothes_size,
            'clothes_quantity': clothes_quantity
        })
        return True  # Item successfully added

    # Checkout function to store the cart details in the database
    def checkout(self, user_id):
        current_time = datetime.datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        day = current_time.strftime("%A")
        time = current_time.strftime("%H:%M:%S")

        # Insert clothes from cart into the add_to_cart_history table
        for item in self.cart:
            self.db.cursor.execute('''INSERT INTO add_to_cart_history (clothes_id, clothes_name, clothes_category, clothes_brand, clothes_size, clothes_price, clothes_quantity, userId, date, day, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',(item['clothes_id'], item['clothes_name'], item['clothes_category'], item['clothes_brand'], item['clothes_size'], item['clothes_price'], item['clothes_quantity'], user_id, date, day, time))

        self.db.conn.commit()

    # Generate a bill for the user's cart items
    def generate_bill(self, user_id):
        # Fetch user details from the database
        self.db.cursor.execute('''SELECT full_name, email FROM Users WHERE id = ?''', (user_id,))
        user = self.db.cursor.fetchone()
        full_name = user[0]
        email = user[1]

        # Initialize bill amounts
        subtotal = 0
        tax = 0
        grand_total = 0

        # Check if the cart is empty
        if not self.cart:
            return None  # Handle empty cart case

        # Calculate subtotal from the cart items
        for item in self.cart:
            quantity = item['clothes_quantity']
            price = item['clothes_price']
            total = quantity * price
            subtotal += total

        # Calculate tax and grand total
        tax = subtotal * 0.15
        grand_total = subtotal + tax

        # Generate the bill details
        bill = {
            'full_name': full_name,
            'email': email,
            "day": datetime.datetime.now().strftime('%A'),
            "date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "time": datetime.datetime.now().strftime('%H:%M:%S'),
            'subtotal': subtotal,
            'tax': tax,
            'grand_total': grand_total,
            'cart': self.cart.copy()
        }

        # Clear the cart after generating the bill
        self.cart.clear()


        return bill  # Return the generated bill details