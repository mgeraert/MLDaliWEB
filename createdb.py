
from classes.database import Database

db = Database()

table_name = 'ballasts'
db.create_table(table_name)

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

db.insert_columns(table_name, columns)

table_name = 'sites'

db.create_table(table_name)
columns = ["site_nr_of_chans INTEGER",
                "site_occupied INTEGER"]

db.insert_columns( table_name, columns)

# ********************************************************
table_name = 'dali_groups'

db.create_table(table_name)
columns = ["dali_group_name TEXT DEFAULT ''",
            "dali_group_number INTEGER",
            "dali_group_channel INTEGER",
            "dali_group_visible INTEGER DEFAULT 1",
            "dali_group_order INTEGER DEFAULT 1",
            "dali_group_is_umbrella INTEGER DEFAULT 0"]

db.insert_columns( table_name, columns)

# ********************************************************

table_name = 'scenes'

db.create_table(table_name)
columns = ["scene_group_id number INTEGER",
            "scene_name TEXT DEFAULT ''",
            "scene_number INTEGER",
            "scene_value INTEGER DEFAULT 255",
            "scene_sort_order INTEGER"]

db.insert_columns( table_name, columns)

# ********************************************************

table_name = 'visual'

db.create_table(table_name)
columns = ["visual_name TEXT DEFAULT ''",
            "visual_sort_order INTEGER DEFAULT 0",
            "visual_type INTEGER",
            "visual_ID_of_type INTEGER DEFAULT 0",
            "visual_page_ID INTEGER DEFAULT 0",
            "visual_columns INTEGER DEFAULT 1"]

db.insert_columns( table_name, columns)

# ********************************************************

table_name = 'pages'

db.create_table(table_name)
columns = ["page_name TEXT DEFAULT ''",
            "page_sort_order INTEGER DEFAULT 0"]

db.insert_columns( table_name, columns)

# ********************************************************


table_name = 'dalichannels'
db.create_table(table_name)
columns = ["channel_nr INTEGER",
            "channel_name TEXT DEFAULT ''",
                "channel_com_port TEXT DEFAULT ''"]

db.insert_columns( table_name, columns)

data = db.select('SELECT * FROM sites')
if len(data) == 0:
    db.execute('INSERT INTO sites (site_nr_of_chans, site_occupied) VALUES (1,1);')

db.insert_ballasts()