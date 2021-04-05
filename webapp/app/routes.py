from flask import request, render_template, url_for, redirect, flash, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, ConnectionForm, UpdateConnectionForm
from app.models import User, Connection
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def start():
    return render_template('exemplum-startpage.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    connections = Connection.query.all() #filter(user_id.has(USER=current_user.username))
    filter_con = []
    new_connections = [] 
    print(connections)
    x = 0
    for connection in connections:
        if str(connection.USER)[5:] != "'" + current_user.username + "'":
            print(f'{str(connection.USER)[5:]} != {current_user.username}')
            
            
        else:
            print(f'{str(connection.USER)[5:]} == {current_user.username}')
            filter_con.append(x)
        x += 1

    print(filter_con)
    
    for i in filter_con:
        new_connections.append(connections[i])
    print(new_connections)
    return render_template('exemplum-home.html', connections=new_connections)



@app.route('/create_account', methods=['GET','POST'])
def create_account():
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password=hashed_password,user_key=form.user_key.data,user_secret=form.user_secret.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created For {form.username.data}')
        
        return redirect(url_for('login'))

    return render_template('exemplum-signup.html', title='SignUp', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unsuccessful login')

    return render_template('exemplum-login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.user_key = form.user_key.data
        current_user.user_secret = form.user_secret.data
        db.session.commit()
        flash('Account Updated')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username 
        form.user_key.data = current_user.user_key

    
    return render_template('exemplum-account.html', title='Account', form=form)
@app.route("/new-connection", methods=['GET','POST'])
@login_required
def new_connection():
    connections = Connection.query.all() #filter(user_id.has(USER=current_user.username))
    filter_con = []
    new_connections = [] 
    print(connections)
    x = 0
    for connection in connections:
        if str(connection.USER)[5:] != "'" + current_user.username + "'":
            print(f'{str(connection.USER)[5:]} != {current_user.username}')
            
            
        else:
            print(f'{str(connection.USER)[5:]} == {current_user.username}')
            filter_con.append(x)
        x += 1

    print(filter_con)
    
    for i in filter_con:
        new_connections.append(connections[i])

    form = ConnectionForm()
    if form.validate_on_submit():
        connection = Connection(name=form.name.data, key=form.key.data, secret=form.secret.data, USER=current_user)
        db.session.add(connection)
        db.session.commit()
        flash('Connection Established')
        return redirect(url_for('home'))
    
    return render_template('exemplum-new-connection.html',form=form, connections=new_connections)

@app.route("/connection/<int:connection_id>", methods=['GET','POST'])
@login_required
def specific_connection(connection_id):
    connections = Connection.query.all() #filter(user_id.has(USER=current_user.username))
    filter_con = []
    new_connections = [] 
    print(connections)
    x = 0
    for connection in connections:
        if str(connection.USER)[5:] != "'" + current_user.username + "'":
            print(f'{str(connection.USER)[5:]} != {current_user.username}')
            
            
        else:
            print(f'{str(connection.USER)[5:]} == {current_user.username}')
            filter_con.append(x)
        x += 1

    print(filter_con)
    
    for i in filter_con:
        new_connections.append(connections[i])
    connection = Connection.query.get_or_404(connection_id)
    if connection.USER != current_user:
        abort(403)
    coins = [] 
    y = 0
    while y < 20:
        nameforcoin = 'Coin' + str(y)
        coins.append(nameforcoin)
        y += 1
    form = UpdateConnectionForm()
    if form.validate_on_submit():
        connection.name = form.name.data
        connection.key = form.key.data
        connection.secret = form.secret.data
        db.session.commit()
        flash('Account Updated')

        return redirect(url_for('specific_connection', connection_id=connection.id))
    elif request.method == 'GET':
        form.name.data = connection.name 
        form.key.data = connection.key

    return render_template('exemplum-specific-connection.html', title=connection.name, sp_connection=connection, connections=new_connections, coins=coins, form=form)

@app.route("/connection/<int:connection_id>/delete", methods=['GET','POST'])
@login_required
def delete_connection(connection_id):
    connection = Connection.query.get_or_404(connection_id)
    if connection.USER != current_user:
        abort(403)
    db.session.delete(connection)
    db.session.commit()
    return redirect(url_for('home'))