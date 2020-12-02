from flask import Flask, request
import json

import sqlite3


app = Flask(__name__)

n
@app.route('/DeleteVisual', methods=['GET'])
def delete_visual():
    visual_id = request.args.get('ID')
    sql_string = 'DELETE * FROM visual WHERE ID=' + visual_id
    c = self.conn.cursor()
    c.execute(sql_string)
    self.conn.commit()
    return 'http200'
