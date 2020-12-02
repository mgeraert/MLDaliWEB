from flask import Flask, render_template, request
from classes.database import Database
import sys
import glob
import serial.tools.list_ports as port_list
import serial
import json
from classes.DaliChannels import DaliChannels
from classes.DaliChannel import AddressModes

from blue_pages import pages
from blue_visual import visual

app = Flask(__name__)
app.register_blueprint(pages)
app.register_blueprint(visual)
dcs = DaliChannels()


@app.route("/groups")
def beneden():
    return render_template('groups.html')


@app.route("/ballasts")
def ballasts():
    return render_template('ballasts.html')


@app.route("/visuals")
def visuals():
    return render_template('visuals.html')

@app.route("/channels")
def channels():
    return render_template('channels.html')

@app.route("/ballasts_per_group")
def ballasts_per_group():
    return render_template('ballast_per_group.html')


@app.route("/scenes")
def scenes():
    return render_template('scenes.html')


@app.route("/bstest")
def bstest():
    return render_template('bstest.html')


@app.route("/settings")
def settings():
    return render_template('settings.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/control', methods=['GET'])
def contol():
    return render_template('control.html')


@app.route("/navbar")
def navbar():
    return render_template('navbar.html')


@app.route("/basicControl")
def basic_control():
    return render_template('basiccontrol.html')


@app.route("/ballasts_get")
def ballasts_get():
    channel_nr = request.args.get("channel")
    db = Database()
    data = db.get_ballasts(channel_nr)
    return json.dumps(data)

@app.route("/channels_get")
def channels_get():
    db = Database()
    data = db.get_channels()
    return json.dumps(data)

@app.route("/groups_get")
def groups_get():
    channel_nr = request.args.get("channel")
    db = Database()
    data = db.get_groups(channel_nr)
    return json.dumps(data)


@app.route("/get_tree")
def get_tree():
    db = Database()
    data = db.get_tree()
    return json.dumps(data)


@app.route('/address', methods=['POST', 'GET'])
def address():
        return request.args.get('q', '')


@app.route('/UpdateBallast', methods=['POST'])
def update_ballast():
    ballast_name = request.form.get('ballast_name')
    ballast_id = request.form.get('ID')
    ballast_id = ballast_id[3:]
    db = Database()
    db.update_ballast_name(ballast_id, ballast_name)
    return ballast_name


@app.route('/UpdateGroupName', methods=['POST'])
def update_group():
    group_name = request.form.get('group_name')
    group_id = request.form.get('ID')
    db = Database()
    db.update_group_name(group_id, group_name)
    return group_name


@app.route('/UpdateGroupIsUmbrella', methods=['POST'])
def update_group_is_umbrella():
    dali_group_is_umbrella = request.form.get('dali_group_is_umbrella')
    group_id = request.form.get('ID')
    db = Database()
    answer = db.update_group_is_umbrella(int(group_id), int(dali_group_is_umbrella))
    return str(answer)


@app.route('/do_value', methods=['POST'])
def do_value():
    db = Database()
    ballast_id = request.form.get('ID')
    nv = db.get_ballast_id_and_channel(ballast_id)
    ballast_short_address = nv['ballast_short_address']
    channel_number = nv['ballast_channel']
    channel = dcs.get_chan(channel_number)
    channel.set_direct_arc_enabled(1)
    channel.set_address_mode(AddressModes.ballast)
    channel.set_ballast_or_group_address(ballast_short_address)
    value = int(request.form.get('value'))
    channel.set_arc_level(value)
    return 'ok'


@app.route('/serial_ports_get')
def serial_ports_get():
    ports = list(port_list.comports())
    out = ''
    for p in ports:
        out = out + p.description
    return out


@app.route('/AddBallastToGroup', methods=['POST'])
def add_ballast_to_group():
    group_number = request.form.get('group_number')
    ballast_id = request.form.get('ID')
    db = Database()
    answer = db.add_ballast_to_group(ballast_id, group_number)
    return answer

