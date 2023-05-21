import socket
from scapy.all import ARP, Ether, srp, conf
from pysnmp.hlapi import *


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip


def get_mac(ip):
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=False)[0]
    return result[0][1].src


def get_neighbors(ip):
    iterator = nextCmd(
        SnmpEngine(),
        CommunityData("public", mpModel=0),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0)),
        lexicographicMode=False,
    )

    neighbors = []
    for response in iterator:
        for varbind in response[3]:
            neighbors.append(varbind[2].prettyPrint())

    return neighbors


def discover_topology():
    ip = conf.route.route("0.0.0.0")[2]
    print(ip)
    mac_address = get_mac(ip)
    neighbors = get_neighbors(ip)

    print("IP Address: " + ip)
    print("MAC Address: " + mac_address)
    print("Neighbors:")
    for neighbor in neighbors:
        print(neighbor)


if __name__ == "__main__":
    discover_topology()
