from flask import request, redirect, render_template
from models import User, database
from ..extensions import bcrypt


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password_hash=hashed_password, role='user')
        database.session.add(new_user)
        database.session.commit()
        return redirect('/login')
    return render_template('register.html')

