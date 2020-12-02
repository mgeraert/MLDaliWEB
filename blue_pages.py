from flask import Blueprint
from classes.database import Database
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


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

