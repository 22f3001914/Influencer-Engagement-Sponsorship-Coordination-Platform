from flask import Flask
from backend.models import *
app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
app.secret_key = "secret key"
from backend.controllers import *
if __name__ == '__main__':
    app.run()

    
