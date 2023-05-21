import scapy.all as scapy
import scapy.layers.dhcp as dhcp
import pysnmp.hlapi as pysnmp


def send_dhcp_discover() -> dhcp.Packet:
    dhcp_offer: dhcp.Packet = dhcp.dhcp_request()
    dhcp_offer.display()
    return dhcp_offer


def find_router_ip_in_dhcp_offer(dhcp_offer: dhcp.Packet) -> str | None:
    return find_router_ip(dhcp_offer["DHCP"].options)


def find_router_ip(options: list[tuple[str, str]]) -> str | None:
    for option in options:
        if option[0] == "router":
            return option[1]

    return None


def get_table_by_ip(ip):
    iterator = pysnmp.nextCmd(
        pysnmp.SnmpEngine(),
        pysnmp.CommunityData("public", mpModel=0),
        pysnmp.UdpTransportTarget((ip, 161)),
        pysnmp.ContextData(),
        pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifDescr")),
        pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifType")),
        pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifMtu")),
        pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifSpeed")),
        pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifPhysAddress")),
        pysnmp.ObjectType(pysnmp.ObjectIdentity("IF-MIB", "ifType")),
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
    print(router_ip)


if __name__ == "__main__":
    main()
