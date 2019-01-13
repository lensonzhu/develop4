from flask import render_template,redirect,url_for,flash
from . import auth
from .. models import User
from . forms import LoginForm,RegisterForm
from flask_login import login_user,logout_user,login_required,current_user
from .. import db
from .. email import send_email
from flask import request

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

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


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account')
    else:
        flash('Is ivalid has expired')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm your account','auth/email/confirm',user=current_user,token=token)
    flash('A new confirm email has been sent you by email')
    return redirect(url_for('main.index'))


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
        db.session.commit()
        token=user.generate_confirmation_token()
        send_email(user.email,'Confirm Your account','auth/email/confirm',user=user,token=token,)
        flash('You can now login, But you must be active your email ')
        print('user======',user)
        return redirect(url_for('auth.login'))
    print('user-------',form)
    return render_template('auth/register.html',form=form)
