import asyncio

class Server(asyncio.Protocol):

    connections = {}

    @staticmethod
    def broadcast(data: bytes, user: str) -> None:
        for key in Server.connections.keys():
            if key != user:
                Server.connections[key].write(data)

    def __init__(self):
        self.user = None

    def connection_made(self, transport: asyncio.transports.BaseTransport) -> None:
        self.user = transport.get_extra_info('peername')[0] + str(transport.get_extra_info('peername')[1])
        Server.connections[self.user] = transport

    def data_received(self, data: bytes) -> None:
        if ':exit' in data.decode():
            Server.connections[self.user].close()
            Server.connections.pop(self.user)
        else:
            Server.broadcast(data, self.user)


async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: Server(), '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
