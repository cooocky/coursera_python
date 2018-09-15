import argparse
import json
import os
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--key", type=str)
parser.add_argument("--value", type=str)
args = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
with open(storage_path, 'a+') as f:
    pass

with open(storage_path, 'r') as f:
    data = f.read()
    container = {}

    if data is not '':
        container = json.loads(data)

if args.value:
    if args.key in container:
        container[args.key].append(args.value)
    else:
        new_list = list()
        new_list.append(args.value)
        container[args.key] = new_list

    with open(storage_path, 'w') as f:
        json.dump(container, f)
else:
    if args.key in container:
        print(', '.join(container[args.key]))
    else:
        print('')
