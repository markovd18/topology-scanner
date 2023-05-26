from dhcp import find_router_ip_in_dhcp_offer, send_dhcp_discover
from routing import Router, has_router_with_ip
from snmp import (
    get_router_host_name,
    get_router_ip_addresses,
    get_routing_table_next_hop_entries,
)

from typing import Set


def print_topology(routers: Set[Router]):
    """Prints network topology."""
    print("------------------------")
    print("\tNetwork topology")
    print("------------------------")
    for router in routers:
        print(str(router))
        print("------------------------")


def main():
    dhcp_offer = send_dhcp_discover()
    if not dhcp_offer:
        print("DHCP Offer packet was not receiver. Unable to scan network topology.")
        return 1

    router_ip = find_router_ip_in_dhcp_offer(dhcp_offer)
    if not router_ip:
        print("Default router IP address was not found. Aborting...")
        return 1

    processed: Set[Router] = set()
    addresses = [router_ip]
    while len(addresses) > 0:
        address = addresses.pop(0)
        if has_router_with_ip(processed, address):
            continue

        print("Processing %s" % address)
        table_entries = get_routing_table_next_hop_entries(address)
        if len(table_entries) == 0:
            continue

        ip_addresses = get_router_ip_addresses(address)
        result = [
            entry
            for entry in table_entries
            if entry not in ip_addresses and entry != "0.0.0.0"
        ]

        sysname = get_router_host_name(address)
        router = Router(
            ip_addresses=ip_addresses, sys_name=sysname, neighbors=set(result)
        )
        addresses.extend(result)
        processed.add(router)

    print_topology(processed)


if __name__ == "__main__":
    main()
