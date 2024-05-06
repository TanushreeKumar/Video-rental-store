import re
import tkinter as tk
from tkinter import messagebox
import mysql.connector

def create_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard"
        )
        cursor = conn.cursor()

        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS video_store")
        conn.commit()
        print("Database 'video_store' created successfully.")

    except mysql.connector.Error as error:
        print("Error occurred while creating database:", error)

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def authenticate_user():
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )

        cursor = connection.cursor()
        username = username_entry.get()
        password = password_entry.get()
        # Query to check if username and password match
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, {}".format(user[1])) # Assuming user[1] is the user's name
            open_main_application_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

        cursor.close()
        connection.close()
    
    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

# Function to create users table and insert a sample user record
def initialize_database():
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )

        cursor = connection.cursor()

        # Create users table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL
            )
        """)

        # Create movie table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movie (
                MovieID INT AUTO_INCREMENT PRIMARY KEY,
                MovieName VARCHAR(255) NOT NULL,
                Director VARCHAR(255),
                ChargePerDay DECIMAL(10, 2),
                Producer VARCHAR(255), 
                Type VARCHAR(50),
                Quantity INT 
            )
        """)

        # Create vcr table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vcr (           
                VCRID INT AUTO_INCREMENT PRIMARY KEY,
                Type VARCHAR(255) NOT NULL,
                VcrBrand VARCHAR(255),
                Charge DECIMAL(10, 2),
                MadeBy VARCHAR(255),
                Quantity INT 
            )
        """)

        # Create video_camera table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS video_camera (
                Video_CameraID INT AUTO_INCREMENT PRIMARY KEY,
                VCamBrand VARCHAR(255) NOT NULL,
                MadeBy VARCHAR(255),
                Charge DECIMAL(10, 2),
                Quantity INT 
            )
        """)

        # Create employees table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                Position VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                CustomerID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                Email VARCHAR(255),
                Phone VARCHAR(20)
            );
        """)

        # Create transactions table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie_transactions (
        TransactionID INT AUTO_INCREMENT PRIMARY KEY,
        TType VARCHAR(10) NOT NULL,
        MovieID INT NOT NULL,
        AmountPayed DECIMAL(10, 2),
        DueDate DATE,
        ReturnDate DATE,
        CustomerID INT,
        EmployeeID INT,
        FOREIGN KEY (MovieID) REFERENCES movie(MovieID) ON DELETE CASCADE,
        FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID) ON DELETE CASCADE,
        FOREIGN KEY (EmployeeID) REFERENCES employees(EmployeeID) ON DELETE CASCADE,
        CONSTRAINT fk_employee FOREIGN KEY (EmployeeID) REFERENCES employees(EmployeeID)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vcr_transactions (
            TransactionID INT AUTO_INCREMENT PRIMARY KEY,
            TType VARCHAR(10) NOT NULL,
            VCRID INT NOT NULL,
            AmountPayed DECIMAL(10, 2),
            DueDate DATE,
            ReturnDate DATE,
            CustomerID INT,
            EmployeeID INT,
            FOREIGN KEY (VCRID) REFERENCES vcr(VCRID) ON DELETE CASCADE,
            FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (EmployeeID) REFERENCES employees(EmployeeID) ON DELETE CASCADE
         );
            """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS video_camera_transactions (
            TransactionID INT AUTO_INCREMENT PRIMARY KEY,
            TType VARCHAR(10) NOT NULL,
            VCamID INT NOT NULL,
            AmountPayed DECIMAL(10, 2),
            DueDate DATE,
            ReturnDate DATE,
            CustomerID INT,
            EmployeeID INT,
            FOREIGN KEY (VCamID) REFERENCES video_camera(Video_CameraID) ON DELETE CASCADE,
            FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (EmployeeID) REFERENCES employees(EmployeeID) ON DELETE CASCADE
         );
         """)

        # Create the customer_transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_transactions (
                TransactionID INT AUTO_INCREMENT PRIMARY KEY,
                TType VARCHAR(10) NOT NULL,
                ItemID INT NOT NULL,
                AmountPayed DECIMAL(10, 2),
                DueDate DATE,
                ReturnDate DATE,
                CustomerID INT,
                EmployeeID INT,
                FOREIGN KEY (ItemID) REFERENCES movie(MovieID) ON DELETE CASCADE,
                FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID) ON DELETE CASCADE,
                FOREIGN KEY (EmployeeID) REFERENCES employees(EmployeeID) ON DELETE CASCADE
            );
        """)

        # Insert a sample user record if the table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("johndoe", "password123"))

        connection.commit()
        
    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to initialize database: {}".format(error))

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Function to open the main application window
def open_main_application_window():
    main_window = tk.Toplevel(root)
    main_window.title("Video Store Management System - Main Menu")

    # Create main menu widgets (e.g., buttons for different modules)
    catalog_button = tk.Button(main_window, text="Catalog Management", command=lambda: open_catalog_management_window(main_window))
    catalog_button.pack(pady=10)

    store_button = tk.Button(main_window, text="Store Management", command=lambda: open_store_management_window(main_window))
    store_button.pack(pady=10)

    transaction_button = tk.Button(main_window, text="Transaction Management", command=lambda: open_transaction_management_window(main_window))
    transaction_button.pack(pady=10)