@app.route('/RemoveBallastFromGroup', methods=['POST'])
def remove_ballast_from_group():
    group_number = request.form.get('group_number')
    ids = request.form.get('ID')
    ids = ids[3:]
    db = Database()
    answer = db.remove_ballast_from_group(ids, group_number)
    return answer

@app.route('/GetBallastsFromGroup', methods=['GET'])
def get_ballasts_from_group():
    group_number = request.args.get('group_number')
    channel_number = request.args.get('channel_number')
    db = Database()
    answer = db.get_ballasts_from_group(channel_number, group_number)
    return json.dumps(answer)

@app.route('/GetBallastsFromGroupID', methods=['GET'])
def get_ballasts_from_group_ID():
    group_ID= request.args.get('group_id')
    db = Database()
    answer = db.get_ballasts_from_groupID(group_ID)
    return json.dumps(answer)

@app.route('/doControl', methods=['GET'])
def do_control():
    action = request.args.get('action')
    visual_id = request.args.get('visualID')
    answer = dcs.do_control(action, visual_id)
    return answer

@app.route('/doControlBallast', methods=['GET'])
def do_control_ballast():
    action = request.args.get('action')
    ballast_id = request.args.get('ballast_id')
    answer = dcs.do_control_ballast(action, ballast_id)
    return answer

@app.route("/doSetArcLevel", methods=['GET'])
def do_set_arc_level():
    arc_level = int(request.args.get('arc_level'))
    visual_id = int(request.args.get('visualID'))
    answer = dcs.do_set_arc_level(arc_level, visual_id)
    return answer

@app.route("/doSetArcLevelBallast", methods=['GET'])
def do_set_arc_level_ballast():
    arc_level = int(request.args.get('arc_level'))
    ballast_id = int(request.args.get('ballast_id'))
    answer = dcs.do_set_arc_level_ballast(arc_level, ballast_id)
    return answer

@app.route('/MoveVisualUp', methods=['GET'])
def move_visual_up():
    visual_id = int(request.args.get('visual_id'))
    db = Database()
    answer = db.move_visual_up(visual_id)
    return answer

@app.route('/MoveVisualDown', methods=['GET'])
def move_visual_down():
    visual_id = int(request.args.get('visual_id'))
    db = Database()
    answer = db.move_visual_down(visual_id)
    return answer

@app.route('/getSystemPorts')
def get_system_ports():

    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return json.dumps(result)


@app.route('/GetChannels', methods=['GET'])
def get_channels():
    db = Database()
    answer = db.get_channels()
    return json.dumps(answer)


@app.route('/GetBallastsOutsideGroup', methods=['GET'])
def get_ballasts_outside_group():
    group_number = request.args.get('group_number')
    channel_number = request.args.get('channel_number')
    db = Database()
    answer = db.get_ballasts_outside_group(channel_number, group_number)
    return json.dumps(answer)


@app.route('/GetBallastIDsFromChannel', methods=['GET'])
def get_ballastids_from_channel():
    channel_number = request.args.get('channel_number')
    db = Database()
    answer = db.get_ballast_id_from_channel(channel_number)
    return json.dumps(answer)


@app.route('/downloadGroupsFromBallast', methods=['GET'])
def download_groups_from_ballast():
    ballast_id = request.args.get('ballast_id')
    answer = dcs.download_groups_from_ballast(ballast_id)
    return answer


@app.route('/query', methods=['GET'])
def query():
    ballast_id = int(request.args.get('ballast_id'))
    query_nr = int(request.args.get('query_nr'))
    return str(dcs.query(ballast_id, query_nr))

@app.route('/getScenesFromGroup', methods=['GET'])
def get_scenes_from_group():
    group_id = int(request.args.get('group_id'))
    db = Database()
    data = db.get_scenes_from_group(group_id)
    return json.dumps(data)

