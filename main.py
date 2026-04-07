from flask import Flask, render_template,request,redirect ,flash, url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'


@app.route('/')
def welcome():
    products = get_products()
    category = request.args.get('category')
    
    products = get_products_by_category(category)
    return render_template('welcome.html',products=products,
                           selected_category=category)


@app.route('/<int:id>/', methods=['GET', 'POST'])
def buy(id):
    product = get_product(id)

    if not product:
        return 'Error'
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session['user_id']
        add_order(id,user_id)
        return render_template('bought.html',i=product)
    return render_template('buy.html', i=product)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(password) < 8:
            flash('Password too short')
            return redirect(url_for('register'))
        if not any(num in '1234567890' for num in password):
            flash('Password must have at least one number')
            return redirect(url_for('register'))
        user = get_user(username)
        if user:
            flash('User already exists')
            return redirect(url_for('register'))
        hashedp = generate_password_hash(password)
        add_user(username,hashedp)
        flash('Successfully registered')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        if not user or not check_password_hash(user.password,password):
            flash('Wrong user or password')
            return redirect(url_for('login'))
        
        session['user_id'] = user.id
        flash('Successfully logged in')
        return redirect(url_for('welcome')) 
    return render_template('login.html')
        

@app.route('/account/')
def account():
    if 'user_id' not in session:
        return render_template('account.html',logged_in= False)
    
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    orders, products = get_orders(user_id)
    return render_template('account.html', logged_in=True, user=user, products=products)


@app.route('/logout/')
def logout():
    session.pop('user_id', None)  
    flash("Successfully logged out")
    return redirect(url_for('welcome'))


@app.route('/change-password/',methods=['POST','GET'])
def change_password():
    if 'user_id' not in session:
        flash('Please log in before changing the password')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = get_user_by_id(user_id)

    cur_pass = request.form['current_password']
    new_pass = request.form['new_password']

    if not check_password_hash(user.password,cur_pass):
        flash('Wrong currect password')
        return redirect(url_for('account'))
    if len(new_pass) < 8:
        flash('New password must contain atleast 8 characters')
        return redirect(url_for('account'))
    if not any(num in '1234567890' for num in new_pass):
        flash('New password must have atleast 1 number in it')
        return redirect(url_for('account'))
    
    new_hashed = generate_password_hash(new_pass)
    upd_password(user_id,new_hashed)
    flash('Password successfully changed')

    return redirect(url_for('account'))
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)