# Function to open the catalog management window
def open_catalog_management_window(parent):
    catalog_window = tk.Toplevel(parent)
    catalog_window.title("Catalog Management")

    # Create radio buttons to select item type
    item_type = tk.StringVar(value="movie")
    movie_radio = tk.Radiobutton(catalog_window, text="Movie", variable=item_type, value="movie")
    movie_radio.pack(anchor="w", padx=10, pady=5)
    vcr_radio = tk.Radiobutton(catalog_window, text="VCR", variable=item_type, value="vcr")
    vcr_radio.pack(anchor="w", padx=10, pady=5)
    video_camera_radio = tk.Radiobutton(catalog_window, text="Video Camera", variable=item_type, value="video_camera")
    video_camera_radio.pack(anchor="w", padx=10, pady=5)

    # Create buttons for selected item type
    view_button = tk.Button(catalog_window, text="View", command=lambda: view_items(item_type.get()))
    view_button.pack(pady=5)
    add_button = tk.Button(catalog_window, text="Add", command=lambda: add_item(item_type.get()))
    add_button.pack(pady=5)
    edit_button = tk.Button(catalog_window, text="Edit", command=lambda: edit_item(item_type.get()))
    edit_button.pack(pady=5)
    delete_button = tk.Button(catalog_window, text="Delete", command=lambda: delete_item(item_type.get()))
    delete_button.pack(pady=5)

# Function to view items based on type
def view_items(item_type):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )

        cursor = connection.cursor()

        if item_type == "movie":
            cursor.execute("SELECT * FROM movie")
        elif item_type == "vcr":
            cursor.execute("SELECT * FROM vcr")
        elif item_type == "video_camera":
            cursor.execute("SELECT * FROM video_camera")

        items = cursor.fetchall()

        if not items:
            messagebox.showinfo("No Items", "No {}s found in the database.".format(item_type.capitalize()))
            return

        # Display item details in a new window
        view_window = tk.Toplevel(root)
        view_window.title("View {}s".format(item_type.capitalize()))

        # Create a text widget to display item details
        text_widget = tk.Text(view_window, height=10, width=50)
        text_widget.pack(padx=10, pady=10)

        # Get column names
        cursor.execute("SHOW COLUMNS FROM {}".format(item_type))
        columns = [column[0] for column in cursor.fetchall()]

        # Insert column names followed by their corresponding values for each item
        for item in items:
            for i in range(len(columns)):
                text_widget.insert(tk.END, "{}: {}\n".format(columns[i], item[i]))
            text_widget.insert(tk.END, "---------------------------------\n\n")

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

