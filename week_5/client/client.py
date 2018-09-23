import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def put(self, key, value, timestamp=int(time.time())):
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                sock.sendall("put {} {} {}\n".format(key, value, timestamp).encode("utf8"))
                data = sock.recv(1024).decode("utf-8")
            except:
                raise ClientError

            if data.split("\n")[0] != 'ok':
                raise ClientError

    def get(self, key):
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                sock.sendall("get {}\n".format(key).encode("utf8"))
                data = sock.recv(1024).decode("utf-8")
                data_list = data.split("\n")
            except:
                raise ClientError

            if data_list[0] != 'ok':
                raise ClientError
            else:
                ret = {}
                for metric in data_list[1::]:
                    if metric == '':
                        continue

                    key, value, timestamp = metric.split()
                    element = (int(timestamp), float(value))
                    if key in ret:
                        ret[key].append(element)
                        sorted(ret[key], key=lambda values: values[1])
                    else:
                        ret[key] = [element]

                return ret