@app.route('/getSceneValuesForGroup', methods=['GET'])
def get_scene_values_for_group():
    group_id = int(request.args.get('group_id'))
    scene_number = int(request.args.get('scene_number'))
    channel = dcs.get_chan_via_group_id(group_id)
    channel.dali_goto_scene(scene_number)
    db = Database()
    data = db.get_scene_values_for_group(group_id, scene_number)
    return json.dumps(data)

@app.route('/setPort', methods=['GET'])
def set_port():
    channel_id = int(request.args.get('channel_id'))
    port_name = request.args.get('port_name')
    db = Database()
    data = db.update_com_port(channel_id, port_name)
    return json.dumps(data)

@app.route('/updateSceneName', methods=['GET'])
def update_scene_name():
    scene_id = int(request.args.get('scene_id'))
    scene_name = request.args.get('scene_name')
    db = Database()
    data = db.update_scene_name(scene_id, scene_name)
    return data

@app.route('/updateSceneValue', methods=['GET'])
def update_scene_value():
    ballast_id = int(request.args.get('ballast_id'))
    scene_number = int(request.args.get('scene_number'))
    scene_value = int(request.args.get('scene_value'))
    db = Database()
    data = db.update_scene_value(ballast_id, scene_number, scene_value)
    channel = dcs.get_chan_via_ballast_id(ballast_id)
    channel.dali_set_scene_value(scene_number, scene_value)
    channel.dali_goto_scene(scene_number)
    return data

@app.route('/DownloadSceneFromBallast', methods=['GET'])
def download_scene_from_ballast():
    ballast_id = int(request.args.get('ballast_id'))
    scene_number = int(request.args.get('scene_number'))
    answer = dcs.download_scene_from_ballast(ballast_id, scene_number)
    return answer


@app.route("/SetBallastOrGroupAddress")
def set_ballast_or_group_address():
    ballast_or_group_address = int(request.args.get('ballast_or_group_address'))
    channel_number = int(request.args.get('channel_number'))
    dcs.set_ballast_or_group_address(ballast_or_group_address, channel_number)
    return 'http200'


@app.route("/SetAddressMode")
def set_address_mode():
    address_mode = int(request.args.get('address_mode'))
    channel_number = int(request.args.get('channel_number'))
    dcs.set_address_mode(address_mode, channel_number)
    return 'http200'


@app.route("/SetDirectArcEnabled")
def set_direct_arc_enabled():
    direct_arc_enabled = int(request.args.get('direct_arc_enabled'))
    channel_number = int(request.args.get('channel_number'))
    dcs.set_direct_arc_enabled(direct_arc_enabled, channel_number)
    return 'http200'

@app.route("/SetArcLevel")
def set_arc_level():
    arc_level = int(request.args.get('arc_level'))
    channel_number = int(request.args.get('channel_number'))
    dcs.set_arc_level(arc_level, channel_number)
    return 'http200'


@app.route("/InsertVisual")
def insert_visual():
    visual_name = request.args.get('visual_name')
    visual_page_id = int(request.args.get('visual_page_ID'))
    visual_type = int(request.args.get('visual_type'))
    visual_columns = int(request.args.get('visual_columns'))
    visual_id_of_type = int(request.args.get('visual_ID_of_type'))

    db = Database()
    db.insert_visual(visual_name, visual_page_id, visual_type, visual_columns, visual_id_of_type)
    return 'http200'


@app.route("/getVisual")
def get_visual():
    visual_page_id = int(request.args.get('visual_page_id'))
    db = Database()
    data = db.get_visual(visual_page_id)
    return json.dumps(data)

@app.route("/gotoScene")
def goto_scene():
    visual_id = int(request.args.get('visual_id'))
    scene_number = int(request.args.get('scene_number'))
    dcs.goto_scene(scene_number, visual_id)
    return 'http200'

    return json.dumps(data)

if __name__ == '__main__':
    #app.run(debug=True, use_reloader=False)
    app.run(host="0.0.0.0", port="5000")
