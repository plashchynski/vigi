from flask import Blueprint, render_template

recordings_blueprint = Blueprint('recordings', __name__)

@recordings_blueprint.route('/recordings')
def index():
    return render_template('recordings.html')
