from flask import Blueprint, request, render_template
import os

updatr = Blueprint('updater', __name__)


@updatr.route("/updater")
def updater():
    return render_template('updater.html')



@updatr.route("/update")
def update():
    os.system('/etc/MLDali/updateMLDali.sh')