# Function to add item based on type
def add_item(item_type):
    add_window = tk.Toplevel(root)
    add_window.title("Add {} - {}".format(item_type.capitalize(), "Movie Store"))

    # Create labels and entry fields for item details
    if item_type == "movie":
        # Create labels and entry fields for movie details
        movie_name_label = tk.Label(add_window, text="Movie Name:")
        movie_name_label.pack(pady=5)
        movie_name_entry = tk.Entry(add_window)
        movie_name_entry.pack(pady=5)

        director_label = tk.Label(add_window, text="Director:")
        director_label.pack(pady=5)
        director_entry = tk.Entry(add_window)
        director_entry.pack(pady=5)

        producer_label = tk.Label(add_window, text="Producer:")
        producer_label.pack(pady=5)
        producer_entry = tk.Entry(add_window)
        producer_entry.pack(pady=5)

        charge_per_day_label = tk.Label(add_window, text="Charge:")
        charge_per_day_label.pack(pady=5)
        charge_per_day_entry = tk.Entry(add_window)
        charge_per_day_entry.pack(pady=5)

        movie_type_label = tk.Label(add_window, text="Type:")
        movie_type_label.pack(pady=5)
        movie_type_entry = tk.Entry(add_window)
        movie_type_entry.pack(pady=5)

        quantity_label = tk.Label(add_window, text="Quantity:")
        quantity_label.pack(pady=5)
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack(pady=5)

        # Create button to add movie
        add_button = tk.Button(add_window, text="Add", command=lambda: add_movie(
            movie_name_entry.get(),
            director_entry.get(),
            charge_per_day_entry.get(),
            producer_entry.get(),
            movie_type_entry.get(),
            quantity_entry.get()
        ))
        add_button.pack(pady=10)

    elif item_type == "vcr":
        # Create labels and entry fields for VCR details
        vcr_type_label = tk.Label(add_window, text="Type:")
        vcr_type_label.pack(pady=5)
        vcr_type_entry = tk.Entry(add_window)
        vcr_type_entry.pack(pady=5)

        charge_label = tk.Label(add_window, text="Charge:")
        charge_label.pack(pady=5)
        charge_entry = tk.Entry(add_window)
        charge_entry.pack(pady=5)

        vcr_brand_label = tk.Label(add_window, text="VCR Brand:")
        vcr_brand_label.pack(pady=5)
        vcr_brand_entry = tk.Entry(add_window)
        vcr_brand_entry.pack(pady=5)

        made_by_label = tk.Label(add_window, text="Made By:")
        made_by_label.pack(pady=5)
        made_by_entry = tk.Entry(add_window)
        made_by_entry.pack(pady=5)

        quantity_label = tk.Label(add_window, text="Quantity:")
        quantity_label.pack(pady=5)
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack(pady=5)

        # Create button to add VCR
        add_button = tk.Button(add_window, text="Add", command=lambda: add_vcr(
            vcr_type_entry.get(),
            vcr_brand_entry.get(),
            charge_entry.get(),
            made_by_entry.get(),
            quantity_entry.get()
        ))
        add_button.pack(pady=10)

    elif item_type == "video_camera":
        # Create labels and entry fields for video camera details
        vcam_brand_label = tk.Label(add_window, text="Brand:")
        vcam_brand_label.pack(pady=5)
        vcam_brand_entry = tk.Entry(add_window)
        vcam_brand_entry.pack(pady=5)

        made_by_label = tk.Label(add_window, text="Made By:")
        made_by_label.pack(pady=5)
        made_by_entry = tk.Entry(add_window)
        made_by_entry.pack(pady=5)

        charge_label = tk.Label(add_window, text="Charge:")
        charge_label.pack(pady=5)
        charge_entry = tk.Entry(add_window)
        charge_entry.pack(pady=5)

        quantity_label = tk.Label(add_window, text="Quantity:")
        quantity_label.pack(pady=5)
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack(pady=5)

        # Create button to add video camera
        add_button = tk.Button(add_window, text="Add", command=lambda: add_video_camera(
            vcam_brand_entry.get(),
            made_by_entry.get(),
            charge_entry.get(),
            quantity_entry.get()
        ))
        add_button.pack(pady=10)

