import json

def read_json(path):
    f = open(path, 'r')
    dat = f.read()
    f.close()
    return json.loads(dat)