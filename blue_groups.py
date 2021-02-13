from flask import Blueprint, request
from classes.Database import Database
from classes.DaliChannels import DaliChannels
from classes.DaliChannel import DaliChannel

import json

groups = Blueprint('groups', __name__)

@groups.route('/AddBallastToGroup', methods=['GET'])
def add_ballast_to_group():
    group_number = request.args.get('group_number')
    ballast_id = request.args.get('ballast_id')
    db = Database()
    c = db.conn.cursor()
    sql_string = 'UPDATE ballasts SET ballast_group_' + str(group_number) + \
                 '=1 WHERE ID=' + str(ballast_id)
    c.execute(sql_string)
    db.conn.commit()
    return 'http200'
    return answer

@groups.route('/RemoveBallastFromGroup', methods=['GET'])
def remove_ballast_from_group():
    group_number = request.args.get('group_number')
    ballast_id = request.args.get('ballast_id')
    db = Database()
    c = db.conn.cursor()
    sql_string = 'UPDATE ballasts SET ballast_group_' + str(group_number) + \
                 '=0 WHERE ID=' + str(ballast_id)
    c.execute(sql_string)
    db.conn.commit()
    return 'http200'

@groups.route('/downloadGroupsFromBallast', methods=['GET'])
def download_groups_from_ballast():
    ballast_id = request.args.get('ballast_id')
    dcs = DaliChannels()
    db = Database()
    ballast = db.get_ballast(ballast_id)
    dc = dcs.get_chan(ballast.get('ballast_channel'))
    answer = dc.download_groups_from_ballast(ballast_id)
    return answer


def download_groups_from_ballast(self, ballast_id):
    db = Database()
    ballast = db.get_ballast(ballast_id)
    dc = DaliChannel()
    dc = dc.get_chan(ballast.get('ballast_channel'));
    dc.download_groups_from_ballast(ballast_id)
