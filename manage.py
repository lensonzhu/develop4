from flask import Flask
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
import os
from app import create_app,db

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
manager=Manager(app)
migrate=Migrate(app,db)


def make_shell():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command('shell',Shell(make_context=make_shell))
manager.add_command('db',MigrateCommand)
#@app.route('/')
#def index():
#    return 'hello world'

#@app.route('/user/<name>')
#def user(name):
#    return '<h1>hello %s</h1>' % name

if __name__=='__main__':
    manager.run()
