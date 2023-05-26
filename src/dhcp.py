import scapy.all as scapy
import scapy.layers.dhcp as dhcp

from typing import Union, List, Tuple


def send_dhcp_discover() -> Union[dhcp.Packet, None]:
    scapy.conf.checkIPaddr = False
    dhcp_offer: dhcp.Packet = dhcp.dhcp_request()
    # dhcp_offer.display()
    return dhcp_offer


def find_router_ip_in_dhcp_offer(dhcp_offer: dhcp.Packet) -> Union[str, None]:
    dhcp_data = dhcp_offer["DHCP"]
    if not dhcp_data:
        return None
    
    return find_router_ip(dhcp_data.options)


def find_router_ip(options: List[Tuple[str, str]]) -> Union[str, None]:
    for option in options:
        if option[0] == "router":
            return option[1]

    return None
