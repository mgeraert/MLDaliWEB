from flask import Blueprint, request, render_template
from classes.Database import Database
import json

virtual_group = Blueprint('virtual_group', __name__)


@virtual_group.route("/getVirtualGroups")
def get_virtual_groups():

    db = Database()
    db.conn.row_factory = dict_factory
    c = db.conn.cursor()
    sql_string = 'SELECT * FROM virtual_group ORDER BY name ASC'
    c.execute(sql_string)
    data = c.fetchall()
    return json.dumps(data)

@virtual_group.route('/InsertVirtualGroup', methods=['GET'])
def insert_virtual_group():
    group_name = request.args.get('group_name')
    db = Database()
    c = db.conn.cursor()
    sql_string = 'INSERT INTO virtual_group (name) VALUES =\'' + group_name + '\''
    c.execute(sql_string)
    return 'http200'

@virtual_group.route("/virtual_groups")
def beneden():
    return render_template('virtual_groups.html')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

