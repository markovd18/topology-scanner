from scapy.all import *
from pysnmp.hlapi import *


def find_topology():
    print("----------------- Topology -----------------")
    routing_table = []
    # SNMP parameters

    # SNMP request to retrieve routing table (OID: 1.3.6.1.2.1.4.21.1)
    var_binds = nextCmd(
        SnmpEngine(),
        CommunityData(communityIndex="public", mpModel=1),
        UdpTransportTarget(("192.168.1.1", 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0)),
    )
    # ObjectType(ObjectIdentity("1.3.6.1.2.1.4.21.1")),
    # lexicographicMode=False)

    # Process SNMP response
    for error_indication, error_status, var_bind_table in var_binds:
        print(f"error_indication: {error_indication}")
        if error_indication:
            print(f"Error indicator: {error_indication}")
            return routing_table

        print(f"error_status: {error_status}")
        if error_status:
            print(f"Error status: {error_status.prettyPrint()}")
            return routing_table

        # Extract routing table information
        # for var_bind in var_bind_table:
        #     oid = var_bind[0]
        #     value = var_bind[1]


find_topology()
