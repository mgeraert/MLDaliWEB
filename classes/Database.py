import sqlite3
import os
import platform


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database(object):

    def __init__(self):
        import configparser
        config = configparser.ConfigParser()
        current_os = platform.system().lower()

        if current_os.lower() == "windows":
            db_path = os.getcwd() + os.path.sep + '..' + os.path.sep + 'database' + os.path.sep
        else:
            #config.read('/var/www/webApp/webApp/mlconfig.ini')
            db_path = '/etc/MLDali/'

        config.read(db_path + 'mlconfig.ini')
        self.db_f_name = config['DEFAULT']['db_f_name']
        self.db_dir_name = db_path
        self.db_full_f_name = self.db_dir_name + self.db_f_name + '.db'
        self.conn = sqlite3.connect(self.db_full_f_name)

    def create_table(self, table_name):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string1 = 'CREATE TABLE IF NOT EXISTS ' \
                      + table_name \
                      + '(ID INTEGER PRIMARY KEY);'
        c.execute(sql_string1)
        conn.close()
        return

    def conn(self):
        return self.conn


    def insert_columns(self, table_name, columns):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        for column in columns:
            sql_string = 'ALTER TABLE ' + table_name + '  ADD COLUMN ' + column + ';'
            try:
                c.execute(sql_string)
            except sqlite3.Error as e:
                if not 'duplicate column name:' in e.args[0]:
                    print(e.args[0])
        conn.close()

    def select(self, sql_string):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def get_base_name(self):
        splitted = self.db_f_name.split('.')
        return splitted[0]

    def get_name(self):
        return self.db_f_name

    def set_name(self, new_name):
        import configparser
        config = configparser.ConfigParser()
        current_os = platform.system().lower()

        config_f_name = self.db_dir_name + 'mlconfig.ini'

        config.read(config_f_name)
        config['DEFAULT']['db_f_name'] = new_name
        with open(config_f_name, 'w') as configfile:
            config.write(configfile)
        dbname = self.db_dir_name + self.db_f_name
        new_dbname = self.db_dir_name + new_name
        os.rename(dbname + '.db', new_dbname + '.db')
        return 'http200'

    def execute(self, sql_string):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        c.execute(sql_string)
        conn.commit()
        conn.close()
        return

    def insert_ballasts(self):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT site_nr_of_chans FROM sites'
        c.execute(sql_string)
        nr_of_chans = c.fetchone()
        nr_of_chans = nr_of_chans["site_nr_of_chans"]

        conn.row_factory = ""

        for channel_nr in range(0, nr_of_chans):
            for ballast_nr in range(0, 64):
                sql_string = 'SELECT ID FROM ballasts WHERE ballast_short_address =' + \
                             str(ballast_nr) + ' AND ballast_channel=' + str(channel_nr + 1)
                c.execute(sql_string)
                if c.fetchone() is None:
                    sql_string = 'INSERT INTO ballasts (ballast_channel, ballast_short_address)  VALUES (' + \
                                 str(channel_nr + 1) + ',' + str(ballast_nr) + ')'
                    c.execute(sql_string)
                    conn.commit()
            for group_nr in range(0, 16):
                sql_string = 'SELECT ID FROM dali_groups WHERE dali_group_number =' + \
                             str(group_nr) + ' AND dali_group_channel=' + str(channel_nr + 1)
                c.execute(sql_string)
                if c.fetchone() is None:
                    sql_string = 'INSERT INTO dali_groups (dali_group_channel, dali_group_number)  VALUES (' + \
                                 str(channel_nr + 1) + ',' + str(group_nr) + ')'
                    c.execute(sql_string)
                    conn.commit()
        conn.close()
        return

    def get_channels(self):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM dalichannels'
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def get_pages(self):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM Pages ORDER BY page_sort_order ASC'
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def get_ballasts(self, channelnr):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string2 = 'SELECT * FROM ballasts WHERE ballast_channel=' + str(channelnr) + \
                      ' ORDER BY ballast_short_address ASC'
        c.execute(sql_string2)
        data = c.fetchall()
        conn.close()
        return data

    def get_ballast(self, i_d):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM ballasts WHERE ID=' + str(i_d)
        c.execute(sql_string)
        data = c.fetchall()
        conn.close
        return data[0]

    def get_ballast_by_short_address(self, sa):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM ballasts WHERE ballast_short_address=' + str(sa)
        c.execute(sql_string)
        data = c.fetchall()
        conn.close
        return data[0]


    def get_group(self, group_id):
        sql_string = 'SELECT * FROM dali_groups WHERE ID =' + str(group_id)
        data = self.get_sql_data(sql_string)
        return data[0]

    def get_groups(self, channelnr):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM dali_groups WHERE dali_group_channel=' + str(channelnr) + \
                     ' ORDER BY dali_group_number ASC'
        c.execute(sql_string)
        data = c.fetchall()
        conn.close
        return data

    def get_group_number(self, group_id):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'SELECT dali_group_number FROM dali_groups WHERE ID=' + str(group_id)
        c.execute(sql_string)
        data = c.fetchone()
        conn.close
        return data[0]

    def get_ballast_number(self, ballast_id):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'SELECT ballast_short_address FROM ballasts WHERE ID=' + str(ballast_id)
        c.execute(sql_string)
        data = c.fetchone()
        conn.close
        return data[0]

    def get_ballast_id_from_channel(self, channel_number):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT ID  FROM ballasts WHERE ballast_channel=' + str(channel_number)
        c.execute(sql_string)
        data = c.fetchall()
        conn.close
        return data

    def get_tree(self):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM dalichannels'
        c.execute(sql_string)
        data_channels = c.fetchall()
        tree_list = []
        tree_list.append({'name': 'Site', 'type': 0, 'id_of_type': -1})
        for row_channel in data_channels:
            tree_list.append({'name': row_channel.get('channel_name'), 'type': 1, 'id_of_type': row_channel.get('ID')})
            sql_string = 'SELECT * FROM dali_groups WHERE dali_group_channel=' + str(row_channel.get('channel_nr'))
            c.execute(sql_string)
            data_groups = c.fetchall()
            for row_group in data_groups:
                tree_list.append(
                    {'name': row_group.get('dali_group_name'), 'type': 2, 'id_of_type': row_group.get('ID')})
                sql_string = 'SELECT * FROM ballasts WHERE ballast_group_' + str(
                    row_group.get('dali_group_number')) + '=1 ORDER BY ballast_short_address ASC'
                c.execute(sql_string)
                data_ballasts = c.fetchall()
                for row_ballast in data_ballasts:
                    ballast_name = row_ballast.get('ballast_name');
                    if not ballast_name:
                        ballast_name = 'Ballast nr ' + str(row_ballast.get('ballast_short_address'))
                    tree_list.append(
                        {'name': ballast_name, 'type': 3, 'id_of_type': row_ballast.get('ID')})

            sql_string = 'SELECT * FROM ballasts WHERE ballast_group_0=0 AND ' + \
                        ' ballast_group_1=0  AND ballast_group_2=0 AND ballast_group_3=0 AND ' + \
                        ' ballast_group_1=0  AND ballast_group_2=0 AND ballast_group_3=0 AND ' + \
                        ' ballast_group_4=0  AND ballast_group_5=0 AND ballast_group_6=0 AND ' + \
                        ' ballast_group_7=0  AND ballast_group_8=0 AND ballast_group_9=0 AND ' + \
                        ' ballast_group_10=0  AND ballast_group_11=0 AND ballast_group_12=0 AND ' + \
                        ' ballast_group_13=0  AND ballast_group_14=0 AND ballast_group_15=0 AND ' + \
                        ' ballast_channel=' + str(row_channel.get('channel_nr'))
            c.execute(sql_string)
            data_ballasts = c.fetchall()
            for row_ballast in data_ballasts:
                tree_list.append(
                    {'name': row_ballast.get('ballast_name'), 'type': 2, 'id_of_type': row_ballast.get('ID')})

            data_groups = c.fetchall()
        conn.close
        return tree_list

    def get_ballast_id_and_channel(self, ID):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string2 = 'SELECT ballast_short_address, ballast_channel FROM ballasts WHERE ID=' + str(ID)
        c.execute(sql_string2)
        data = c.fetchall()
        conn.close()
        return data[0]

    def get_comport(self, channel_nr):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string2 = 'SELECT channel_com_port FROM dalichannels WHERE channel_nr=' + channel_nr.__str__()
        c.execute(sql_string2)
        data = c.fetchall()
        conn.close()
        return data[0]

    def update_com_port(self, channel_id, port_name):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string2 = 'UPDATE dalichannels SET  channel_com_port="' + port_name + \
                      '" WHERE ID=' + str(channel_id)
        c.execute(sql_string2)
        conn.commit()
        conn.close()
        return 'http200'

    def update_ballast_name(self, ballast_id, ballast_name):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string2 = 'UPDATE ballasts SET  ballast_name=\'' + ballast_name + \
                      '\' WHERE ID=' + str(ballast_id)
        c.execute(sql_string2)
        conn.commit()
        conn.close()

    def update_group_name(self, group_id, group_name):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'UPDATE dali_groups SET dali_group_name=\'' + group_name + \
                     '\' WHERE ID=' + str(group_id)
        c.execute(sql_string)
        conn.commit()
        conn.close()

    def update_group_is_umbrella(self, group_id, dali_group_is_umbrella):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'UPDATE dali_groups SET dali_group_is_umbrella=' + str(dali_group_is_umbrella) + \
                     ' WHERE ID=' + str(group_id)
        c.execute(sql_string)
        conn.commit()
        conn.close()
        return (dali_group_is_umbrella)

    def update_group_name(self, group_id, group_name):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'UPDATE dali_groups SET dali_group_name=\'' + group_name + \
                     '\' WHERE ID=' + str(group_id)
        c.execute(sql_string)
        conn.commit()
        conn.close()


    def get_ballasts_from_group(self, channel_number, group_number):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT ID, ballast_short_address, ballast_name FROM ballasts WHERE ballast_channel=' + \
                     channel_number + ' AND ballast_group_' + group_number + "=1 ORDER BY ballast_short_address ASC"
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def get_ballasts_from_groupID(self, group_ID):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = "SELECT dali_group_number, dali_group_channel FROM dali_groups WHERE ID=" + str(group_ID)
        c.execute(sql_string)
        data = c.fetchall()
        data = data[0]
        dali_group_number = data["dali_group_number"]
        dali_group_channel = data["dali_group_channel"]
        sql_string = 'SELECT ID, ballast_short_address, ballast_name FROM ballasts WHERE ballast_channel=' + \
                     str(dali_group_channel) + ' AND ballast_group_' + str(dali_group_number) + "=1 ORDER BY ballast_short_address ASC"
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def get_ballasts_outside_group(self, channel_number, group_number):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT ID, ballast_short_address, ballast_name FROM ballasts WHERE ballast_channel=' + \
                     channel_number + ' AND ballast_group_' + group_number + "=0"
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def get_ballast_is_in_group(self, ballast_id, group_number):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'SELECT ballast_group_' + str(group_number) + ' FROM ballasts WHERE ID=' + str(ballast_id)
        c.execute(sql_string)
        data = c.fetchone()
        data = data[0]
        conn.close()
        return data

    def set_dali_groups_0_7(self, ballast_id, byte_data):
        byte_string = bin(256 + byte_data)
        byte_string = byte_string[-8:]
        for index in range(0, 8):
            is_in_group = byte_string[index]
            if is_in_group == '1':
                self.add_ballast_to_group(ballast_id, 7 - index)
            else:
                self.remove_ballast_from_group(ballast_id, 7 - index)

    def set_dali_groups_8_15(self, ballast_id, byte_data):
        byte_string = bin(256 + byte_data)
        byte_string = byte_string[-8:]
        for index in range(0, 8):
            is_in_group = byte_string[index]
            if is_in_group == '1':
                self.add_ballast_to_group(ballast_id, 15 - index)
            else:
                self.remove_ballast_from_group(ballast_id, 15 - index)

    def set_dali_groups_7_15(self, ballast_id, byte_data):
        byte_string = bin(256 + byte_data)
        byte_string = byte_string[-8:]
        for index in range(8, 17):
            is_in_group = byte_string[index]
            if is_in_group:
                self.add_ballast_to_group(ballast_id, index)
            else:
                self.remove_ballast_from_group(ballast_id, index)

    def add_ballast_to_group(self, ballast_id, group_number):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'UPDATE ballasts SET ballast_group_' + str(group_number) + \
                     '=1 WHERE ID=' + str(ballast_id)
        c.execute(sql_string)
        conn.commit()
        conn.close()
        return 'http200'
        return answer

    def remove_ballast_from_group(self, ballast_id, group_number):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'UPDATE ballasts SET ballast_group_' + str(group_number) + \
                     '=0 WHERE ID=' + str(ballast_id)
        c.execute(sql_string)
        conn.commit()
        conn.close()
        return 'http200'

    def get_group_is_umbrella(self, group_id):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'SELECT dali_group_is_umbrella FROM dali_groups WHERE ID = ' + str(group_id)
        c.execute(sql_string)
        data = c.fetchone()
        conn.close()
        return data['dali_group_is_umbrella']

    def get_scenes_from_group(self, group_id):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string_select = 'SELECT * FROM scenes WHERE scene_group_id = ' + str(group_id)
        c.execute(sql_string_select)
        data = c.fetchall()

        if len(data) == 0:
            scene_offset = 0

            if group_id > -1:
                scene_offset = 10
                if self.get_group_is_umbrella(group_id):
                    scene_offset = 4

            for index in range(0, 6):
                sql_string = "INSERT INTO scenes (scene_group_id, scene_number, scene_sort_order) VALUES ($groupID, $sceneNr, $sceneOrder)"
                sql_string = sql_string.replace('$groupID', str(group_id))
                sql_string = sql_string.replace('$sceneNr', str(index + scene_offset))
                sql_string = sql_string.replace('$sceneOrder', str(index))
                c.execute(sql_string)
                conn.commit()

            c.execute(sql_string_select)
            data = c.fetchall()
        conn.close()
        return data

    def get_scene_values_for_group(self, group_id, scene_number):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT dali_group_number FROM dali_groups WHERE ID=' + str(group_id)
        c.execute(sql_string)
        data = c.fetchone()
        dali_group_number = data['dali_group_number']
        sql_string = 'SELECT ID, ballast_name, ballast_short_address, $SceneValue as scene_value FROM ballasts WHERE $ballastGroup = 1 ORDER BY ballast_short_address'
        sql_string = sql_string.replace('$SceneValue', 'ballast_scene' + str(scene_number) + '_value')
        sql_string = sql_string.replace('$ballastGroup', 'ballast_group_' + str(dali_group_number))
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def get_pages(self):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM pages ORDER BY page_sort_order ASC'
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def update_scene_name(self, scene_id, scene_name):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string2 = 'UPDATE scenes SET scene_name=\'' + scene_name + \
                      '\' WHERE ID=' + str(scene_id)
        c.execute(sql_string2)
        conn.commit()
        conn.close()
        return 'http200'

    def update_scene_value(self, ballast_id, scene_number, scene_value):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'UPDATE ballasts SET $daliscenelevel=' + str(scene_value) + \
                     ' WHERE ID=' + str(ballast_id)
        sql_string = sql_string.replace('$daliscenelevel', 'ballast_scene' + str(scene_number) + '_value')
        c.execute(sql_string)
        conn.commit()
        conn.close()
        return 'http200'

    def insert_visual(self, visual_name, visual_page_ID, visual_type, visual_columns, visual_ID_of_type):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'SELECT visual_sort_order FROM visual WHERE visual_page_ID= ' + str(
            visual_page_ID) + ' ORDER BY visual_sort_order DESC LIMIT 1'
        c.execute(sql_string)
        data = c.fetchone()
        if data is None:
            sort_order = 0
        else:
            sort_order = data[0]

        sql_string = 'INSERT INTO visual (visual_name, visual_page_ID, visual_type, visual_columns, ' + \
                     ' visual_ID_of_type, visual_sort_order) VALUES ("' + \
                     visual_name + '", ' + \
                     str(visual_page_ID) + ", " + \
                     str(visual_type) + ", " + \
                     str(visual_columns) + ", " + \
                     str(visual_ID_of_type) + ", " + \
                     str(sort_order + 1) + ")"
        c.execute(sql_string)
        conn.commit()
        return 'http200'

    def get_visual(self, visual_page_ID):
        sql_string = 'SELECT * FROM visual WHERE visual_page_ID =' + str(visual_page_ID) + " ORDER BY visual_sort_order"
        return self.get_sql_data(sql_string)

    def get_visual_item(self, visualID):
        sql_string = 'SELECT * FROM visual WHERE ID =' + str(visualID)
        data = self.get_sql_data(sql_string)
        return data[0]

    def get_sql_data(self, sql_string):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute(sql_string)
        return c.fetchall()

    def move_visual_down(self, visual_id):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'SELECT visual_sort_order FROM visual WHERE ID=' + str(visual_id)
        c.execute(sql_string)
        data = c.fetchone()
        sort_order_1 = data[0]
        sql_string_2 = 'SELECT visual_sort_order, ID FROM visual WHERE visual_sort_order>' + str(sort_order_1) + \
                       ' ORDER BY visual_sort_order ASC LIMIT 1'
        data = self.get_sql_data(sql_string_2)
        if data:
            data = data[0]
            sort_order_2 = data["visual_sort_order"]
            other_id = data["ID"]
            execute_string = "UPDATE visual SET visual_sort_order =" + str(sort_order_1) + " WHERE ID=" + str(other_id)
            self.execute(execute_string)
            execute_string = "UPDATE visual SET visual_sort_order =" + str(sort_order_2) + " WHERE ID=" + str(visual_id)
            self.execute(execute_string)
        conn.close()
        return 'http200'

    def move_visual_up(self, visual_id):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = 'SELECT visual_sort_order, visual_page_ID FROM visual WHERE ID=' + str(visual_id)
        c.execute(sql_string)
        data = c.fetchone()
        sort_order_1 = data[0]
        visual_page_ID = data[1]
        sql_string_2 = 'SELECT visual_sort_order, ID FROM visual WHERE visual_sort_order<' + str(sort_order_1) + \
                       ' AND visual_page_ID=' + str(visual_page_ID) + \
                       ' ORDER BY visual_sort_order DESC LIMIT 1'
        data = self.get_sql_data(sql_string_2)
        if data:
            data = data[0]
            sort_order_2 = data["visual_sort_order"]
            other_id = data["ID"]
            execute_string = "UPDATE visual SET visual_sort_order =" + str(sort_order_1) + " WHERE ID=" \
                             + str(other_id)
            self.execute(execute_string)
            execute_string = "UPDATE visual SET visual_sort_order =" + str(sort_order_2) + " WHERE ID=" \
                             + str(visual_id)
            self.execute(execute_string)
        conn.close()
        return 'http200'


    def create_db(self):
        table_name = 'ballasts'
        self.create_table(table_name)

        columns = ["ballast_channel INTEGER",
                   "ballast_name TEXT DEFAULT ''",
                   "ballast_short_address INTEGER",
                   "ballast_channel INTEGER DEFAULT 0",
                   "ballast_group_0 INTEGER DEFAULT 0",
                   "ballast_group_1 INTEGER DEFAULT 0",
                   "ballast_group_2 INTEGER DEFAULT 0",
                   "ballast_group_3 INTEGER DEFAULT 0",
                   "ballast_group_4 INTEGER DEFAULT 0",
                   "ballast_group_5 INTEGER DEFAULT 0",
                   "ballast_group_6 INTEGER DEFAULT 0",
                   "ballast_group_7 INTEGER DEFAULT 0",
                   "ballast_group_8 INTEGER DEFAULT 0",
                   "ballast_group_9 INTEGER DEFAULT 0",
                   "ballast_group_10 INTEGER DEFAULT 0",
                   "ballast_group_11 INTEGER DEFAULT 0",
                   "ballast_group_12 INTEGER DEFAULT 0",
                   "ballast_group_13 INTEGER DEFAULT 0",
                   "ballast_group_14 INTEGER DEFAULT 0",
                   "ballast_group_15 INTEGER DEFAULT 0",
                   "ballast_scene0_value INTEGER DEFAULT 255",
                   "ballast_scene1_value INTEGER DEFAULT 255",
                   "ballast_scene2_value INTEGER DEFAULT 255",
                   "ballast_scene3_value INTEGER DEFAULT 255",
                   "ballast_scene4_value INTEGER DEFAULT 255",
                   "ballast_scene5_value INTEGER DEFAULT 255",
                   "ballast_scene6_value INTEGER DEFAULT 255",
                   "ballast_scene7_value INTEGER DEFAULT 255",
                   "ballast_scene8_value INTEGER DEFAULT 255",
                   "ballast_scene9_value INTEGER DEFAULT 255",
                   "ballast_scene10_value INTEGER DEFAULT 255",
                   "ballast_scene11_value INTEGER DEFAULT 255",
                   "ballast_scene12_value INTEGER DEFAULT 255",
                   "ballast_scene13_value INTEGER DEFAULT 255",
                   "ballast_scene14_value INTEGER DEFAULT 255",
                   "ballast_scene15_value INTEGER DEFAULT 255"]

        self.insert_columns(table_name, columns)

        table_name = 'sites'

        self.create_table(table_name)
        columns = ["site_nr_of_chans INTEGER",
                   "site_occupied INTEGER"]

        self.insert_columns(table_name, columns)

        # ********************************************************
        table_name = 'dali_groups'

        self.create_table(table_name)
        columns = ["dali_group_name TEXT DEFAULT ''",
                   "dali_group_number INTEGER",
                   "dali_group_channel INTEGER",
                   "dali_group_visible INTEGER DEFAULT 1",
                   "dali_group_order INTEGER DEFAULT 1",
                   "dali_group_is_umbrella INTEGER DEFAULT 0"]

        self.insert_columns(table_name, columns)

        # ********************************************************

        table_name = 'scenes'

        self.create_table(table_name)
        columns = ["scene_group_id number INTEGER",
                   "scene_name TEXT DEFAULT ''",
                   "scene_number INTEGER",
                   "scene_value INTEGER DEFAULT 255",
                   "scene_sort_order INTEGER"]

        self.insert_columns(table_name, columns)

        # ********************************************************

        table_name = 'visual'

        self.create_table(table_name)
        columns = ["visual_name TEXT DEFAULT ''",
                   "visual_sort_order INTEGER DEFAULT 0",
                   "visual_type INTEGER",
                   "visual_ID_of_type INTEGER DEFAULT 0",
                   "visual_page_ID INTEGER DEFAULT 0",
                   "visual_columns INTEGER DEFAULT 1"]

        self.insert_columns(table_name, columns)

        # ********************************************************

        table_name = 'pages'

        self.create_table(table_name)
        columns = ["page_name TEXT DEFAULT ''",
                   "page_control_type INTEGER DEFAULT 0",
                   "page_font_size INTEGER DEFAULT 15",
                   "page_button_height INTEGER DEFAULT 30",
                   "page_sort_order INTEGER DEFAULT 0"]

        self.insert_columns(table_name, columns)

        # ********************************************************

        table_name = 'virtual_group'

        self.create_table(table_name)
        columns = ["name TEXT DEFAULT ''"]
        self.insert_columns(table_name, columns)

        # ********************************************************

        table_name = 'virtual_group_items'

        self.create_table(table_name)
        columns = ["ballast_id INTEGER DEFAULT ''",
                   "virtual_group_ID INTEGER"]
        self.insert_columns(table_name, columns)
        # ********************************************************

        table_name = 'dali_action'

        self.create_table(table_name)
        columns = ["dali_action_is_ballast INTEGER",
                   "dali_action_is_group INTEGER",
                   "dali_action_is_broadcast INTEGER",
                   "dali_action_is_command INTEGER DEFAULT 1",
                   "dali_action_command INTEGER DEFAULT 1",
                   "dali_action_arc_level INTEGER DEFAULT 1"]

        self.insert_columns(table_name, columns)

        # ********************************************************

        table_name = 'dali_event'

        self.create_table(table_name)
        columns = ["dali_event_name INTEGER",
                   "dali_event_is_fixed_time INTEGER",
                   "dali_event_is_change INTEGER",
                   "dali_event_hour INTEGER",
                   "dali_event_minute INTEGER",
                   "dali_event_on_sun_rise INTEGER",
                   "dali_event_on_sun_set INTEGER",
                   "dali_event_on_leaving INTEGER",
                   "dali_event_on_entering INTEGER",
                   "dali_event_on_waking INTEGER",
                   "dali_event_on_left INTEGER",
                   "dali_event_on_sleep INTEGER",
                   "dali_event_valid_on_monday INTEGER",
                   "dali_event_valid_on_tuesday INTEGER",
                   "dali_event_valid_on_wednesday INTEGER",
                   "dali_event_valid_on_thursday INTEGER",
                   "dali_event_valid_on_friday INTEGER",
                   "dali_event_valid_on_saturday INTEGER",
                   "dali_event_valid_on_sunday INTEGER",
                   "dali_event_valid_on_occupied INTEGER",
                   "dali_event_valid_on_empty INTEGER",
                   "dali_event_valid_on_sleep INTEGER",
                   "dali_event_valid_on_leaving INTEGER",
                   "dali_event_valid_on_going_to_sleep INTEGER",
                   "dali_event_valid_on_light INTEGER",
                   "dali_event_valid_on_dark INTEGER"]

        self.insert_columns(table_name, columns)

        # ********************************************************

        table_name = 'dalichannels'
        self.create_table(table_name)
        columns = ["channel_nr INTEGER",
                   "channel_name TEXT DEFAULT ''",
                   "channel_com_port TEXT DEFAULT ''"]

        self.insert_columns(table_name, columns)

        data = self.select('SELECT * FROM sites')
        if len(data) == 0:
            self.execute('INSERT INTO sites (site_nr_of_chans, site_occupied) VALUES (1,1);')

        self.insert_ballasts()