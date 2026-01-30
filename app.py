from flask import Flask, render_template, request, session
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store orders in memory
orders = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    name = request.form['name']
    pizza = request.form['pizza']
    size = request.form['size']
    quantity = request.form['quantity']
    
    # Generate order ID
    order_id = secrets.token_hex(4).upper()
    
    # Store order details
    orders[order_id] = {
        'name': name,
        'pizza': pizza,
        'size': size,
        'quantity': int(quantity),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'Confirmed'
    }
    
    return render_template('confirmation.html', 
                         order_id=order_id,
                         name=name, 
                         pizza=pizza, 
                         size=size, 
                         quantity=quantity)

@app.route('/tracking/<order_id>')
def tracking(order_id):
    if order_id in orders:
        order = orders[order_id]
        return render_template('tracking.html', order_id=order_id, order=order)
    return "Order not found", 404

@app.route('/payment/<order_id>')
def payment(order_id):
    if order_id in orders:
        order = orders[order_id]
        # Calculate price
        price = 8 if order['size'] == 'Small' else 12 if order['size'] == 'Medium' else 16
        total = price * order['quantity']
        return render_template('payment.html', order_id=order_id, order=order, total=total)
    return "Order not found", 404

@app.route('/delivery/<order_id>')
def delivery(order_id):
    if order_id in orders:
        order = orders[order_id]
        return render_template('delivery.html', order_id=order_id, order=order)
    return "Order not found", 404

if __name__ == '__main__':
    app.run(debug=True)
