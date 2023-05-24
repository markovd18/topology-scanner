import scapy.all as scapy
import scapy.layers.dhcp as dhcp
import scapy.layers.l2 as l2
import pysnmp.hlapi as pysnmp

from typing import List, Tuple, Union

SYS_NAME_OID = "1.3.6.1.2.1.1.5"
ROUTING_TABLE_ENTRY_OID = "1.3.6.1.2.1.4.21.1"
ROUTING_TABLE_ENTRY_IP_OID = "1.3.6.1.2.1.4.21.1.1"
ROUTING_TABLE_ENTRY_MASK_OID = "1.3.6.1.2.1.4.21.1.11"
ROUTING_TABLE_ENTRY_TYPE_OID = "1.3.6.1.2.1.4.21.1.8"
ROUTING_TABLE_ENTRY_DIST_OID = "1.3.6.1.2.1.4.21.1.1"
IP_ADDRESS_ENTRY_OID = "1.3.6.1.2.1.4.20.1.1"


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


def get_routing_table_entries(ip: str) -> List[str]:
    iterator = pysnmp.nextCmd(
        pysnmp.SnmpEngine(),
        pysnmp.CommunityData(communityIndex="PSIPUB", mpModel=0),
        pysnmp.UdpTransportTarget((ip, 161)),
        pysnmp.ContextData(),
        # pysnmp.ObjectType(pysnmp.ObjectIdentity(ROUTING_TABLE_ENTRY_IP_OID)),
        # pysnmp.ObjectType(pysnmp.ObjectIdentity(ROUTING_TABLE_ENTRY_OID)),
        pysnmp.ObjectType(pysnmp.ObjectIdentity(IP_ADDRESS_ENTRY_OID)),
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
                print(" = ".join([x.prettyPrint() for x in varBind]))
                result.append(varBind[1].prettyPrint())

    return result


def address_is_local(ip: str) -> bool:
    return ip.startswith("192.168.") or ip.startswith("10.")


def retain_local_net_router_ips(table_entries: List[str]) -> List[str]:
    return [
        entry
        for entry in table_entries
        if not entry.endswith(".0") and address_is_local(entry)
    ]


def main():
    scapy.conf.checkIPaddr = False

    dhcp_offer = send_dhcp_discover()
    router_ip = find_router_ip_in_dhcp_offer(dhcp_offer)
    if not router_ip:
        print("Default router IP address was not found. Aborting...")
        return 1

    print(router_ip)
    table_entries = get_routing_table_entries(router_ip)
    print(table_entries)
    router_ips = retain_local_net_router_ips(table_entries)
    print(router_ips)


if __name__ == "__main__":
    main()
