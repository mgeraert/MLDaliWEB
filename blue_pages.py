from flask import Blueprint, request
from classes.Database import Database
import json

pages = Blueprint('pages', __name__)


@pages.route("/getPages")
def get_pages():

    db = Database()
    db.conn.row_factory = dict_factory
    c = db.conn.cursor()
    sql_string = 'SELECT * FROM Pages ORDER BY page_sort_order ASC'
    c.execute(sql_string)
    data = c.fetchall()
    return json.dumps(data)


@pages.route("/getPage", methods=['GET'])
def get_page():
    page_id = request.args.get('page_id')
    db = Database()
    db.conn.row_factory = dict_factory
    c = db.conn.cursor()
    sql_string = 'SELECT * FROM Pages WHERE ID=' + page_id
    c.execute(sql_string)
    data = c.fetchall()
    return json.dumps(data)

@pages.route("/InsertPage", methods=['GET'])
def insert_page():
    db = Database()
    c = db.conn.cursor()
    sql_string = 'INSERT INTO pages (page_name, page_sort_order) VALUES ("new",1)'
    c.execute(sql_string)
    db.conn.commit()
    return 'http200'

@pages.route("/UpdatePage", methods=['GET'])
def update_page():

    page_id  = request.args.get('page_id')
    page_name = request.args.get('page_name')
    page_font_size = request.args.get('page_font_size')
    page_button_height = request.args.get('page_button_height')

    db = Database()
    c = db.conn.cursor()
    sql_string = 'UPDATE pages SET page_name="' + page_name + '", page_font_size=' + page_font_size + ', page_button_height=' + page_button_height + \
                                                               ' WHERE ID=' + page_id
    c.execute(sql_string)
    db.conn.commit()
    return 'http200'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

