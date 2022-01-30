import serial
import time
from enum import Enum
from classes.Database import Database

class AddressModes(Enum):
    broadcast = 1
    group = 2
    ballast = 3


class DaliChannel(object):
    __db = Database()
    __address_mode = AddressModes.ballast
    __commander_mode = 0
    __direct_arc_enabled = 0
    __ballast_or_group_address = 0
    __dali_channel_nr = 0
    __port_error = 0
    __ser = 0

    def __init__(self, dali_channel_nr):
        self.__dali_channel_nr = dali_channel_nr
        data = self.__db.get_comport(dali_channel_nr)
        self.com_port = data['channel_com_port']
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.port = self.com_port
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.bytesize = serial.EIGHTBITS
        ser.timeout = .3
        try:
            if not(ser.isOpen()):
                ser.open()

        except:
            __port_error = 1

        self.ser = ser

    def get_port_error(self):
        return self.__port_error

    def get_channel_number(self):
        return self.__dali_channel_nr

    def set_ballast_or_group_address(self, ballast_or_group_address):
        self.__ballast_or_group_address = ballast_or_group_address

    def set_address_mode(self, address_mode):
        self.__address_mode = address_mode

    def set_direct_arc_enabled(self, enabled):
        self.__direct_arc_enabled = enabled

    def send_over_dali(self, first_byte, second_byte):
        r_list = [0x01, first_byte, second_byte, 0xC1]
        arr = bytearray(r_list)
        self.ser.write(arr)

    def send_over_dali_double(self, first_byte, second_byte):
        self.send_over_dali(first_byte, second_byte)
        time.sleep(.08)
        self.send_over_dali(first_byte, second_byte)
        time.sleep(.08)

    def set_arc_level(self, arc_level):
        self.__direct_arc_enabled = 1
        r_list = [0x01,  self.get_address(), arc_level, 0xC1]
        arr = bytearray(r_list)
        self.ser.write(arr)
        return 'ok'

    def get_address(self):
        address = 0
        if self.__address_mode == AddressModes.broadcast.value:
            address = 254
        if self.__address_mode.value == AddressModes.group.value:
            address = 128 + self.__ballast_or_group_address * 2
        if self.__address_mode.value == AddressModes.ballast.value:
            address = self.__ballast_or_group_address * 2
        if not self.__direct_arc_enabled:
            address = address + 1
        return address

    def dali_off(self):
        self.__direct_arc_enabled = 0
        self.send_over_dali(self.get_address(), 0)

    def dali_up(self):
        self.__direct_arc_enabled = 0
        self.send_over_dali(self.get_address(), 1)

    def dali_down(self):
        self.__direct_arc_enabled = 0
        self.send_over_dali(self.get_address(), 2)

    def dali_step_up(self):
        self.__direct_arc_enabled = 0
        self.send_over_dali(self.get_address(), 3)

    def dali_step_down(self):
        self.__direct_arc_enabled = 0
        self.send_over_dali(self.get_address(), 4)

    def dali_recall_max_level(self):
        self.__direct_arc_enabled = 0
        self.send_over_dali(self.get_address(), 5)

    def dali_recall_min_level(self):
        self.__direct_arc_enabled = 0
        self.send_over_dali(self.get_address(), 6)

    def dali_step_down_and_off(self):
        self.__direct_arc_enabled = 0
        self.send_over_dali(self.get_address(), 7)

    def dali_on_and_step_up(self):
        self.__direct_arc_enabled = 0
        self.send_over_dali(self.get_address(), 8)


    def dali_set_fade_time(self, fade_time):
        self.__direct_arc_enabled = 0
        self.dali_set_dtr(fade_time)
        self.send_over_dali_double(self.get_address(), 46)

    def dali_set_fade_rate(self, fade_rate):
        self.__direct_arc_enabled = 0
        self.dali_set_dtr(fade_rate)
        self.send_over_dali_double(self.get_address(), 47)

    def dali_goto_scene(self, scene_number):
        self.__direct_arc_enabled = 0

        if scene_number < 0:
            scene_number = 0

        if scene_number > 15:
            scene_number = 15

        self.send_over_dali(self.get_address(), scene_number + 16)

    def scene_number(self, scene_number):
        self.__direct_arc_enabled = 0

        if scene_number < 0:
            scene_number = 0

        if scene_number > 15:
            scene_number = 15

        self.send_over_dali(self.get_address(), scene_number + 16)

    def query(self, query_nr):
        self.ser.flush()
        self.__direct_arc_enabled = 0
        self.__address_mode = AddressModes.ballast
        r_list = [0x01,  self.get_address(), query_nr, 0xC1]
        arr = bytearray(r_list)
        self.ser.write(arr)
        answer = self.ser.readline()
        value = answer[-1]
        return value

    def dali_query_actual_level(self):
        return self.query(160)

    def dali_query_max_level(self):
        return self.query(161)

    def dali_query_min_level(self):
        return self.query(162)

    def dali_query_power_on_level(self):
        return self.query(163)

    def dali_query_scene_level(self, scene_number):
        if scene_number < 0:
            scene_number = 0
        if scene_number > 15:
            scene_number = 15
        return self.query(176+scene_number)

    def dali_query_group_0_to_7(self):
        return self.query(192)

    def dali_query_group_8_to_15(self):
        return self.query(193)

    def dali_set_dtr(self, dtr_value):
        self.__direct_arc_enabled = 0
        self.send_over_dali_double(163, dtr_value)

    def dali_store_dtr_as_scene(self, scene_number):
        self.__direct_arc_enabled = 0
        self.send_over_dali_double(self.get_address(), scene_number + 64)

    def dali_set_scene_value(self, scene_number, scene_value):
        self.dali_set_dtr(scene_value)
        self.dali_store_dtr_as_scene(scene_number)

    def download_groups_from_ballast(self, ballast_id):
        db = Database()
        ballast_data = db.get_ballast_id_and_channel(ballast_id)
        self.__address_mode = AddressModes.ballast
        self.__ballast_or_group_address = ballast_data['ballast_short_address']
        group0_7 = self.dali_query_group_0_to_7()
        group8_15 = self.dali_query_group_8_to_15()
        db.set_dali_groups_0_7(ballast_id, group0_7)
        db.set_dali_groups_8_15(ballast_id, group8_15)
        byte_string0_7 = bin(256 + group0_7)
        byte_string0_7 = byte_string0_7[-8:]
        byte_string8_15 = bin(256 + group8_15)
        byte_string8_15 = byte_string8_15[-8:]
        return 'Ballast: ' + str(self.__ballast_or_group_address) \
               + '; groups 0-7: ' \
               + byte_string0_7 \
               + '; groups 8-15: ' \
               + byte_string8_15

    def download_scene_from_ballast(self, ballast_short_address, ballast_id, scene_number):
        self.__address_mode = AddressModes.ballast
        self.__ballast_or_group_address = ballast_short_address
        scene_value = self.dali_query_scene_level(scene_number)
        db = Database()
        db.update_scene_value(ballast_id, scene_number, scene_value)
        return 'Ballast ' + str(self.__ballast_or_group_address) \
               + ' - scene ' \
               + str(scene_number) \
               + ' level: '\
               + str(scene_value)


    def DaliAddToGroup(self, ballast_short_address, group_address):
        self.__address_mode = AddressModes.ballast
        self.__ballast_or_group_address = ballast_short_address
        self.send_over_dali_double(self.get_address(), 96 + group_address)

    def DaliRemoveFromGroup(self, ballast_short_address, group_address):
        self.__address_mode = AddressModes.ballast
        self.__ballast_or_group_address = ballast_short_address
        self.send_over_dali_double(self.get_address(), 112 + group_address)


    def UploadGroupsToDevice(self, ballast_sa):
        db = Database()
        ballast_data = db.get_ballast_by_short_address(ballast_sa)
        self.__address_mode = AddressModes.ballast
        sa = ballast_data['ballast_short_address']
        self.__ballast_or_group_address = sa

        for i in range(16):
            if ballast_data['ballast_group_' + str(i)]:
                self.DaliAddToGroup(sa, i)
            else:
                self.DaliRemoveFromGroup(sa, i)

        return 'Ballast ' + str(sa) + ': groups uploaded'


    def do_command(self, command):
        self.__direct_arc_enabled = 0
        command = command.lower()
        if command == 'on':
            self.dali_recall_max_level()
        if command == 'off':
            self.dali_off()
        if command == 'up':
            self.dali_up()
        if command == 'down':
            self.dali_down()
