import random
import socket
import typing

import msgspec
import requests


class Station(msgspec.Struct):
    stationuuid: str
    name: str
    url: str


class RadioBrowserAPI:
    def __init__(self) -> None:
        self.base_url = self.get_base_url()

    def get_base_url(self):
        hosts = []
        ips = socket.getaddrinfo(
            "all.api.radio-browser.info", port=80, proto=socket.IPPROTO_TCP
        )

        for ip in ips:
            ip_address = ip[4][0]
            host = socket.gethostbyaddr(ip_address)[0]

            if host not in hosts:
                hosts.append(host)

        return f"https://{random.choice(hosts)}/json"

    def search(self, name: str):
        response = requests.get(
            f"{self.base_url}/stations/byname/{name}", params={"limit": 25}
        )

        return msgspec.json.decode(response.text, type=typing.List[Station])