# Function to add a new movie
def add_movie(movie_name, director, charge_per_day, producer, movie_type, quantity):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )

        cursor = connection.cursor()

        query = "INSERT INTO MOVIE (MovieName, Director, ChargePerDay, Producer, Type, Quantity) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (movie_name, director, charge_per_day, producer, movie_type, quantity))
        connection.commit()

        messagebox.showinfo("Success", "Movie added successfully")

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

# Function to add a new VCR
def add_vcr(vcr_type, vcr_brand, charge, made_by, quantity):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )

        cursor = connection.cursor()
        
        query = "INSERT INTO VCR (Type, VcrBrand, Charge, MadeBy, Quantity ) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (vcr_type, vcr_brand, charge, made_by, quantity))
        connection.commit()

        messagebox.showinfo("Success", "VCR added successfully")

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

# Function to add a new video camera
def add_video_camera(vcam_brand, made_by, charge, quantity):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )

        cursor = connection.cursor()
        
        query = "INSERT INTO VIDEO_CAMERA (VCamBrand, MadeBy, Charge, Quantity) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (vcam_brand, made_by, charge, quantity))
        connection.commit()

        messagebox.showinfo("Success", "Video camera added successfully")

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

# Function to edit item based on type
def edit_item(item_type):
    try:
        # Fetch items of the selected type
        fetch_items(item_type)

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))


def fetch_items(item_type):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )

        cursor = connection.cursor()

        # Fetch all items of the selected type
        if item_type == "movie":
            cursor.execute("SELECT * FROM movie")
        elif item_type == "vcr":
            cursor.execute("SELECT * FROM vcr")
        elif item_type == "video_camera":
            cursor.execute("SELECT * FROM video_camera")

        items = cursor.fetchall()

        if not items:
            messagebox.showinfo("No Items", "No {}s found in the database.".format(item_type.capitalize()))
            return

        # Display item details in a new window
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit {}s".format(item_type.capitalize()))

        # Create a listbox to display items
        listbox = tk.Listbox(edit_window, width=50)
        listbox.pack(padx=10, pady=10)

        # Insert items into the listbox
        for item in items:
            listbox.insert(tk.END, item)

        # Function to handle item selection
        def select_item():
            selected_index = listbox.curselection()[0]
            selected_item = items[selected_index]
            open_edit_window(selected_item, item_type)

        # Button to select an item for editing
        select_button = tk.Button(edit_window, text="Select Item", command=select_item)
        select_button.pack(pady=5)

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

def open_edit_window(item, item_type):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit {} - {}".format(item_type.capitalize(), "Video Store"))

    # Create labels and entry fields for item details
    if item_type == "movie":
        labels = ["Movie Name:", "Director:", "Charge Per Day:", "Producer:", "Type:", "Quantity:"]
    elif item_type == "vcr":
        labels = ["Type:", "VCR Brand:", "Charge:", "Made By:", "Quantity:"]
    elif item_type == "video_camera":
        labels = ["Brand:", "Made By:", "Charge:", "Quantity:"]

    entries = []
    # Populate labels and entry fields
    for label_text, value in zip(labels, item[1:]):
        label = tk.Label(edit_window, text=label_text)
        label.pack(pady=5)
        entry = tk.Entry(edit_window)
        entry.insert(tk.END, value)
        entry.pack(pady=5)
        entries.append(entry)

    # Function to update the item details
    def update_item():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mathsboard",
                database="video_store"
            )

            cursor = connection.cursor()

            updated_values = [entry.get() for entry in entries]
            query, params = generate_update_query(item_type, updated_values, item[0])
            cursor.execute(query, params)
            connection.commit()
            messagebox.showinfo("Success", "{} details updated successfully".format(item_type.capitalize()))
            edit_window.destroy()

            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

     # Button to update the item details
    update_button = tk.Button(edit_window, text="Update", command=update_item)
    update_button.pack(pady=10)

