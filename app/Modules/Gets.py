from ncclient import manager
from netmiko import ConnectHandler, ssh_exception
import xmltodict
import ipaddress


interface_types = ("GigabitEthernet", "Loopback", "Tunnel", "Vlan", "Port-channel", "TenGigabitEthernet",
                   "Port-channel-subinterface")

trunk_types = ("GigabitEthernet", "TenGigabitEthernet")

def is_instance(list_or_dict):
    """"""

    if isinstance(list_or_dict, list):
        make_list = list_or_dict
    else:
        make_list = [list_or_dict]

    return make_list


def is_in_list(list_or_dict):
    """y"""

    if isinstance(list_or_dict, list):
        make_list = list_or_dict
    else:
        make_list = [list_or_dict]

    return make_list


def get_prefix_config(session):

    config = None
    xml_filter = """<filter xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <ip>
                    <prefix-list/>
                    </ip>
                    </native>
                    </filter>"""

    try:
        get_prefix = session.get(xml_filter)
        parsed = xmltodict.parse(get_prefix.xml)["rpc-reply"]["data"]
        prefixes = parsed.get("native").get("ip").get("prefix-list").get("prefixes")
        config = is_instance(prefixes)
    except manager.operations.errors.TimeoutExpiredError as error:
        converted_config = 'error'
    except AttributeError as error:
        converted_config = 'error'
    except manager.transport.TransportError as error:
        converted_config = 'error'
    except manager.operations.rpc.RPCError as error:
        converted_config = 'error'

    return config


def get_config(session):
    """Gets interfaces configurations"""

    try:
        xml_filter = """<filter xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                        <interface/>
                        </native>
                        </filter>"""

        intf_info = session.get(xml_filter)
        intf_dict = xmltodict.parse(intf_info.xml)["rpc-reply"]["data"]
        converted_config = is_instance(intf_dict)

    except manager.operations.errors.TimeoutExpiredError as error:
        converted_config = 'error'
    except AttributeError as error:
        converted_config = 'error'
    except manager.transport.TransportError as error:
        converted_config = 'error'
    except manager.operations.rpc.RPCError as error:
        converted_config = 'error'

    return converted_config


def get_stats(session, interface=None):

    interface_state = None

    if interface is not None:

        xml_filter = f"""<filter>
                        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                        <name>{interface}</name>
                        </interface>
                        </interfaces-state>
                        </filter>"""
    else:

        xml_filter = f"""<filter>
                        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                        </interface>
                        </interfaces-state>
                        </filter>"""

    try:
        get_state = session.get(xml_filter)
        int_status = xmltodict.parse(get_state.xml)["rpc-reply"]["data"]
        interface_state = int_status["interfaces-state"]["interface"]
    except manager.operations.errors.TimeoutExpiredError as error:
        print(error)
    except AttributeError as error:
        print(error)
    except manager.transport.TransportError as error:
        print(error)
    except manager.operations.rpc.RPCError as error:
        print(error)

    return interface_state


def get_interface_stats(session, select_int, ip=None):
    """Called from get_interfaces method and returns interface state information. (up/down, speed, change, mac, etc).
    Returns information to the caller"""

    interface_stats = {}

    interface = get_stats(session, select_int)

    speed_conversion = int(int(interface.get("speed")) / 1e+6)
    interface_stats[select_int] = {'ip': ip, "admin": interface.get("admin-status"),
                                   "operational": interface.get("oper-status"),
                                   "speed": speed_conversion,
                                   "last_change": interface.get("last-change"),
                                   "MAC": interface.get("phys-address"),
                                   "in_octets": interface.get("statistics")["in-octets"],
                                   "In Unicast": interface.get("statistics")["in-unicast-pkts"],
                                   "In Multicast": interface.get("statistics")[
                                       "in-multicast-pkts"],
                                   "In Discards": interface.get("statistics")["in-discards"],
                                   "In Errors": interface.get("statistics")["in-errors"],
                                   "Protocol Drops": interface.get("statistics")[
                                       "in-unknown-protos"],
                                   "out_octets": interface.get("statistics")["out-octets"],
                                   "Out Unicast": interface.get("statistics")[
                                       "in-unicast-pkts"],
                                   "Out Multicast": interface.get("statistics")[
                                       "in-multicast-pkts"],
                                   "Out Discards": interface.get("statistics")["in-discards"],
                                   "Out Errors": interface.get("statistics")["in-errors"],
                                   "Out Boradcast": interface.get("statistics")[
                                       "out-broadcast-pkts"]}

    return interface_stats


def get_ip_interfaces(session, config, device):
    """Gets interface ips addresses"""

    interface_info = []
    unassigned_interfaces = ['Tunnel', 'Loopback', 'Vlan']
    interface_num = []

    try:
        for ints in interface_types:
            for ip in is_in_list(config[0]["native"]["interface"].get(ints)):
                if ip is None:
                    continue
                elif ip.get("ip", {}).get("address", {}):
                    address = ipaddress.ip_interface(
                        ip.get('ip', '').get('address').get('primary').get('address') + '/' + ip.get('ip', '').get(
                            'address').get('primary').get('mask'))
                    parsed_info = get_interface_stats(session, ints + ip.get('name'), ip=address)
                    interface_info.append(parsed_info)
                else:
                    try:
                        parsed_info = get_interface_stats(session, ints + ip.get('name'), ip='Not Assigned')
                        interface_info.append(parsed_info)
                    except TypeError:
                        pass

                    try:
                        unassigned_interfaces.append(ints + ip.get('name'))
                        interface_num.append(ip.get('name'))
                    except TypeError:
                        pass

    except TypeError:
        pass

    return interface_info

def indivisual_poll(host, username, password, netconf_port):
    """Poll indivisual configurations via table poll buttons"""

    # Creates the netconf connection.
    try:
        with manager.connect(host=host, port=netconf_port, username=username, password=password, device_params={'name': 'csr'}) as session:
            config = get_config(session)
            interfaces = get_ip_interfaces(session, config, host)

            return interfaces

    except manager.operations.errors.TimeoutExpiredError:
        pass
    except AttributeError:
        pass
    except manager.transport.TransportError:
        pass
    except manager.operations.rpc.RPCError:
        pass
    except OSError:
        pass


def more_int_details(host, username, password, ssh_port, interface):

    credentials = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'port': ssh_port,
        'session_log': 'my_file.out'}

    try:
        with ConnectHandler(**credentials) as session:
            interface_details = session.send_command(f'show interface {interface}')
            return interface_details
    except OSError:
        pass

    return get_more_details
