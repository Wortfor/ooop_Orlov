class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


class Server:
    __ip_counter = 0

    def __init__(self):
        Server.__ip_counter += 1
        self.__ip = Server.__ip_counter
        self.__buffer = []

    def send_data(self, data):
        self.__router.buffer.append(data)

    def get_data(self):
        packets = self.__buffer[:]
        self.__buffer.clear()
        return packets

    def get_ip(self):
        return self.__ip

    def _set_router(self, router):
        self.__router = router

    def _remove_router(self):
        self.__router = None

    def _receive(self, data):
        self.__buffer.append(data)


class Router:
    def __init__(self):
        self.buffer = []
        self.__servers = {}

    def link(self, server):
        server._set_router(self)
        self.__servers[server.get_ip()] = server

    def unlink(self, server):
        server._remove_router()
        self.__servers.pop(server.get_ip(), None)

    def send_data(self):
        for data in self.buffer:
            server = self.__servers.get(data.ip)
            if server:
                server._receive(data)
        self.buffer.clear()