from flask import Flask, request, jsonify, render_template,session , flash , redirect , url_for
# from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_cors import CORS
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app) 

products = [
    {"id": 1, "name": "Golden Ring", "price": 1599, "img": "ring1.png", "category": "ring"},
    {"id": 2, "name": "Diamond Ring", "price": 849, "img": "ring2.png", "category": "ring"},
    {"id": 3, "name": "Silver Ring", "price": 499, "img": "ring3.png", "category": "ring"},
    {"id": 4, "name": "Pearl Bangle", "price": 2199, "img": "bangle2.png", "category": "bangle"},
    {"id": 5, "name": "Modern Ring", "price": 399, "img": "ring5.png", "category": "ring"},
    {"id": 6, "name": "Modern Ring", "price": 399, "img": "bangle3.png", "category": "ring"},
    {"id": 7, "name": "Modern Ring", "price": 399, "img": "bangle4.png", "category": "ring"},
    {"id": 8, "name": "Modern Ring", "price": 399, "img": "bangle5.png", "category": "ring"},
]


# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "hello@123"

db = SQLAlchemy(app)

# -------------------
# Database Model
# -------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

# -------------------
# Utility Functions
# -------------------
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

# -------------------
# Routes
# -------------------
@app.route('/')
def home():
    return render_template('index.html' , products=products)

# @app.route('/add_to_cart', methods=['POST'])
# def add_to_cart():
#     product_id = int(request.json['id'])

#     # product find karo
#     product = next((p for p in products if p['id'] == product_id), None)
#     if not product:
#         return jsonify({"success": False, "message": "Product not found"}), 404

#     # cart session me rakho
#     if "cart" not in session:
#         session["cart"] = []

#     cart = session["cart"]

#     # check if already exists
#     for item in cart:
#         if item["id"] == product_id:
#             item["quantity"] += 1
#             break
#     else:
#         cart.append({"id": product["id"], "name": product["name"], "price": product["price"], "quantity": 1})

#     session["cart"] = cart
#     return jsonify({"success": True, "cart": cart})

# @app.route('/cart')
# def view_cart():
#     cart = session.get("cart", [])
#     return jsonify(cart)



@app.route('/forgot_pass')
def Forgot_pass():
    return render_template('forgotpass.html')

@app.route('/index')
def coustumer_care():
    return render_template('coustcare.html')

# @app.route('/signup')
# def Sign_up():
#     return render_template('signup.html')

@app.route('/coustmure_care')
def index_home():
    return render_template('/index.html')

@app.route('/cart')
def cart():
    return render_template('bangle_cart.html')

@app.route('/shop')
def shop():
    return render_template('index.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route("/order_place")
def order_place():
   return render_template('orderplaced.html')


# Signup API
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        # Expecting JSON request
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Request must be JSON'}), 400

        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        # Validation
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        if not is_valid_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400

        # Duplicate check
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400

        # Save user
        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Signup successful'}), 201



# Login API
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

     # POST request handle karo

    if request.method == 'POST':
        data= request.get_json()
        email = request.get['email']
        password = request.get['password']
    
    if email and password :
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password): # (⚠️ real app me password hashing use karo)
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('login'))
        else:
            return "Invalid email or password"
    return render_template('login.html')


# ---------- Index ----------
@app.route('/')
def index():
    if 'user_id' in session:
        return f"Welcome {session['username']}! This is your home page."
    else:
        return "Welcome Guest! Please <a href='/login'>login</a> or <a href='/signup'>signup</a>."


# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def render():
    return render_template("product_showcase.html", products=products)
# -------------------
# Initialize DB
# -------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

