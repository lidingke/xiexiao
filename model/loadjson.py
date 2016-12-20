import json

class WriteReadJson(object):
    """docstring for WriteReadJson"""
    def __init__(self, dir_):
        super(WriteReadJson, self).__init__()
        self.dir_ = dir_
        self.store = {}

    def load(self):
        with open(self.dir_,'rb') as f:
            # try:
            bitFileRead2Str = f.read().decode('utf-8')
            self.store = json.loads(bitFileRead2Str)
            # except FileNotFoundError:

            # except Exception as e:
            #     raise e
        return self.store

    def save(self , store):
        with open(self.dir_,'wb') as f:
            jsonBitBuffer = json.dumps(store).encode('utf-8')
            # print('json', jsonBitBuffer)
            f.write(jsonBitBuffer)