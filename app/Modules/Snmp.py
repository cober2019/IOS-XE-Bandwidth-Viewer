from pysnmp.hlapi import *

def get_current_cpu(device, snmp_comm):
    """Poll CPU usage using snmp OID 1.3.6.1.4.1.9.2.1.56.0"""

    cpu_usage = 0
    iterator = getCmd(SnmpEngine(),
                      CommunityData(f'{snmp_comm}'),
                      UdpTransportTarget((f'{device}', 161)),
                      ContextData(),
                      ObjectType(ObjectIdentity('1.3.6.1.4.1.9.2.1.56.0')))

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:  # SNMP engine errors
        pass
    else:
        if errorStatus:  # SNMP agent errors
           pass
        else:
            for varBind in varBinds:  # SNMP response contents
                cpu_usage = [x.prettyPrint() for x in varBind][1]

    return cpu_usage