def generate_update_query(item_type, updated_values, item_id):
    # Define the fields and table based on the item type
    if item_type == "movie":
        fields = ["MovieName", "Director", "ChargePerDay", "Producer", "Type", "Quantity"]
        table = "movie"
    elif item_type == "vcr":
        fields = ["Type", "VcrBrand", "Charge", "MadeBy", "Quantity"]
        table = "vcr"
    elif item_type == "video_camera":
        fields = ["VCamBrand", "MadeBy", "Charge", "Quantity"]
        table = "video_camera"
    else:
        raise ValueError("Invalid item type: {}".format(item_type))

    # Construct the SET clause of the SQL query
    set_clause = ", ".join(["{} = %s".format(field) for field in fields])

    # Construct the full SQL query
    query = "UPDATE {} SET {} WHERE {}ID = %s".format(table, set_clause, item_type.capitalize())

    # Prepare the values to be substituted into the query
    query_values = tuple(updated_values + [item_id])
    return query, query_values


# Function to delete item based on type
def delete_item(item_type):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )

        cursor = connection.cursor()

        # Fetch all items of the selected type
        if item_type == "movie":
            cursor.execute("SELECT * FROM movie")
        elif item_type == "vcr":
            cursor.execute("SELECT * FROM vcr")
        elif item_type == "video_camera":
            cursor.execute("SELECT * FROM video_camera")

        items = cursor.fetchall()

        if not items:
            messagebox.showinfo("No Items", "No {}s found in the database.".format(item_type.capitalize()))
            return

        # Display item details in a new window
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete {}s".format(item_type.capitalize()))

        # Create a listbox to display items
        listbox = tk.Listbox(delete_window, width=50)
        listbox.pack(padx=10, pady=10)

        # Insert items into the listbox
        for item in items:
            listbox.insert(tk.END, item)

        # Function to handle item selection for deletion
        def delete_selected_item():
            selected_index = listbox.curselection()[0]
            selected_item = items[selected_index]
            confirm_delete(selected_item)

        # Button to select an item for deletion
        delete_button = tk.Button(delete_window, text="Delete Selected Item", command=delete_selected_item)
        delete_button.pack(pady=5)

        # Function to confirm deletion of selected item
        def confirm_delete(item):
            confirm_message = "Are you sure you want to delete this {}?\n{}".format(item_type.capitalize(), item)
            if messagebox.askyesno("Confirm Deletion", confirm_message):
                perform_deletion(item)

        # Function to perform deletion of selected item from the database
        def perform_deletion(item):
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="mathsboard",
                    database="video_store"
                )

                cursor = connection.cursor()

                if item_type == "movie":
                    delete_query = "DELETE FROM movie WHERE MovieID = %s"
                elif item_type == "vcr":
                    delete_query = "DELETE FROM vcr WHERE VCRID = %s"
                elif item_type == "video_camera":
                    delete_query = "DELETE FROM video_camera WHERE VCamID = %s"
                
                cursor.execute(delete_query, (item[0],))
                connection.commit()
                messagebox.showinfo("Success", "{} deleted successfully".format(item_type.capitalize()))
                delete_window.destroy()

                cursor.close()
                connection.close()

            except mysql.connector.Error as error:
                messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

# Function to add a new employee
def add_employee(name, position):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )

        cursor = connection.cursor()
        
        query = "INSERT INTO employees (Name, Position) VALUES (%s, %s)"
        cursor.execute(query, (name, position))
        connection.commit()

        messagebox.showinfo("Success", "Employee added successfully")

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

