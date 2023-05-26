from typing import Set


class Router:
    def __init__(self, ip_addresses: Set[str], sys_name: str):
        self.__ip_addresses = ip_addresses
        self.__sys_name = sys_name

    def __str__(self) -> str:
        return self.__sys_name + "\n" + "\n\t".join(self.__ip_addresses)

    def __eq__(self, __value: object) -> bool:
        return self.__sys_name == __value.__sys_name and str(
            self.__ip_addresses
        ) == str(__value.__ip_addresses)

    def __hash__(self) -> int:
        return hash(self.__sys_name) + hash(self.__ip_addresses)

    def has_ip_address(self, ip_address: str) -> bool:
        return ip_address in self.__ip_addresses


def has_router_with_ip(routers: Set["Router"], ip_address: str):
    for router in routers:
        if router.has_ip_address(ip_address):
            return True
    return False
