# Import flask and template operators
from flask import Flask, redirect
from app.dashboards.controllers import dashboards
from app.auth.controllers import auth
from app.init_database import mongo


# Define the WSGI application object
app = Flask(__name__)
# Configurations
app.config.from_object('config')

mongo.init_app(app)


# Set the redirecting route for dashboard
@app.route('/')
def stats():
    return redirect('auth/login')


app.register_blueprint(dashboards)
app.register_blueprint(auth)