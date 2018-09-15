import os
import tempfile


class File:
    def __init__(self, path):
        self.path = path
        with open(path, 'a+') as _:
            pass
        self._read_fd = open(path, 'r')

    def write(self, string):
        with open(self.path, 'a+') as f:
            f.write(string)

    def __add__(self, obj):
        sum_file = File(os.path.join(tempfile.gettempdir(), 'sum.txt'))
        for curr_path in [self.path, obj.path]:
            with open(curr_path, 'r') as f:
                sum_file.write(f.read())

        return sum_file

    def __iter__(self):
        return iter([x.strip() for x in self._read_fd.readlines()])

    def __str__(self):
        return self.path

    def __del__(self):
        self._read_fd.close()


if __name__ == '__main__':
    f = File('/tmp/first.txt')
    g = File('/tmp/second.txt')
    h = f + g
    print(h)
    for i in h:
        print(i)
