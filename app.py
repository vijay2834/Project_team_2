# app.py
from flask import Flask, render_template
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MySQL
mysql = MySQL(app)
app.extensions['mysql'] = mysql  # Store in extensions for easier access

# Make mysql available to routes
from routes import init_app
init_app(mysql)

# Register blueprints
from routes.main import main
from routes.auth import auth
from routes.pet import pet
from routes.product import product
from routes.cart import cart
from routes.user import user
from routes.admin import admin

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(pet)
app.register_blueprint(product)
app.register_blueprint(cart)
app.register_blueprint(user)
app.register_blueprint(admin)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('404.html', error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)