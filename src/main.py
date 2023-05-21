import scapy.all as scapy
import scapy.layers.dhcp as dhcp
import pysnmp.hlapi as pysnmp

from typing import List, Tuple, Union

SYS_NAME_OID = "1.3.6.1.2.1.1.5"
ROUTING_TABLE_ENTRY_OID = "1.3.6.1.2.1.4.21.1"
ROUTING_TABLE_ENTRY_IP_OID = "1.3.6.1.2.1.4.21.1.1"
ROUTING_TABLE_ENTRY_MASK_OID = "1.3.6.1.2.1.4.21.1.11"
ROUTING_TABLE_ENTRY_TYPE_OID = "1.3.6.1.2.1.4.21.1.8"


def send_dhcp_discover() -> dhcp.Packet:
    dhcp_offer: dhcp.Packet = dhcp.dhcp_request()
    dhcp_offer.display()
    return dhcp_offer


def find_router_ip_in_dhcp_offer(dhcp_offer: dhcp.Packet) -> Union[str, None]:
    return find_router_ip(dhcp_offer["DHCP"].options)


def find_router_ip(options: List[Tuple[str, str]]) -> Union[str, None]:
    for option in options:
        if option[0] == "router":
            return option[1]

    return None


def get_table_by_ip(ip: str):
    iterator = pysnmp.nextCmd(
        pysnmp.SnmpEngine(),
        pysnmp.CommunityData(communityIndex="public", mpModel=0),
        pysnmp.UdpTransportTarget((ip, 161)),
        pysnmp.ContextData(),
        # pysnmp.ObjectType(pysnmp.ObjectIdentity(SYS_NAME_OID)),
        pysnmp.ObjectType(pysnmp.ObjectIdentity(ROUTING_TABLE_ENTRY_IP_OID)),
        pysnmp.ObjectType(pysnmp.ObjectIdentity(ROUTING_TABLE_ENTRY_TYPE_OID)),
        # pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifDescr")),
        # pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifType")),
        # pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifMtu")),
        # pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifSpeed")),
        # pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifPhysAddress")),
        # pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifType")),
        lexicographicMode=False,
    )

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
                print(" = ".join([x.prettyPrint() for x in varBind]))


def main():
    interfaces = scapy.conf.ifaces
    default_iface = scapy.conf.iface
    print(scapy.get_if_addr(default_iface))
    print(scapy.get_if_hwaddr(default_iface))
    # print(get_table_by_ip("192.168.1.1"))
    print(default_iface)
    print(interfaces)

    print()

    scapy.conf.checkIPaddr = False

    dhcp_offer = send_dhcp_discover()
    router_ip = find_router_ip_in_dhcp_offer(dhcp_offer)
    if not router_ip:
        print("Default router IP address was not found. Aborting...")
        return 1

    print(router_ip)
    get_table_by_ip(router_ip)


if __name__ == "__main__":
    main()
