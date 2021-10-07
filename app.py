#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import secrets
import os
from PIL import Image
from datetime import datetime
from enum import unique
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_login.utils import login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from forms import *
from models import *
from config import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user, current_user, logout_user
from itsdangerous.url_safe import URLSafeTimedSerializer
from flask_mail import Message
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#----------------------------------------------------------------------------#
# Functions.
#----------------------------------------------------------------------------#
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)

    op_size = (200, 200)
    img = Image.open(form_picture)
    img.thumbnail(op_size)
    img.save(picture_path)
    return picture_fn

def save_art_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    op_size = (846, 480)
    img = Image.open(form_picture)
    img.thumbnail(op_size)
    img.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@artify.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
    {url_for('reset_token',token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made to your account
     '''
    mail.send(msg)
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    all_art = Art.query.all()
    counter = []
    for art in all_art:
        if art.counter > 1:
            counter.append(art.item_id)
    trending_art = []
    for id in counter[:4]:
        trending_art.append(Art.query.filter_by(item_id=id).first())
    return render_template('pages/homepage.html', items=trending_art)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Logged In Successfully, Welcome { user.fname }!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful! Please Check Your Email or Password", 'danger')
    return render_template('forms/login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Creating RegistrationForm class object
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(fname=form.fname.data, lname=form.lname.data, email=form.email.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account Created, Please Log In To Continue!', 'success')
        return redirect(url_for('login'))
    return render_template('forms/register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.email.data = current_user.email
    image_file = url_for('static', filename='/img/' + current_user.image_file)
    return render_template('pages/account.html', dp = image_file, form=form)


@app.route('/sell', methods=['GET', 'POST'])
def sell():
    form = SellersForm()
    if form.validate_on_submit():
        new_art = Art(artist_name=form.artist_name.data, title=form.title.data, description=form.description.data,category=form.category.data,price=form.price.data, item_quantity=form.quantity.data)
        if form.image.data:
           picture_file = save_art_picture(form.image.data)
           new_art.images = picture_file
        db.session.add(new_art)
        db.session.commit()
        flash('Item successfully added!', 'success')
        return redirect(url_for('sell'))
    print(form.errors)
    return render_template('pages/sell.html', form=form)

@app.route('/about')
def about():
    artist = Art.query.all()
    return render_template('pages/about.html', artist=artist)


@app.route('/categories')
def categories():
    paintings = Art.query.filter_by(category='Painting')
    drawings = Art.query.filter_by(category='Drawing/Sketch')
    digitalArt = Art.query.filter_by(category='Digital Art')
    handcrafts = Art.query.filter_by(category='Handcrafts')

    return render_template('pages/categories.html', paintings=paintings,drawings=drawings,digitalArt=digitalArt,handcrafts=handcrafts)


@app.route('/categories/paintings')
def paintings():
    paintings = Art.query.filter_by(category='Painting')

    return render_template('pages/paintings.html', paintings=paintings)


@app.route('/categories/digitalArt')
def digitalart():
    digitalArt = Art.query.filter_by(category='Digital Art')

    return render_template('pages/digitalArt.html',digitalArt=digitalArt)


@app.route('/categories/drawings')
def drawings():
    drawings = Art.query.filter_by(category='Drawing/Sketch')
    return render_template('pages/drawings.html', drawings=drawings)


@app.route('/categories/handcrafts')
def handcrafts():
    handcrafts = Art.query.filter_by(category='Handcrafts')

    return render_template('pages/handcrafts.html',handcrafts=handcrafts)


@app.route('/cart/') 
def cart():
    products = CartItem.query.all()
    price = []
    for product in products:
        price.append(product.price)
    cart_total = sum(price)
    cart_len = len(products)
    return render_template('pages/cart.html', products=products, cart_len=cart_len, cart_total=cart_total)

@app.route('/cart/<int:product_id>',methods=['GET','POST'])
def add_to_cart(product_id):
    items = Art.query.filter_by(item_id=product_id).all()
    for item in items:
        cart_item=CartItem(product_id=product_id,title=item.title,artist_name=item.artist_name,images=item.images,price=item.price,item_quantity=item.item_quantity)
    db.session.add(cart_item)
    db.session.commit()
    flash('Product Added to Cart Successfully!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/delete/<int:id>',methods=['GET','POST'])
def delete_from_cart(id):
    cart_item = CartItem.query.get(id)
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('cart'))
@app.route('/cart/clear_cart',methods=['GET','POST'])
def clear_cart():
    db.session.query(CartItem).delete()
    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/product/<int:product_id>',methods=['GET','POST'])
def single_product(product_id):
    products = Art.query.filter_by(item_id=product_id).all()
    cat=[]
    for product in products:
        cat.append(product.category)
        product.counter = product.counter + 1
        db.session.commit()
    similar_items = Art.query.filter_by(category=cat[0]).all()
    return render_template('pages/singleProduct.html', products=products, similar_items=similar_items)

@app.route('/checkout',methods=['GET','POST'])
def checkout():
    cart_items = CartItem.query.all()
    cart_len = len(cart_items)
    price=[]
    for item in cart_items:
        price.append(item.price)
    total_price = sum(price)
    if total_price < 1000:
        subtotal = total_price + 50
    else:
        subtotal = total_price
    return render_template('pages/checkout.html', cart_items=cart_items,total_price=total_price,cart_len=cart_len,subtotal=subtotal)

@app.route('/addAddress',methods=['GET','POST'])
def address():
    if current_user.is_authenticated:
        form = AddressForm()
        if form.validate_on_submit():
            current_user.address = form.address.data
            current_user.city = form.city.data
            current_user.state = form.state.data
            current_user.zip_code = form.zip_code.data
            db.session.commit()
            flash('Address Successfully Added, proceed with checkout', 'success')
            return redirect(url_for('checkout'))
        return render_template('pages/addaddress.html', form=form)
    else:
        flash('Please Log-IN to Continue', 'danger')
        return redirect(url_for('login'))    

@app.route('/checkout/final')
def final():
    items = CartItem.query.all()
    db.session.query(CartItem).delete()
    db.session.commit()
    return render_template('pages/orderPlaced.html',items=items)


@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('A resert password link has been sent to your email id', 'success')
        return redirect(url_for('login'))
    return render_template('pages/reset_request.html', form=form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This link is invalid or expired','danger')
        return redirect(url_for('reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_pass
        db.session.commit()
        flash('Your Password has been updated,Please login to continue', 'success')
        return redirect(url_for('login'))
    return render_template('pages/reset_token.html', form=form)
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
