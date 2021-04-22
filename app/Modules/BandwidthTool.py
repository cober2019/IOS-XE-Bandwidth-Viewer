"""Bandwidth calculator class used to poll and calculate various statistics"""

import app.Modules.ClassMaps as SearchClassMaps
from ncclient import manager
import xmltodict
import time
import multiprocessing
import collections


def is_instance(list_or_dict) -> list:
    """convert anything not a list to list"""

    if isinstance(list_or_dict, list):
        make_list = list_or_dict
    else:
        make_list = [list_or_dict]

    return make_list


def get_qos_policies(sesssion):
    """Gets current prefix-lists from device and converts from xml to dictionary"""

    policy_maps = None
    class_maps = None
    xml_filter = """<filter xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <policy/>
                    </native>
                    </filter>"""

    intf_info = sesssion.get(xml_filter)
    policy_maps = xmltodict.parse(intf_info.xml)["rpc-reply"]["data"]['native']['policy']['policy-map']
    class_maps = is_instance(xmltodict.parse(intf_info.xml)["rpc-reply"]["data"]['native']['policy']['class-map'])

    return policy_maps, class_maps


def get_stats(session, interface):
    """Gets interface statistics for selected interface"""

    interface_state = None
    xml_filter = f"""<filter>
                    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                    <interface>
                    <name>{interface}</name>
                    </interface>
                    </interfaces-state>
                    </filter>"""

    get_state = session.get(xml_filter)
    int_status = xmltodict.parse(get_state.xml)["rpc-reply"]["data"]
    interface_state = int_status["interfaces-state"]["interface"]

    return interface_state


