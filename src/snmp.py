import pysnmp.hlapi as pysnmp

from typing import List

SYS_NAME_OID = "1.3.6.1.2.1.1.5"
ROUTING_TABLE_ENTRY_OID = "1.3.6.1.2.1.4.21.1"
ROUTING_TABLE_ENTRY_IP_OID = "1.3.6.1.2.1.4.21.1.1"
ROUTING_TABLE_ENTRY_MASK_OID = "1.3.6.1.2.1.4.21.1.11"
ROUTING_TABLE_ENTRY_TYPE_OID = "1.3.6.1.2.1.4.21.1.8"
ROUTING_TABLE_ENTRY_DIST_OID = "1.3.6.1.2.1.4.21.1.1"
IP_ADDRESS_ENTRY_OID = "1.3.6.1.2.1.4.20.1.1"
ROUTING_TABLE_NEXT_HOP_OID = "1.3.6.1.2.1.4.21.1.7"


def get_snmp_object_identity(ip: str, object_oid: str) -> List[str]:
    iterator = pysnmp.nextCmd(
        pysnmp.SnmpEngine(),
        pysnmp.CommunityData(communityIndex="PSIPUB", mpModel=0),
        pysnmp.UdpTransportTarget((ip, 161)),
        pysnmp.ContextData(),
        pysnmp.ObjectType(pysnmp.ObjectIdentity(object_oid)),
        lexicographicMode=False,
    )

    result: List[str] = []
    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print(errorIndication)
            break

        elif errorStatus:
            print(
                "%s at %s"
                % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                )
            )
            break

        else:
            for varBind in varBinds:
                # print(" = ".join([x.prettyPrint() for x in varBind]))
                result.append(varBind[1].prettyPrint())

    return result


def get_routing_table_next_hop_entries(router_ip: str) -> List[str]:
    return get_snmp_object_identity(
        ip=router_ip,
        object_oid=ROUTING_TABLE_NEXT_HOP_OID,
    )


def get_router_ip_addresses(router_ip: str) -> List[str]:
    return get_snmp_object_identity(
        ip=router_ip,
        object_oid=IP_ADDRESS_ENTRY_OID,
    )


def get_router_host_name(router_ip: str) -> str:
    return get_snmp_object_identity(
        ip=router_ip,
        object_oid=SYS_NAME_OID,
    )[0]