# Function to add a new customer
def add_customer(name, email, phone):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )

        cursor = connection.cursor()
        
        query = "INSERT INTO customers (Name, Email, Phone) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, phone))
        connection.commit()

        messagebox.showinfo("Success", "Customer added successfully")

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

# Function to manage store (employees, customers, transactions)
def open_store_management_window(parent):
    store_management_window = tk.Toplevel(parent)
    store_management_window.title("Store Management")

    # Create buttons to manage employees and customers
    add_employee_button = tk.Button(store_management_window, text="Add Employee", command=open_add_employee_window)
    add_employee_button.pack(pady=10)

    # Create a button to display customer transactions
    display_transactions_button = tk.Button(store_management_window, text="Display Customer Transactions", command=display_customer_transactions)
    display_transactions_button.pack(pady=20)

    # Create a button to display customer details
    display_transactions_button = tk.Button(store_management_window, text="Display Customer Details", command=display_customer_details)
    display_transactions_button.pack(pady=20)

    # Create a button to display employee details
    display_transactions_button = tk.Button(store_management_window, text="Display Employee Details", command=display_employee_details)
    display_transactions_button.pack(pady=20)

# Function to open window for adding a new employee
def open_add_employee_window():
    add_employee_window = tk.Toplevel(root)
    add_employee_window.title("Add Employee")

    # Create labels and entry fields for employee details
    name_label = tk.Label(add_employee_window, text="Name:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(add_employee_window)
    name_entry.pack(pady=5)

    position_label = tk.Label(add_employee_window, text="Position:")
    position_label.pack(pady=5)
    position_entry = tk.Entry(add_employee_window)
    position_entry.pack(pady=5)

    # Create button to add employee
    add_button = tk.Button(add_employee_window, text="Add Employee", command=lambda: add_employee(
        name_entry.get(),
        position_entry.get()
    ))
    add_button.pack(pady=10)

def display_customer_transactions():
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )
        cursor = connection.cursor()

        # Fetch customer transactions from the database
        cursor.execute("SELECT * FROM customer_transactions")
        transactions = cursor.fetchall()

        if not transactions:
            messagebox.showinfo("No Transactions", "No Transactions found in the database.")
            return
        
        # Display transaction details in a new window
        view_window = tk.Toplevel(root)
        view_window.title("View Customer Transactions")

        # Create a text widget to display transaction details
        text_widget = tk.Text(view_window, height=10, width=50)
        text_widget.pack(padx=10, pady=10)

        # Get column names
        cursor.execute("SHOW COLUMNS FROM customer_transactions")
        columns = [column[0] for column in cursor.fetchall()]

        # Insert column names followed by their corresponding values for each item
        for transaction in transactions:
            for i in range(len(columns)):
                text_widget.insert(tk.END, "{}: {}\n".format(columns[i], transaction[i]))
            text_widget.insert(tk.END, "---------------------------------\n\n")

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

