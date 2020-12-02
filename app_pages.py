from flask import Flask
import sqlite3


app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d





@app.route("/getPages")
def get_pages():
    sql_string = 'SELECT * FROM Pages ORDER BY page_sort_order ASC'
    data = get_sql_data(sql_string)
    return data[0]


def get_visual_item(self, visualID):
    sql_string = 'SELECT * FROM visual WHERE ID =' + str(visualID)
    data = self.get_sql_data(sql_string)
    return data[0]


def get_sql_data(self, sql_string):
    self.conn.row_factory = dict_factory
    c = self.conn.cursor()
    c.execute(sql_string)
    return c.fetchall()
