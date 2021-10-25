from flask import Flask
from flask import render_template, request, redirect, url_for, flash
#from flask_login import LoginManager

app = Flask(__name__,template_folder="views")
app.secret_key ="WilmerPerdomo"

from application.controllers import controllersUsers

