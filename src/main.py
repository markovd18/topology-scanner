import scapy.all as scapy
import pysnmp.hlapi as pysnmp


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
    print(get_table_by_ip(scapy.get_if_addr(default_iface)))
    print(default_iface)
    print(interfaces)


if __name__ == "__main__":
    main()
