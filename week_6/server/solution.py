import asyncio


class ClientServerProtocol(asyncio.Protocol):
    container_global = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode(), ClientServerProtocol.container_global)
        self.transport.write(resp.encode())


class Server:
    def __init__(self):
        self.container = {}

    async def handle(self, reader, writer):
        data = await reader.read(1024)
        resp = await process_data(data.decode(), self.container)
        writer.write(resp.encode())


def process_data(data, container):
    data_list = data.split()

    if data_list[0] == 'get':
        string = "ok\n"
        if data_list[1] == '*':
            for curr_map in container:
                for arr in container[curr_map]:
                    string += curr_map + " " + str(arr[0]) + " " + str(arr[1]) + "\n"
        elif data_list[1] in container:
            for arr in container[data_list[1]]:
                string += data_list[1] + " " + str(arr[0]) + " " + str(arr[1]) + "\n"

        string += "\n"
        return string

    elif data_list[0] == 'put':
        element = (float(data_list[2]), int(data_list[3]))

        if data_list[1] in container:
            if element not in container[data_list[1]]:
                container[data_list[1]].append(element)
        else:
            container[data_list[1]] = [element]

        return "ok\n\n"

    else:
        return "error\nwrong command\n\n"


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
