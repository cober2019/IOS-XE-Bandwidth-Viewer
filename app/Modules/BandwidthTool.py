"""Bandwidth calculator class used to poll and calculate various statistics"""

from ncclient import manager
import xmltodict
import time
import multiprocessing


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
    try:
        get_state = session.get(xml_filter)
        int_status = xmltodict.parse(get_state.xml)["rpc-reply"]["data"]
        interface_state = int_status["interfaces-state"]["interface"]
    except manager.operations.errors.TimeoutExpiredError as error:
        pass
    except AttributeError as error:
        pass
    except manager.transport.TransportError as error:
        pass
    except manager.operations.rpc.RPCError as error:
        pass

    return interface_state

class CalcBandwidth:
    """Bandwidth calculation class"""

    def __init__(self, host, netconf_port, username, password, interface):

        self.host = host
        self.netconf_port = netconf_port
        self.username = username
        self.password = password
        self._interface = interface
        self.previous_in_bandwidth = 0
        self.previous_out_bandwidth = 0
        self.previous_in_discards = 0
        self.previous_out_discards = 0

    def get_interface_bandwith_out(self):
        """Calculate outbound bandwidth"""

        mbps_out = -1

        try:
            with manager.connect(host=self.host, port=self.netconf_port, username=self.username, password=self.password,
                                 device_params={'name': 'csr'}) as session:

                interface = get_stats(session, interface=self._interface)

                try:
                    speed_conversion = int(int(interface.get("speed")))
                    bytes_out_diff = int(interface.get("statistics").get("out-octets", {})) - int(self.previous_out_bandwidth)
                    calc_1 = round(bytes_out_diff * 8 * 100, 4)
                    calc_2 = round(10 * int(speed_conversion), 2)
                    mbps_out = round(calc_1 / calc_2 / 100, 2) * int(speed_conversion / 1e+6)
                    self.previous_out_bandwidth = interface.get("statistics").get("out-octets", {})
                except ValueError:
                    pass
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

        return mbps_out

    def get_interface_bandwith_in(self):
        """Calculate inbound bandwidth"""

        mbps_in = -1

        try:
            with manager.connect(host=self.host, port=self.netconf_port, username=self.username, password=self.password,
                                 device_params={'name': 'csr'}) as session:

                interface = get_stats(session, interface=self._interface)

                try:
                    speed_conversion = int(int(interface.get("speed")))
                    bytes_in_diff = int(interface.get("statistics").get("in-octets", {})) - int(self.previous_in_bandwidth)
                    calc_1 = round(bytes_in_diff * 8 * 100, 4)
                    calc_2 = round(10 * int(speed_conversion), 2)
                    mbps_in = round(calc_1 / calc_2 / 100, 2)  * int(speed_conversion / 1e+6)
                    self.previous_in_bandwidth = interface.get("statistics").get("in-octets", {})
                except ValueError:
                    pass
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

        return mbps_in

    def get_interface_bandwith_out_discards(self):
        """Calculate outbound discards"""

        discards = -1

        try:
            with manager.connect(host=self.host, port=self.netconf_port, username=self.username, password=self.password,
                                 device_params={'name': 'csr'}) as session:

                interface = get_stats(session, interface=self._interface)

                try:
                    speed_conversion = int(int(interface.get("speed")))
                    discards = int(interface.get("statistics").get("out-discards", {})) - int(self.previous_out_discards)
                    self.previous_out_discards = interface.get("statistics").get("out-discards", {})
                except ValueError:
                    pass
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

        return discards

    def get_interface_bandwith_in_discards(self):
        """Calculate inbound discards"""

        discards = -1

        try:
            with manager.connect(host=self.host, port=self.netconf_port, username=self.username, password=self.password,
                                 device_params={'name': 'csr'}) as session:

                interface = get_stats(session, interface=self._interface)

                try:
                    speed_conversion = int(int(interface.get("speed")))
                    discards = int(interface.get("statistics").get("in-discards", {})) - int(self.previous_in_discards)
                    self.previous_in_discards = interface.get("statistics").get("in-discards", {})
                except ValueError:
                    pass
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

        return discards

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, interface):
        self._interface = interface



