
from classes.DaliChannels import DaliChannels
from classes.DaliChannel import AddressModes
import _thread
import time
from threading import Timer

global barrel_counter

class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue:  # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False  # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")




dcs = DaliChannels()
channel = dcs.get_chan(1)

channel.set_direct_arc_enabled(0)
channel.set_address_mode(AddressModes.ballast)
channel.set_ballast_or_group_address(28)
channel.dali_set_fade_time(2)
channel.dali_set_fade_rate(2)

fade_time_color = 7
channel.set_ballast_or_group_address(32)
channel.dali_set_fade_time(fade_time_color)
channel.dali_set_fade_rate(fade_time_color)
channel.set_ballast_or_group_address(33)
channel.dali_set_fade_time(fade_time_color)
channel.dali_set_fade_rate(fade_time_color)
channel.set_ballast_or_group_address(34)
channel.dali_set_fade_time(fade_time_color)
channel.dali_set_fade_rate(fade_time_color)
channel.set_ballast_or_group_address(36)
channel.dali_set_fade_time(fade_time_color)
channel.dali_set_fade_rate(fade_time_color)
channel.set_ballast_or_group_address(37)
channel.dali_set_fade_time(fade_time_color)
channel.dali_set_fade_rate(fade_time_color)
channel.set_ballast_or_group_address(38)
channel.dali_set_fade_time(fade_time_color)
channel.dali_set_fade_rate(fade_time_color)


barrel_counter = 1
toggle = 1
ColorCounter = 1

loop_morgan = [41, 43, 42, 22]
loop_onder = [31, 18 ,19, 25 ,21, 23, 20, 22]

def doLoop(threadName, loop_list, direct_arc, time_span, loops):
    for x in range(loops):
        for sa in loop_list:
            swithOnOff(sa, direct_arc,  time_span)
    do_switch_off(loop_list)

def doToggle(threadName):
    global toggle
    if toggle:
        do_arc(28, 30)
    else:
        do_arc(28, 120)
    if toggle == 1:
        toggle = 0
    else:
        toggle = 1

def do_switch_off(loop_list):
    for sa in loop_list:
        channel.set_direct_arc_enabled(1)
        channel.set_address_mode(AddressModes.ballast)
        channel.set_ballast_or_group_address(sa)
        channel.set_arc_level(1)
        time.sleep(.015)
        channel.set_arc_level(1)
        time.sleep(.015)

def do_toggle_color(threadName):
    global ColorCounter
    if ColorCounter == 1:
        do_arc(33, 230)
        do_arc(32, 1)
        do_arc(34, 1)
        do_arc(37, 1)
        do_arc(36, 1)
        do_arc(38, 230)
    if ColorCounter == 2:
        do_arc(33, 1)
        do_arc(32, 1)
        do_arc(34, 230)
        do_arc(37, 220)
        do_arc(36, 1)
        do_arc(38, 1)
    if ColorCounter == 3:
        do_arc(33, 2320)
        do_arc(32, 120)
        do_arc(34, 1)
        do_arc(37, 250)
        do_arc(36, 1)
        do_arc(38, 230)
    ColorCounter = ColorCounter +1
    if ColorCounter == 4:
        ColorCounter = 1



def tick():
    global barrel_counter
    barrel_counter += 1
    if barrel_counter % 61 == 0:
      _thread.start_new_thread(doLoop, ("thre1", loop_morgan, 210, 0.15, 3,))
    if barrel_counter % 130 == 0:
      _thread.start_new_thread(doLoop, ("thre2", loop_onder, 210, 0.15, 3,))
    if barrel_counter % 4 == 0:
      _thread.start_new_thread(doToggle, ("thre3", ))
    if barrel_counter % 49 == 0:
      _thread.start_new_thread(do_toggle_color, ("thre3", ))

def swithOnOff(short_address, direct_arc, time_span):
    channel.set_direct_arc_enabled(1)
    channel.set_address_mode(AddressModes.ballast)
    channel.set_ballast_or_group_address(short_address)
    channel.set_arc_level(direct_arc)
    time.sleep(time_span)
    channel.set_arc_level(1)
    time.sleep(.03)

def do_arc(short_address, direct_arc):
    channel.set_direct_arc_enabled(1)
    channel.set_address_mode(AddressModes.ballast)
    channel.set_ballast_or_group_address(short_address)
    channel.set_arc_level(direct_arc)
    time.sleep(.03)