
from classes.Database import Database
from classes.DaliChannel import DaliChannel, AddressModes


class DaliChannels(object):

    __channels = []
    __db = Database()

    def __init__(self):
        channels = self.__db.get_channels()
        for channel in channels:
            dc = DaliChannel(channel.get('channel_nr'))
            self. __channels.append(dc)


    def get_chan(self, channel_number):
        for channel in self.__channels:
            if channel.get_channel_number() == channel_number:
                return channel


    def get_chan_via_ballast_id(self, ballast_id):
        ballast = self.__db.get_ballast(ballast_id)
        channel = self.get_chan(ballast.get('ballast_channel'));
        channel.set_ballast_or_group_address(ballast.get('ballast_short_address'))
        channel.set_address_mode(AddressModes.ballast)
        return channel


    def get_chan_via_group_id(self, group_id):
        group = self.__db.get_group(group_id)
        channel = self.get_chan(group.get('dali_group_channel'));
        channel.set_ballast_or_group_address(group.get('dali_group_number'))
        channel.set_address_mode(AddressModes.group)
        return channel


    def query(self, ballast_id, query_nr):
        ballast = self.__db.get_ballast(ballast_id)
        for channel in self.__channels:
            if channel.get_channel_number() == ballast.get('ballast_channel'):
                return channel.query(query_nr)


    def download_scene_from_ballast(self, ballast_id, scene_number):
        ballast = self.__db.get_ballast(ballast_id)
        channel = self.get_chan_via_ballast_id(ballast_id)
        answer = channel.download_scene_from_ballast(ballast.get('ballast_short_address'), ballast_id, scene_number)
        return answer


    def set_ballast_or_group_address(self, ballast_or_group_address, channel_number):
        channel = self.get_chan(channel_number)
        channel.set_ballast_or_group_address(ballast_or_group_address)


    def set_address_mode(self, address_mode, channel_number):
        channel = self.get_chan(channel_number)
        channel.set_address_mode(address_mode)


    def set_arc_level(self, arc_level, channel_number):
        channel = self.get_chan(channel_number)
        channel.set_arc_level(arc_level)


    def set_address_mode(self, address_mode, channel_number):
        channel = self.get_chan(channel_number)
        channel.set_address_mode(address_mode)


    def set_direct_arc_enabled(self, direct_arc_enabled, channel_number):
        channel = self.get_chan(channel_number)
        channel.set_direct_arc_enabled(direct_arc_enabled)


    def download_groups_from_ballast(self, ballast_id):
        ballast = self.__db.get_ballast(ballast_id)
        dc = DaliChannel(self.__channels[ballast.get('ballast_channel')])
        dc.download_scene_from_ballast(ballast_id)


    def do_control(self, action, visualID):

        db = Database()
        visual_item = db.get_visual_item(visualID)

        var = 100
        if visual_item.get('visual_type') == 0:
            var = 1
        elif visual_item.get('visual_type') == 1:
            var = 1
        elif visual_item.get('visual_type') == 2:
            group = db.get_group(visual_item.get('visual_ID_of_type'))
            channel = self.get_chan(group.get('dali_group_channel'))
            channel.set_ballast_or_group_address(group.get('dali_group_number'))
            channel.set_address_mode(AddressModes.group)
            channel.set_direct_arc_enabled(0)
            channel.do_command(action)
        elif visual_item.get('visual_type') == 3:
            ballast = db.get_ballast(visual_item.get('visual_ID_of_type'))
            channel = self.get_chan(ballast.get('ballast_channel'))
            channel.set_ballast_or_group_address(ballast.get('ballast_short_address'))
            channel.set_address_mode(AddressModes.ballast)
            channel.set_direct_arc_enabled(0)
            channel.do_command(action)
        return 'http200'

    def do_control_ballast(self, action, ballastID):
        db = Database()
        ballast = db.get_ballast(ballastID);
        channel = self.get_chan(ballast.get('ballast_channel'))
        channel.set_ballast_or_group_address(ballast.get('ballast_short_address'))
        channel.set_address_mode(AddressModes.ballast)
        channel.set_direct_arc_enabled(0)
        channel.do_command(action)
        return 'http200'

    def do_set_arc_level(self, arc_level, visualID):
        db = Database()
        visual_item = db.get_visual_item(visualID)

        var = 100
        if visual_item.get('visual_type') == 0:
            var = 1
        elif visual_item.get('visual_type') == 1:
            var = 1
        elif visual_item.get('visual_type') == 2:
            group = db.get_group(visual_item.get('visual_ID_of_type'))
            channel = self.get_chan(group.get('dali_group_channel'))
            channel.set_ballast_or_group_address(group.get('dali_group_number'))
            channel.set_address_mode(AddressModes.group)
            channel.set_direct_arc_enabled(1)
            channel.set_arc_level(arc_level)
        elif visual_item.get('visual_type') == 3:
            ballast = db.get_ballast(visual_item.get('visual_ID_of_type'))
            channel = self.get_chan(ballast.get('ballast_channel'))
            channel.set_ballast_or_group_address(ballast.get('ballast_short_address'))
            channel.set_address_mode(AddressModes.ballast)
            channel.set_direct_arc_enabled(1)
            channel.set_arc_level(arc_level)
        return 'http200'

    def do_set_arc_level_ballast(self, arc_level, ballast_id):
        db = Database()
        ballast = db.get_ballast(ballast_id)
        channel = self.get_chan(ballast.get('ballast_channel'))
        channel.set_ballast_or_group_address(ballast.get('ballast_short_address'))
        channel.set_address_mode(AddressModes.ballast)
        channel.set_direct_arc_enabled(1)
        channel.set_arc_level(arc_level)
        return 'http200'

    def goto_scene(self, scene_number, visualID):
        db = Database()
        visual_item = db.get_visual_item(visualID)

        var = 100
        if visual_item.get('visual_type') == 0:
            var = 1
        elif visual_item.get('visual_type') == 1:
            var = 1
        elif visual_item.get('visual_type') == 2:
            group = db.get_group(visual_item.get('visual_ID_of_type'))
            channel = self.get_chan(group.get('dali_group_channel'))
            channel.set_ballast_or_group_address(group.get('dali_group_number'))
            channel.set_address_mode(AddressModes.group)
            channel.dali_goto_scene(scene_number)
        elif visual_item.get('visual_type') == 3:
            ballast = db.get_ballast(visual_item.get('visual_ID_of_type'))
            channel = self.get_chan(ballast.get('ballast_channel'))
            channel.set_ballast_or_group_address(ballast.get('ballast_short_address'))
            channel.set_address_mode(AddressModes.ballast)
            channel.dali_goto_scene(scene_number)
        return 'http200'
