from flask import render_template,redirect,url_for,flash
from . import auth
from .. models import User
from . forms import LoginForm,RegisterForm
from flask_login import login_user,logout_user,login_required,current_user
from .. import db
from .. email import send_email

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            print('username======',user)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
        print('username////////',user)
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logouting. ')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,password=form.password.data,username=form.username.data)
        db.session.add(user)
        flash('You can now login')
        print('user======',user)
        return redirect(url_for('auth.login'))
    print('user-------',form)
    return render_template('auth/register.html',form=form)
