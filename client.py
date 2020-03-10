import asyncio
import threading
import sys


class Client(asyncio.Protocol):

    def __init__(self, username, on_con_lost):
        self.username = username + '-> '
        self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport: asyncio.transports.BaseTransport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        sys.stdout.write('\b' * len(self.username))
        message = data.decode()
        print(f'{message}\n{self.username}', end=' ')

    def connection_lost(self, exc) -> None:
        self.on_con_lost.set_result(True)


def writing(client: Client, transport: asyncio.transports.BaseTransport) -> None:
    while True:
        input_ = input(client.username)
        message = client.username + input_
        transport.write(message.encode())
        if input_ == ':exit':
            break


async def main():
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()
    username = input('Insert your username: ')
    while len(username) > 20:
        username = input('Insert your username: ').strip()

    client = Client(username, on_con_lost)

    transport, protocol = await loop.create_connection(lambda: client, '127.0.0.1', 8888)
    thread = threading.Thread(target=writing, args=(client, transport))
    thread.start()
    try:
        await on_con_lost
    finally:
        transport.close()
        thread.join()


if __name__ == '__main__':
    asyncio.run(main())
