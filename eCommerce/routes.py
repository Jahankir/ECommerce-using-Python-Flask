from datetime import datetime
from eCommerce import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request, get_flashed_messages, session
from eCommerce.forms import RegisterForm, LoginForm 
from bson import ObjectId
from functools import wraps

# Custom decorator to check if the user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('please log in to access this page', category='info')
            return redirect(url_for('login_page'))
    return wrap

# Home page route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

#Market page route
@app.route('/market')
@is_logged_in
def market_page():
    items = db.items.find()
    return render_template('market.html',items=items)

# ---------USED TO ADD STOCKS IN DB---------------
#Stock Add page route
# @app.route('/stock_add', methods=['GET', 'POST'])
# def add_stock():
#     form = StockImport()
#     if form.validate_on_submit():
        
#         db.item.insert_one({
#              "name": form.name.data,
#              "barcode": form.barcode.data,
#              "price": form.price.data,
#              "desription": form.description.data,
#              "imageUrl": form.imageUrl.data #paths like '../static/product/laptop.png'
#             })
        
#         flash("Item Added Successfully", category='success')
#         return redirect(url_for('add_stock'))
#     if form.errors != {}:
#         for er_msg in form.errors.values():
#             flash(f'{er_msg[0]}', category='danger')
#     return render_template('stockadd.html', form=form)

# Registration page route
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form =RegisterForm() 
    if form.validate_on_submit():
        # Process registration form data
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        date_created = datetime.utcnow()

        db.user.insert_one ({
            'username': username,
            'email': email,
            'password' : password,
            'date_created' : date_created,
            'cart': []
        })
        session['logged_in'] = True
        session['email'] = email
        session['username'] = username
        flash(f"User Added Successfully {username}", category='success')
        return redirect(url_for('market_page'))
    
    if form.errors != {}:
        for er_msg in form.errors.values():
            flash(f'{er_msg[0]}', category='danger')
    return render_template('register.html', form=form)

# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # Process login form data
        email = form.email.data
        password = form.password.data
        user_data = db.user.find_one({'email': email})
        
        if user_data:
            check_password = bcrypt.check_password_hash(user_data['password'],password)
            if user_data and check_password:
                session['logged_in'] = True
                session['email'] = email
                session['username'] = user_data['username']

                flash(f'You are successfully logged in as {user_data['username']}', category='success')
                return redirect(url_for('market_page'))
            else:
                flash('email and password are not match, please try again', category='danger')
        else:
            flash('email and password are not match, please try again', category='danger')
    return render_template('login.html', form=form)

# Add to cart route
@app.route('/add_cart/<product_id>')
def add_to_cart(product_id):
    if 'email' in session:
        user = db.user.find_one({'email': session['email']})
        product = db.items.find_one({'_id': ObjectId(product_id)})
        product_exists = any(item["_id"] == ObjectId(product_id) for item in user["cart"])
        if product_exists:
            return redirect(url_for('market_page'))
        elif user and product:
            db.user.update_one({'_id': user['_id']}, {'$push': {'cart': product}})
            flash('successfully added to cart', category='success')
            return redirect(url_for('market_page'))
    return render_template('market.html')

# Remove from cart route
@app.route('/remove_cart/<product_id>')
def remove_from_cart(product_id):
    if 'email' in session:
        user = db.user.find_one({'email': session['email']})
        if user:
            db.user.update_one({'_id': user['_id']},{'$pull': {'cart': {'_id': ObjectId(product_id)}}})
            flash('Removed', category='success')
            return redirect(url_for('cart_page'))
    return render_template('cart.html')

# Cart page route
@app.route('/cart')
def cart_page():
    if 'email' in session:
        user = db.user.find_one({'email': session['email']})
        if user:
            cart_items = user['cart']
            return render_template('cart.html', cart_items= cart_items)
    return render_template('cart.html')

# Logout page route
@app.route('/logout')
def logout_page():
    session.clear()
    flash("You have been Logging Out!", category='info')
    return redirect(url_for('home'))