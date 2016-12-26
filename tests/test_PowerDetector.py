from model.modelpump import PowerDetector
from model.loadjson import WriteReadJson
import pdb

def test_powerdetector():
    # b'\x9aG\tY\t\x00\x00\x00\x00\xa9' 6w 3w
    #  b'\x9a<\x0f\xa4\t\x07\x00\x98\x06\xa9' 6.7
    pdetector = PowerDetector(serialNo='inclined')
    power = pdetector.hex2power(b'\xff\xff', b'\xff\xff')
    assert isinstance(power, float)
    # assert power > 100

def test_open_jsonfile():
    wr = WriteReadJson('data\\test\\detector.json')
    store = {'vertical':{'slope':1,'intercept':2},'inclined':{'slope':3,'intercept':4}}
    wr.save(store)
    get = wr.load()
    assert isinstance(get, dict)
    assert get == store


def test_json_para():
    pd = PowerDetector(detect = 'C50-MC', serialNo = 'vertical')
    get = pd._fitParaGet('vertical')
    assert len(get) == 2
    assert isinstance(get[0], int) or isinstance(get[0], float)



if __name__ == '__main__':
    wr = WriteReadJson('data\\detector.json')
    store = {'vertical':{'slope':1,'intercept':2},'inclined':{'slope':3,'intercept':4}}
    wr.save(store)
    get = wr.load()
    assert get == store
    pdb.set_trace()