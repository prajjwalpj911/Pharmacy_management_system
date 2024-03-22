# app.py

from flask import Flask, render_template, request, redirect, send_from_directory
import mysql.connector

app = Flask(__name__)


# Connect to the MySQL database (replace with your database details)
db = mysql.connector.connect(
    host="localhost",
    user="prajjwal",
    password="Autoexpo@1",
    database="pharmacy"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create a table for medicines if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        quantity INT,
        price DECIMAL(10, 2)
    )
""")

# Function to add a new medicine to the inventory
def add_medicine(name, quantity, price):
    cursor.execute("INSERT INTO medicines (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
    db.commit()

# Function to view the inventory
def view_inventory():
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()

    return medicines

# Function to sell a medicine by ID
def sell_medicine_by_id(medicine_id, quantity_sold):
    cursor.execute("SELECT * FROM medicines WHERE id = %s", (medicine_id,))
    medicine = cursor.fetchone()

    if medicine:
        if medicine[2] >= quantity_sold:
            total_price = quantity_sold * medicine[3]
            cursor.execute("UPDATE medicines SET quantity = quantity - %s WHERE id = %s", (quantity_sold, medicine_id))
            db.commit()
            return f"Sold {quantity_sold} units of {medicine[1]} for Rs.{total_price:.2f}"
        else:
            return "Insufficient quantity in stock."
    else:
        return "Medicine not found in inventory."

# Function to sell a medicine by name
def sell_medicine_by_name(medicine_name, quantity_sold):
    cursor.execute("SELECT * FROM medicines WHERE name = %s", (medicine_name,))
    medicine = cursor.fetchone()

    if medicine:
        if medicine[2] >= quantity_sold:
            total_price = quantity_sold * medicine[3]
            cursor.execute("UPDATE medicines SET quantity = quantity - %s WHERE id = %s", (quantity_sold, medicine[0]))
            db.commit()
            return f"Sold {quantity_sold} units of {medicine[1]} for Rs.{total_price:.2f}"
        else:
            return "Insufficient quantity in stock."
    else:
        return "Medicine not found in inventory."

# Function to get starting names for the dropdown
def get_starting_names():
    cursor.execute("SELECT DISTINCT LEFT(name, 1) FROM medicines")
    starting_names = [name[0] for name in cursor.fetchall()]
    return starting_names

# Menu-driven interface
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        add_medicine(name, quantity, price)
    return render_template('add.html', starting_names=get_starting_names())

@app.route('/view')
def view():
    medicines = view_inventory()
    return render_template('view.html', medicines=medicines)

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        sell_option = request.form['sell_option']
        quantity_sold = int(request.form['quantity_sold'])

        if sell_option == 'by_id':
            medicine_id = int(request.form['medicine_id'])
            message = sell_medicine_by_id(medicine_id, quantity_sold)
        elif sell_option == 'by_name':
            medicine_name = request.form['medicine_name']
            message = sell_medicine_by_name(medicine_name, quantity_sold)

        return message

    medicines = view_inventory()
    return render_template('sell.html', medicines=medicines)

# Serve static files (CSS, images, etc.)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('', filename)

if __name__ == '__main__':
    # app.run(debug=True)  # use it when you want to use it on the same machine
    app.run(host='0.0.0.0', port=8080, debug=True)  # by it we can use it on mobile phone using ip address  192.168.4.103:5000

