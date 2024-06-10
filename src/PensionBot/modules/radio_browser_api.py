import random
import socket
import typing

import msgspec
import requests


class Station(msgspec.Struct):
    name: str
    url: str
    favicon: str
    homepage: str


class RadioBrowserAPI:
    def __init__(self) -> None:
        self.base_url = self.get_base_url()

    def get_base_url(self):
        hosts = []
        ips = socket.getaddrinfo(
            "all.api.radio-browser.info", port=80, proto=socket.IPPROTO_TCP
        )

        for ip_tupple in ips:
            ip = ip_tupple[4][0]
            host_addr = socket.gethostbyaddr(ip)

            if host_addr[0] not in hosts:
                hosts.append(host_addr[0])

        return f"https://{random.choice(hosts)}/json"

    def search(self, name: str) -> Station:
        response = requests.get(
            f"{self.base_url}/stations/byname/{name}", params={"limit": 1}
        )
        return msgspec.json.decode(response.text, type=typing.List[Station])[0]
