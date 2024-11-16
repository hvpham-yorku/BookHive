from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    # Render the home.html template when the user is logged in
    return render_template("home.html", user=current_user)