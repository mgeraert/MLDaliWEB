from RouterInfo import RouterInfo
import platform
import os


def lists_all_commands():
    ri = RouterInfo("192.168.1.1", "admin", "jolien01")
    # print("Uptime    : " + str(ri.get_uptime()))
    # print("Uptime    : " + str(ri.get_uptime_secs()))
    # print("Memory    : " + str(ri.get_memory_usage()))
    # print("CPU       : " + str(ri.get_cpu_usage()))
    # print("Data      : " + str(ri.get_traffic_total()))
    # print("Bandwidth : " + str(ri.get_traffic()))
    # print("WAN       : " + str(ri.get_status_wan()))
    # print("Online    : " + str(ri.is_wan_online()))
    # print("Settings  : " + str(ri.get_settings()))
    # print("IP addr   : " + str(ri.get_lan_ip_address()))
    # print("Netmask   : " + str(ri.get_lan_netmask()))
    # print("Gateway   : " + str(ri.get_lan_gateway()))
    # print("Clients   : " + str(ri.get_clients_fullinfo()))
    # print("Clients   : " + str(ri.get_clients_info()))
    # print("Client   : " + str(ri.get_client_info('B8:2C:A0:5F:37:52')))
    # print("DHCP      : " + str(ri.get_dhcp_list()))
    # print("Online    : " + str(ri.get_online_clients()))



def building_is_empty():
    import configparser

    config = configparser.ConfigParser()
    current_os = platform.system().lower()

    if current_os.lower() == "windows":
        db_path = os.getcwd() + os.path.sep + '..' + os.path.sep + 'database' + os.path.sep
    else:
        # config.read('/var/www/webApp/webApp/mlconfig.ini')
        db_path = '/etc/MLDali/'

    config.read(db_path + 'mlconfig.ini')

    login = config['ROUTER']['login']
    pw = config['ROUTER']['pw']
    ri = RouterInfo("192.168.1.1", login, pw)

    attendee_devices = ['6E:B3:65:C4:D1:C7', "8A:3E:66:1A:3F:A5"]

    occupied = 0

    for client in ri.get_clients_info():
        for attendee_device in attendee_devices:
            if client['mac'] == attendee_device:
                occupied = 1

    return occupied
