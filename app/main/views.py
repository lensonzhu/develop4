from flask import Flask,render_template,redirect,url_for,session
from .forms import NameForm
from .. models import User
from ..email import send_email
from .. import db
from . import main


@main.route('/',methods=['GET','POST'])
def index():
    form =NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'],'New user','mail/new_user',user=user)
        else:
            session['known']=True
        session['name']=form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',form=form,name=session.get('name'),knowm=session.get('known',False))

