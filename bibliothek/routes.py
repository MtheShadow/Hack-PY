from bibliothek import app, db, mail, limiter
from flask import render_template 
from flask import request, redirect, url_for, session
from flask_mail import Message
from sqlalchemy import text
import re
import json
import random

@app.route('/')
def home_page():
    return render_template('home.html', isLoggedIn=isLoggedIn())

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute",methods=['POST'])
def login_page():
    if request.method == 'POST':
        print("post")
    
        username = request.form.get('Username')
        password = request.form.get('Password')

        print(username, password)
        
        query_stmt = f"SELECT username from testusers where username = :username and password = :password"
        print(query_stmt)
        result = db.session.execute(text(query_stmt), {'username': username, 'password': password})
        user = result.fetchall()
        
        query_stmt = f"SELECT email_address from testusers where username = :username and password = :password"
        print(query_stmt)
        result = db.session.execute(text(query_stmt), {'username': username, 'password': password})
        email = result.fetchall()

        print(email)
        print(user)

        if not user:
            print("user not found")
            return render_template('login.html', isLoggedIn=isLoggedIn())
        else:
            print("user found")
            mail_address = email[0][0]
            username = user[0][0]
            #resp.set_cookie('username', username)
            #session['username'] = username
            global global_username
            global global_mail
            global_username = username
            global_mail = mail_address
            return redirect('/2FA')

        return render_template('login.html', isLoggedIn=isLoggedIn())
    
    return render_template('login.html', isLoggedIn=isLoggedIn())

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        print("post")
    
        username = request.form.get('Username')
        email = request.form.get('Email')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        print(username, email, password1, password2)

        if password1 != password2:
            print("passwords do not match")
            return render_template('register.html', isLoggedIn=isLoggedIn())
        
        query_stmt = f"insert into testusers (username, email_address, password) values (:username, :email, :password1)"
        db.session.execute(text(query_stmt), {'username': username, 'email': email, 'password1': password1})	
        db.session.commit()
        print("user created")

        query_stmt = f"SELECT username from testusers where username = :username and password = :password1"
        result = db.session.execute(text(query_stmt), {'username': username, 'password1': password1})
        user = result.fetchall()

        if not user:
            print("user not created")
            return render_template('register.html', isLoggedIn=isLoggedIn())
        else:
            print("user found")
            resp = redirect('/books')
            #resp.set_cookie('username', username)
            session['username'] = username
            return resp


        return render_template('register.html', isLoggedIn=isLoggedIn())
    
    return render_template('register.html', isLoggedIn=isLoggedIn())

@app.route('/books')
def books_page():
    if not session.get('username'):
        return redirect(url_for('login_page'))

    query_stmt = f"SELECT * from books"
    result = db.session.execute(text(query_stmt))
    items = result.fetchall()
    #name = session['username'] #request.cookies.get('username')

    print(items)

    return render_template('books.html', items=items, isLoggedIn=isLoggedIn())

@app.route('/addBook', methods=['GET', 'POST'])
def addBook_page():
    if not session.get('username'):
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        print("post")

        title = request.form.get('Title')
        isbn = request.form.get('ISBN')
        description = request.form.get('Description')
        author = request.form.get('Author') 
        date = request.form.get('ReleaseDate')

        print(f"{title}, {isbn}, {description}, {author}, {date}")
        
        query_stmt = f"insert into books (title, isbn, description, author, releaseDate) values (:title, :isbn, :description, :author, :date)"
        db.session.execute(text(query_stmt), {
            'title': title,
            'isbn': isbn,
            'description': description,
            'author': author,
            'date': date
        })
        db.session.commit()
        print("book created")

        resp = redirect('/books')
        return resp

    return render_template('addBook.html', isLoggedIn=isLoggedIn())


@app.route('/bookDetails')
def bookDetails_page():
    if not session.get('username'):
        return redirect(url_for('login_page'))

    book_id = request.args.get('id')
    query_stmt = f"SELECT * from books where bookID = :book_id"
    result = db.session.execute(text(query_stmt),{'book_id': book_id})
    item = result.fetchall()

    print(item)

    return render_template('bookDetails.html', item=item[0], isLoggedIn=isLoggedIn())

@app.route('/2FA', methods=['GET','POST'])
def twoFA_page():
    
    if request.method == 'GET':
        global global_code2FA
        global_code2FA = ""

  
        for i in range(5):
            global_code2FA += str(random.randint(0, 9))

        send2FAEmail(global_mail, global_code2FA)

    if request.method == 'POST':
        print("post")
        
        entered_code = request.form.get('twoFactor')
        print(entered_code)

        if entered_code == global_code2FA:
            print("2FA successful")
            session['username'] = global_username
            return redirect('/books')
        else:
            print("2FA failed")
            return redirect('/login')


    return render_template('2FA.html', isLoggedIn=isLoggedIn())


@app.route('/logout')
def logout():
    resp = redirect('/')
    #resp.set_cookie('username', '', expires=0)
    session.pop('username', None)
    return resp

@app.route('/stealing', methods=['POST'])
def stealing():
    if request.method == 'POST':
        print("post")
        
        jsonData = json.loads(request.data)
        print(jsonData["cookie"])
        

    

    resp = redirect('/books')
    return resp

def isLoggedIn():
    if session.get('username'):
        return True
    else:
        return False

def send2FAEmail(email, code):
    msg = Message('Your 2FA Code', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Your 2FA code is: {code}'
    mail.send(msg)
    print(f"Sent 2FA code {code} to {email}")