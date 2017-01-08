from util.load import WRpickle
import pdb
import collections
from model.filter import Filter






def test_load_powerdatas():
    wr = WRpickle("tests\\data\\datasforfilter.pickle")
    data = wr.loadPick()
    data = data[0]
    # one = 0.0
    data1 = []
    # for x in data:
    #     if x == one:
    #         continue
    #     else:
    #         one = x
    #         data1.append(x)
    one = Filter()
    for x in data:
        x = one.run(x)
        if x :
            data1.append(x)
    for d in data1:
        print(d)
    print(len(data),len(data1))

    # pdb.set_trace()
    # for i in data:
    #     x,y = i
    #     print(x,y)



if __name__ == "__main__":
    test_load_powerdatas()