# Add functionality for managing transactions (buy/rent items) within the store management window
# For example, you can create functions to handle buying or renting items by customers
# Function to open the transaction management window
def open_transaction_management_window(parent):
    transaction_management_window = tk.Toplevel(parent)
    transaction_management_window.title("Transaction Management")

    # Create radio buttons to select transaction type (buy/rent)
    transaction_type = tk.StringVar(value="buy")
    buy_radio = tk.Radiobutton(transaction_management_window, text="Buy", variable=transaction_type, value="buy")
    buy_radio.grid(row=0, column=0, padx=10, pady=5)
    rent_radio = tk.Radiobutton(transaction_management_window, text="Rent", variable=transaction_type, value="rent")
    rent_radio.grid(row=0, column=1, padx=10, pady=5)

    # Create radio buttons to select item type (movie/VCR/video camera)
    item_type = tk.StringVar(value="movie")
    movie_radio = tk.Radiobutton(transaction_management_window, text="Movie", variable=item_type, value="movie")
    movie_radio.grid(row=1, column=0, padx=10, pady=5)
    vcr_radio = tk.Radiobutton(transaction_management_window, text="VCR", variable=item_type, value="vcr")
    vcr_radio.grid(row=1, column=1, padx=10, pady=5)
    video_camera_radio = tk.Radiobutton(transaction_management_window, text="Video Camera", variable=item_type, value="video_camera")
    video_camera_radio.grid(row=1, column=2, padx=10, pady=5)

    # Label and entry for item ID
    item_id_label = tk.Label(transaction_management_window, text="Item ID:")
    item_id_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    item_id_entry = tk.Entry(transaction_management_window)
    item_id_entry.grid(row=2, column=1, padx=10, pady=5)

    amount_label = tk.Label(transaction_management_window, text="Amount Payed:")
    amount_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    amount_entry = tk.Entry(transaction_management_window)
    amount_entry.grid(row=3, column=1, padx=10, pady=5)

    due_date_label = tk.Label(transaction_management_window, text="Due Date (YYYY-MM-DD):")
    due_date_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    due_date_entry = tk.Entry(transaction_management_window)
    due_date_entry.grid(row=4, column=1, padx=10, pady=5)

    # Label and entry for employee ID
    employee_id_label = tk.Label(transaction_management_window, text="Employee ID:")
    employee_id_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    employee_id_entry = tk.Entry(transaction_management_window)
    employee_id_entry.grid(row=5, column=1, padx=10, pady=5)

    # Label and entry for customer details
    customer_name_label = tk.Label(transaction_management_window, text="Customer Name:")
    customer_name_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
    customer_name_entry = tk.Entry(transaction_management_window)
    customer_name_entry.grid(row=6, column=1, padx=10, pady=5)

    customer_email_label = tk.Label(transaction_management_window, text="Customer Email:")
    customer_email_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
    customer_email_entry = tk.Entry(transaction_management_window)
    customer_email_entry.grid(row=7, column=1, padx=10, pady=5)

    customer_phone_label = tk.Label(transaction_management_window, text="Customer Phone:")
    customer_phone_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
    customer_phone_entry = tk.Entry(transaction_management_window)
    customer_phone_entry.grid(row=8, column=1, padx=10, pady=5)

    # Button to add transaction
    add_transaction_button = tk.Button(transaction_management_window, text="Add Transaction", command=lambda: add_transaction(
        transaction_type.get(),
        item_type.get(),
        item_id_entry.get(),
        amount_entry.get(),
        due_date_entry.get(),
        employee_id_entry.get(),
        customer_name_entry.get(),
        customer_email_entry.get(),
        customer_phone_entry.get()
    ))
    add_transaction_button.grid(row=9, columnspan=2, pady=10)


