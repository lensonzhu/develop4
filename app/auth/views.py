from flask import render_template,redirect,url_for,flash
from . import auth
from .. models import User
from . forms import LoginForm,RegisterForm,ChangePasswordForm,ResetPasswordRequestForm,ChangeEmailForm

from flask_login import login_user,logout_user,login_required,current_user
from .. import db
from .. email import send_email
from flask import request


@auth.route('/change_email',methods=['GET','POST'])
@login_required
def change_email_request():
    form=ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email=form.email.data
            token=curreny_user.generate_email_change_token(new_email)
            send_email(new_email,'Confirm your email address','auth/email/change_email',user=current_user,token=token)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password')
    return render_template('auth/email/change_email.html',form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Has been changed')
    else:
        flash('Invalid request')
    return redirect(url_for('main.index'))

@auth.route('/resetpassword',methods=['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form=ResetPasswordRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            token=user.reset_token()
            send_email(user.email,'Reset your password','auth/email/reset_password',user=user,token=token,next=request.args.get('next'))
        flash('Send you email confirm')
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset',form=form)


@auth.route('/resetpassword/<token>',methods=['GET','POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form=ResetPasswordRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token,form.password.data):
            flash('Password has been changed')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/password_reset',form=form)

@auth.route('/updatepassword',methods=['GET','POST'])
@login_required
def updatepassword():
    form=ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password=form.password.data
            db.session.add(current_user)
            flash('Password be Changed')
            print('newpaswword========',current_user)
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid password')
    print('-----------',form)
    return render_template('auth/updatepassword.html',form=form)

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
