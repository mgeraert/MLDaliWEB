from flask import Blueprint, request
from classes.Database import Database
import json

visual = Blueprint('visual', __name__)


@visual.route("/DeleteVisual", methods=['GET'])
def delete_visual():
    visual_id = request.args.get('ID')
    db = Database()
    c = db.conn.cursor()
    sql_string = 'DELETE FROM visual WHERE ID=' + visual_id
    c.execute(sql_string)
    db.conn.commit()
    return 'http200'

@visual.route("/ResizeVisual", methods=['GET'])
def resize_visual():
    visual_id = request.args.get('ID')
    col_width = request.args.get('col_width')
    db = Database()
    c = db.conn.cursor()
    sql_string = 'UPDATE visual SET visual_columns = ' +  col_width + ' WHERE ID=' + visual_id
    c.execute(sql_string)
    db.conn.commit()
    return 'http200'