class CalcBandwidth:
    """Bandwidth calculation class"""

    def __init__(self,  host, port, username, password, interface):

        self.host = host
        self.netconf_port = port
        self.username = username
        self.password = password
        self._interface = interface
        self.previous_in_bandwidth = 0
        self.previous_out_bandwidth = 0
        self.previous_in_discards = 0
        self.previous_out_discards = 0
        self.previous_mbps_in = 0
        self.previous_mbps_out = 0


        self.policy_name = None
        self.policies = None
        self.calc_stats = collections.defaultdict(list)
        self.qos_policies = None

    def get_interface_bandwith_out(self):
        """Calculate outbound bandwidth"""

        mbps_out = 0

        try:
            with manager.connect(host=self.host, port=self.netconf_port, username=self.username, password=self.password,
                                 device_params={'name': 'csr'}) as session:

                interface = get_stats(session, interface=self._interface)
                speed_conversion = int(int(interface.get("speed")))
                bytes_out_diff = int(interface.get("statistics").get("out-octets", {})) - int(self.previous_out_bandwidth)
                calc_1 = round(bytes_out_diff * 8 * 100, 4)
                calc_2 = round(13 * int(speed_conversion), 2)
                mbps_out = round(calc_1 / calc_2 / 100, 2) * int(speed_conversion / 1e+6)

        except (manager.operations.errors.TimeoutExpiredError, manager.transport.TransportError, manager.operations.rpc.RPCError):
            pass
        except (AttributeError, OSError, ValueError):
            pass
        finally:
            if mbps_out < 0:
                mbps_out = self.previous_mbps_out

            self.previous_mbps_out = mbps_out
            self.previous_out_bandwidth = interface.get("statistics").get("out-octets", {})

        return mbps_out

    def get_interface_bandwith_in(self):
        """Calculate inbound bandwidth"""

        mbps_in = 0

        try:
            with manager.connect(host=self.host, port=self.netconf_port, username=self.username, password=self.password,
                                 device_params={'name': 'csr'}) as session:

                interface = get_stats(session, interface=self._interface)
                speed_conversion = int(int(interface.get("speed")))
                bytes_in_diff = int(interface.get("statistics").get("in-octets", {})) - int(self.previous_in_bandwidth)
                calc_1 = round(bytes_in_diff * 8 * 100, 4)
                calc_2 = round(13 * int(speed_conversion), 2)
                mbps_in = round(calc_1 / calc_2 / 100, 2) * int(speed_conversion / 1e+6)

        except (manager.operations.errors.TimeoutExpiredError, manager.transport.TransportError,
                manager.operations.rpc.RPCError):
            pass
        except (AttributeError, OSError, ValueError):
            pass
        finally:
            if mbps_in < 0:
                mbps_in = self.previous_mbps_in

            self.previous_mbps_in = mbps_in
            self.previous_in_bandwidth = interface.get("statistics").get("in-octets", {})

        return mbps_in

    def get_interface_bandwith_out_discards(self):
        """Calculate outbound discards"""

        discards = 0

        try:
            with manager.connect(host=self.host, port=self.netconf_port, username=self.username, password=self.password,
                                 device_params={'name': 'csr'}) as session:

                interface = get_stats(session, interface=self._interface)
                speed_conversion = int(int(interface.get("speed")))
                discards = int(interface.get("statistics").get("out-discards", {})) - int(self.previous_out_discards)
                self.previous_out_discards = interface.get("statistics").get("out-discards", {})

        except (manager.operations.errors.TimeoutExpiredError, manager.transport.TransportError, manager.operations.rpc.RPCError):
            pass
        except (AttributeError, OSError, ValueError) as e:
            print(e)
        finally:
            if discards < 0:
                discards = 0

        return discards


    def get_interface_bandwith_in_discards(self):
        """Calculate inbound discards"""

        discards = 0
        try:
            with manager.connect(host=self.host, port=self.netconf_port, username=self.username, password=self.password,
                                 device_params={'name': 'csr'}) as session:

                interface = get_stats(session, interface=self._interface)
                speed_conversion = int(int(interface.get("speed")))
                discards = int(interface.get("statistics").get("in-discards", {})) - int(self.previous_in_discards)
                self.previous_in_discards = interface.get("statistics").get("in-discards", {})

        except (manager.operations.errors.TimeoutExpiredError, manager.transport.TransportError, manager.operations.rpc.RPCError):
            pass
        except (AttributeError, OSError, ValueError):
            pass
        finally:
            if discards < 0:
                discards = 0

        return discards

    def get_interface_queues_out(self):
        """Calculate outbound bandwidth"""

        queues = []
        policy = None
        policies = collections.defaultdict(list)

        try:
            with manager.connect(host=self.host, port=self.netconf_port, username=self.username, password=self.password,
                                 device_params={'name': 'csr'}) as session:

                interface = get_stats(session, interface=self._interface)
                # Get initial interface queue statistics
                for i in is_instance(interface):
                    if i.get("diffserv-target-entry", {}).get("direction", {}):
                        policy = i.get('diffserv-target-entry', {}).get('policy-name', {})
                        queues = collections.defaultdict(list)
                        for index, stat in enumerate(
                            i.get("diffserv-target-entry", {}).get("diffserv-target-classifier-statistics", {})):
                            queue = {'queue_name': stat.get('classifier-entry-name', {}),
                                     'parent_path': stat.get('parent-path', {}),
                                     'rate': int(stat.get("classifier-entry-statistics", {}).get("classified-rate", {})),
                                     'bytes': int(stat.get('classifier-entry-statistics', {}).get('classified-bytes', {})),
                                     'packets': int(stat.get('classifier-entry-statistics', {}).get('classified-pkts', {})),
                                     'out_bytes': int(stat.get('queuing-statistics', {}).get('output-bytes', {})),
                                     'out_packets': int(stat.get('queuing-statistics', {}).get('output-pkts', {})),
                                     'drop_packets': int(stat.get('queuing-statistics', {}).get('drop-pkts', {})),
                                     'drop_bytes': int(stat.get('queuing-statistics', {}).get('drop-bytes', {})),
                                     'wred_drops_pkts': stat.get('queuing-statistics', {}).get('wred-stats', {}).get(
                                         'early-drop-pkts', {}),
                                     'wred_drop_bytes': stat.get('queuing-statistics', {}).get('wred-stats', {}).get(
                                         'early-drop-bytes', {}), 'speed': i.get("speed")}
                            queues['queues'].append(queue)
                            policies[stat.get('parent-path', {})].append(queues)

                self.qos_policies = get_qos_policies(session)
                self.calc_stats = collections.defaultdict(list)
                child_policy = [i.split()[2] for i in dict.fromkeys(policies) if len(i.split()) > 2][0]

                #Check for first poll. If None dont examine policy assign self.policies for next poll
                if self.policies is not None:
                    for i in self.qos_policies[0]:
                        if i.get('name') == child_policy:
                            self._get_policy_structure(i, policies)
                        elif i.get('name') == policy:
                            self._get_policy_structure(i, policies)
                self.policies = policies

        except (manager.operations.errors.TimeoutExpiredError, manager.transport.TransportError, manager.operations.rpc.RPCError):
            print(e)
        except (AttributeError, IndexError, TypeError, OSError) as e:
            print(e)

        return self.calc_stats

    def _get_policy_structure(self, i, policies):
        """Initial policy break down"""

        if isinstance(i.get('class'), list):
            for queue in i.get('class'):
                if isinstance(queue.get('action-list'), list):
                    [self._list_calculations(c, policies, queue=queue) for c in queue.get('action-list')]
                elif isinstance(queue.get('action-list'), dict):
                    self._action_list_dict(queue, policies)
        elif isinstance(i.get('class'), dict):
            if isinstance(i.get('class').get('action-list'), list):
                [self._list_calculations(c, policies, queue=i.get('class')) for c in i.get('class').get('action-list')]
            elif isinstance(i.get('class').get('action-list'), dict):
                self._dict_calculations(i, policies)

    def _list_calculations(self, c, policies, queue=None):
        """Slices lists inside the configurations, check queue actions"""

        key = [i for i in dict.fromkeys(policies)][0]

        if c.get("action-type") == 'bandwidth':
            if 'percent' in c.get('bandwidth'):
                allocation = c.get('bandwidth').get('percent')
                self._list_comp_two(allocation, policies, key, queue)
            elif 'kilo-bits' in c.get('bandwidth'):
                allocation = round(int(c.get('bandwidth').get('kilo-bits')) * 1000 / 1e+6)
                self._list_comp_two(allocation, policies, key, queue)
        elif c.get("action-type") == 'priority':
            if 'percent' in c.get('priority'):
                allocation = c.get('priority').get('percent')
                self._list_comp_two(allocation, policies, key, queue)
            elif 'kilo-bits' in c.get('priority'):
                allocation = round(int(c.get('priority').get('kilo-bits')) * 1000 / 1e+6)
                self._list_comp_two(allocation, policies, key, queue)
        elif c.get("action-type") == 'police':
            allocation = int(c.get('police').get('bit-rate')) / 1e+6
            self._list_comp_two(allocation, policies, key, queue)
        elif c.get("action-type") == 'shape':
            if 'bit-rate' in c.get('shape').get('average'):
                allocation = round(int(c.get('shape').get('average').get('bit-rate')) / 1e+6)
                self._list_comp_two(allocation, policies, key, queue)
            elif 'percent' in c.get('shape').get('average'):
                allocation = c.get('shape').get('average').get('percent')
                self._list_comp_two(allocation, policies, key, queue)

    def _action_list_dict(self, queue, policies):
        """Slices lists of dictionaries inside the configuration, check queue actions"""

        key = [i for i in dict.fromkeys(policies)][0]

        if queue.get('action-list').get("action-type") == 'bandwidth':
            if 'percent' in queue.get('action-list').get('bandwidth'):
                allocation = queue.get('action-list').get('bandwidth').get('percent')
                self._list_comp_two(allocation, policies, key, queue)
            elif 'kilo-bits' in queue.get('action-list').get('bandwidth'):
                allocation = round(int(queue.get('action-list').get('bandwidth').get('kilo-bits')) * 1000 / 1e+6)
                self._list_comp_two(allocation, policies, key, queue)
        elif queue.get('action-list').get("action-type") == 'priority':
            if 'percent' in queue.get('action-list').get('priority'):
                allocation = queue.get('action-list').get('priority').get('percent')
                self._list_comp_two(allocation, policies, key, queue)
            elif 'kilo-bits' in queue.get('action-list').get('priority'):
                allocation = round(int(queue.get('action-list').get('priority').get('kilo-bits')) * 1000 / 1e+6)
                self._list_comp_two(allocation, policies, key, queue)
        elif queue.get('action-list').get("action-type") == 'police':
            allocation = int(queue.get('action-list').get('police').get('bit-rate')) / 1e+6
            self._list_comp_two(allocation, policies, key, queue)
        elif queue.get('action-list').get("action-type") == 'shape':
            if 'bit-rate' in queue.get('action-list').get('shape').get('average'):
                allocation = round(int(queue.get('action-list').get('shape').get('average').get('bit-rate')) / 1e+6)
                self._list_comp_two(allocation, policies, key, queue)
            elif 'percent' in inqueue.get('action-list').get('shape').get('average'):
                allocation = queue.get('action-list').get('shape').get('average').get('percent')
                self._list_comp_two(allocation, policies, key, queue)


    def _dict_calculations(self, i, policies):
        """Slices dictionary configurations, check queue actions"""

        key = [i for i in dict.fromkeys(policies)][0]

        if i.get('class').get('action-list').get("action-type") == 'bandwidth':
            if 'kilo-bits' in i.get('class').get("action-list").get('bandwidth'):
                allocation = round(int(i.get('class').get("action-list").get('bandwidth').get('kilo-bits')) * 1000 / 1e+6)
                self._list_comp_one(allocation, policies, key, i)
            elif 'percent' in i.get('class').get("action-list").get('bandwidth'):
                allocation = i.get('class').get("action-list").get('bandwidth').get('percent')
                self._list_comp_one(allocation, policies, key, i)
        elif i.get('class').get('action-list').get("action-type") == 'priority':
            if 'kilo-bits' in i.get('class').get("action-list").get('priority'):
                allocation = round(int(i.get('class').get("action-list").get('priority').get('kilo-bits')) * 1000 / 1e+6)
                self._list_comp_one(allocation, policies, key, i)
            elif 'percent' in i.get('class').get("action-list").get('priority'):
                allocation = i.get('class').get("action-list").get('priority').get('percent')
                self._list_comp_one(allocation, policies, key, i)
        elif i.get('class').get('action-list').get("action-type") == 'police':
            allocation = round(int(i.get('class').get("action-list").get('police').get('bit-rate')) / 1e+6)
            self._list_comp_one(allocation, policies, key, i)
        elif i.get('class').get('action-list').get("action-type") == 'shape':
            if 'bit-rate' in i.get('class').get("action-list").get('shape').get('average'):
                allocation = round(int(i.get('class').get("action-list").get('shape').get('average').get('bit-rate')) / 1e+6)
                self._list_comp_one(allocation, policies, key, i)
            elif 'percent' in i.get('class').get("action-list").get('shape').get('average'):
                allocation = i.get('class').get("action-list").get('shape').get('average').get('percent')
                self._list_comp_one(allocation, policies, key, i)


    def _list_comp_one(self, allocation, policies, key, i):
        """Takes sliced data configuration and matches it to a configured queue"""

        [self.queue_calculation(new_stat, old_stat, allocation=allocation) for old_stat, new_stat in
         zip(self.policies[key][0]['queues'], policies[key][0]['queues']) if
         i.get('class').get('name') == new_stat.get('parent_path').split()[-1:][0]]


    def _list_comp_two(self, allocation, policies, key, queue):
        """Takes data sliced configuration and matches it to a configured queue"""

        [self.queue_calculation(new_stat, old_stat, allocation=allocation) for old_stat, new_stat in
         zip(self.policies[key][0]['queues'], policies[key][0]['queues']) if
         queue.get('name') == new_stat.get('parent_path').split()[-1:][0]]


    def queue_calculation(self, new_stat, old_stat, allocation=None):
        """Queue diffrence calculations"""
        # Ensure the queues are the parent queues using parent path ietf-interfaces yang model
        if len(new_stat.get('parent_path').split()) == 2:
            print(new_stat.get('bytes') - old_stat.get('bytes'))

            self.calc_stats[new_stat.get('parent_path')].append({'queue_name': new_stat.get('queue_name'),
                                                      'allocation': allocation,
                                                      'parent_path': old_stat.get('parent_path').split()[0],
                                                      'who_am_i': 'parent',
                                                      'bytes': new_stat.get(
                                                          'bytes') - old_stat.get('bytes'),
                                                      'packets': new_stat.get(
                                                          'packets') - old_stat.get('packets'),
                                                      'out_bytes': new_stat.get(
                                                          'out_bytes') - old_stat.get(
                                                          'out_bytes'),
                                                      'out_packets': new_stat.get(
                                                          'out_packets') - old_stat.get(
                                                          'out_packets'),
                                                      'drop_packets': new_stat.get(
                                                          'drop_packets') - old_stat.get(
                                                          'drop_packets'),
                                                      'drop_bytes': new_stat.get(
                                                          'drop_bytes') - old_stat.get(
                                                          'drop_bytes'),
                                                                 'speed': new_stat.get('speed')})
            #Reverse list so parent policies are presented first on the web page
            self.calc_stats[new_stat.get('parent_path')].reverse()
        else:
            for k in self.policies.keys():
                #Ensure the queues arnt a the parent queues using parent path ietf-interfaces yang model
                if ' '.join(new_stat.get('parent_path').split()[:2]) == ' '.join(k.split()[:2]) and new_stat.get('queue_name') != new_stat.get('parent_path').split()[1]:
                    self.calc_stats[' '.join(k.split()[:2])].append({'queue_name': new_stat.get('queue_name'),
                                                              'allocation': allocation,
                                                              'parent_path': ' '.join(new_stat.get('parent_path').split()[:3]),
                                                              'who_am_i': 'child',
                                                              'bytes': new_stat.get(
                                                                  'bytes') - old_stat.get('bytes'),
                                                              'packets': new_stat.get(
                                                                  'packets') - old_stat.get('packets'),
                                                              'out_bytes': new_stat.get(
                                                                  'out_bytes') - old_stat.get(
                                                                  'out_bytes'),
                                                              'out_packets': new_stat.get(
                                                                  'out_packets') - old_stat.get(
                                                                  'out_packets'),
                                                              'drop_packets': new_stat.get(
                                                                  'drop_packets') - old_stat.get(
                                                                  'drop_packets'),
                                                              'drop_bytes': new_stat.get(
                                                                  'drop_bytes') - old_stat.get(
                                                                  'drop_bytes'),
                                                                     'match': [SearchClassMaps.search_strings(i) for i in
                                                                               self.qos_policies[1] if i.get('name') == new_stat.get('queue_name')][0],
                                                                     'speed': new_stat.get('speed')})

                    break
            #Reverse list so parent policies are presented first on the web page
            self.calc_stats[new_stat.get('parent_path')].reverse()
