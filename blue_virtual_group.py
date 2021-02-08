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
    sql_string = 'INSERT INTO virtual_group (name) VALUES ("' + group_name + '")'
    db.execute(sql_string)
    return 'http200'

@virtual_group.route('/RemoveVirtualGroup', methods=['GET'])
def remove_virtual_group():
    virtual_group_ID = request.args.get('virtual_group_id')
    db = Database()
    sql_string = 'DELETE FROM virtual_group_items WHERE virtual_group_id = ' + virtual_group_ID
    db.execute(sql_string)
    sql_string = 'DELETE FROM virtual_group WHERE ID = ' + virtual_group_ID
    db.execute(sql_string)
    return 'http200'

@virtual_group.route('/RenameVirtualGroup', methods=['GET'])
def rename_virtual_group():
    virtual_group_ID = request.args.get('virtual_group_id')
    group_name = request.args.get('new_name')
    db = Database()
    sql_string = 'UPDATE virtual_group SET name="' + group_name + '" WHERE ID = ' + virtual_group_ID
    db.execute(sql_string)
    return 'http200'

@virtual_group.route('/GetBallastNotInGroup', methods=['GET'])
def get_ballasts_not_in_group():
    virtual_group_id= request.args.get('virtual_group_id')
    channel_number = request.args.get('channel_number')
    db = Database()
    sql_string = 'SELECT ballasts.ID as BallastID, ballast_name, virtual_group_items.ballast_id FROM ballasts LEFT JOIN virtual_group_items ON ballasts.ID = virtual_group_items.ballast_id ' \
                 'WHERE ballast_channel = ' \
                 + channel_number + ' AND virtual_group_ID IS NULL ORDER BY ballast_short_address ASC'
    data = db.get_sql_data(sql_string)
    return json.dumps(data)

@virtual_group.route('/GetBallastInGroup', methods=['GET'])
def get_ballasts_in_group():
    virtual_group_id= request.args.get('virtual_group_id')
    channel_number = request.args.get('channel_number')
    db = Database()
    sql_string = 'SELECT ballasts.ID as BallastID, ballast_name, virtual_group_items.ballast_id FROM ballasts LEFT JOIN virtual_group_items ON ballasts.ID  = virtual_group_items.ballast_id ' \
                 'WHERE ballast_channel = ' \
                 + channel_number + ' AND virtual_group_ID=' + virtual_group_id + ' ORDER BY ballast_short_address ASC'
    data = db.get_sql_data(sql_string)
    return json.dumps(data)

@virtual_group.route('/AddBallastToVirtualGroup', methods=['GET'])
def add_ballast_to_virtual_group():
    ballast_id = request.args.get('ballast_id')
    virtual_group_id = request.args.get('virtual_group_id')
    db = Database()
    sql_string = 'INSERT INTO virtual_group_items (ballast_id, virtual_group_id) VALUES (' + ballast_id + ', ' + virtual_group_id + ')'
    db.execute(sql_string)
    return 'http200'

@virtual_group.route('/RemoveBallastFromVirtualGroup', methods=['GET'])
def remove_ballast_from_virtual_group():
    ballast_id = request.args.get('ballast_id')
    virtual_group_id = request.args.get('virtual_group_id')
    db = Database()
    sql_string = 'DELETE FROM virtual_group_items WHERE ballast_id=' + ballast_id + ' AND virtual_group_id=' + virtual_group_id
    db.execute(sql_string)
    return 'http200'


@virtual_group.route("/virtual_groups")
def beneden():
    return render_template('virtual_groups.html')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

