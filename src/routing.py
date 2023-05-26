from typing import Set


class Router:
    """
    Represents a router in the network topology described by IP addresses of it's interfaces, a host name and a set of neighbors.
    """

    def __init__(self, ip_addresses: Set[str], sys_name: str, neighbors: Set[str]):
        self.__ip_addresses = ip_addresses
        self.__sys_name = sys_name
        self.__neighbors = neighbors

    def __str__(self) -> str:
        return (
            self.__sys_name
            + ":\n\t"
            + "\n\t".join(self.__ip_addresses)
            + "\nNeighbors:\n\t"
            + "\n\t".join(self.__neighbors)
        )

    def __eq__(self, __value: object) -> bool:
        return str(self.__ip_addresses) == str(__value.__ip_addresses)

    def __hash__(self) -> int:
        return hash(tuple(self.__ip_addresses))

    def has_ip_address(self, ip_address: str) -> bool:
        return ip_address in self.__ip_addresses


def has_router_with_ip(routers: Set["Router"], ip_address: str):
    """Checks if there is a router with the given IP address in given set of routers.

    Args:
        routers (Set[&quot;Router&quot;]): set of routers to check
        ip_address (str): sought IP address

    Returns:
        bool: does any router have the given IP address
    """
    for router in routers:
        if router.has_ip_address(ip_address):
            return True
    return False
