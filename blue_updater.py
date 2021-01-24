from flask import Blueprint, request, render_template
from git import Repo

updatr = Blueprint('updater', __name__)


@updatr.route("/updater")
def updater():
    return render_template('updater.html')


@updatr.route("/update")
def update():
    Repo.clone_from('https://github.com/mgeraert/MLDaliWEB.git',
                    r'C:\Users\marcg\OneDrive\Documents\updatetest',
                    recursive=True)