def add_transaction(transaction_type, item_type, item_id, amount_payed, due_date, employee_id, customer_name, customer_email, customer_phone):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )
        cursor = connection.cursor()

        # Determine the appropriate transaction table based on the item type
        if item_type == "movie":
            transaction_table = "movie_transactions"
            item_id_column = "MovieID"
        elif item_type == "vcr":
            transaction_table = "vcr_transactions"
            item_id_column = "VCRID"
        elif item_type == "video_camera":
            transaction_table = "video_camera_transactions"
            item_id_column = "VCamID"
        else:
            messagebox.showerror("Error", "Invalid item type: {}".format(item_type))
            return

        # Validate if the item ID exists in the catalog
        cursor.execute("SELECT * FROM {} WHERE {} = %s".format(item_type, item_id_column), (item_id,))
        item = cursor.fetchone()

        if not item:
            messagebox.showerror("Error", "Item with ID {} not found in the catalog.".format(item_id))
            return
        
        # Check if the amount paid matches the catalog price
        catalog_price = item[3]  # Assuming price is stored in the third column
        if float(amount_payed) != catalog_price:
            messagebox.showerror("Error", "Amount paid does not match the catalog price.")
            return

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", customer_email):
            messagebox.showerror("Error", "Invalid email format.")
            return
        
        # Validate phone number format and length
        if not re.match(r"^\d{10}$", customer_phone):
            messagebox.showerror("Error", "Invalid phone number format. Please enter a 10-digit number.")
            return
        
        # Add customer to the customers table if not already exists
        cursor.execute("SELECT CustomerID FROM customers WHERE Name = %s AND Email = %s AND Phone = %s",
                       (customer_name, customer_email, customer_phone))
        customer = cursor.fetchone()
        if not customer:
            cursor.execute("INSERT INTO customers (Name, Email, Phone) VALUES (%s, %s, %s)",
                           (customer_name, customer_email, customer_phone))
            connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            customer_id = cursor.fetchone()[0]
        else:
            customer_id = customer[0]

        # Add transaction to the appropriate transaction table
        query = "INSERT INTO {} (TType, {}, AmountPayed, DueDate, EmployeeID, CustomerID) VALUES (%s, %s, %s, %s, %s, %s)".format(
            transaction_table, item_id_column)
        cursor.execute(query, (transaction_type, item_id, amount_payed, due_date, employee_id, customer_id))
        connection.commit()

        customer_transaction_query = "INSERT INTO customer_transactions (TType, ItemID, AmountPayed, DueDate, CustomerID, EmployeeID) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(customer_transaction_query, (transaction_type, item_id, amount_payed, due_date, customer_id, employee_id))
        connection.commit()


        messagebox.showinfo("Success", "Transaction added successfully")

    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to connect to database: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def display_customer_details():
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )
        cursor = connection.cursor()

        # Fetch customer details from the database
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()

        if not customers:
            messagebox.showinfo("No Items", "No customers found in the database.")
            return

        # Display item details in a new window
        customer_details_window = tk.Toplevel(root)
        customer_details_window.title("Customer Details")

        # Create a text widget to display item details
        text_widget = tk.Text(customer_details_window, height=10, width=50)
        text_widget.pack(padx=10, pady=10)

        # Get column names
        cursor.execute("SHOW COLUMNS FROM customers")
        columns = [column[0] for column in cursor.fetchall()]

        # Insert column names followed by their corresponding values for each item
        for customer in customers:
            for i in range(len(columns)):
                text_widget.insert(tk.END, "{}: {}\n".format(columns[i], customer[i]))
            text_widget.insert(tk.END, "---------------------------------\n\n")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def display_employee_details():
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mathsboard",
            database="video_store"
        )
        cursor = connection.cursor()

        # Fetch employee details from the database
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        if not employees:
            messagebox.showinfo("No Items", "No employees found in the database.")
            return

        # Display item details in a new window
        employee_details_window = tk.Toplevel(root)
        employee_details_window.title("Employee Details")

        # Create a text widget to display item details
        text_widget = tk.Text(employee_details_window, height=10, width=50)
        text_widget.pack(padx=10, pady=10)

        # Get column names
        cursor.execute("SHOW COLUMNS FROM employees")
        columns = [column[0] for column in cursor.fetchall()]

        # Insert column names followed by their corresponding values for each item
        for employee in employees:
            for i in range(len(columns)):
                text_widget.insert(tk.END, "{}: {}\n".format(columns[i], employee[i]))
            text_widget.insert(tk.END, "---------------------------------\n\n")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Create main window
root = tk.Tk()
root.title("Video Store Management System - Login")

# Test the function
create_database()
# Initialize database (create users table and insert sample user record)
initialize_database()

# Create username label and entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=5)

# Create password label and entry
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Create login button
login_button = tk.Button(root, text="Login", command=authenticate_user)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
