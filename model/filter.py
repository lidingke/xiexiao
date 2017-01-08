from __future__ import  division
import collections

class Filter(object):

    def __init__(self):
        self.oldforrepet = 0
        self.oldbeforcounter = 0.0001
        self.counter = 0
        self.queue = collections.deque(maxlen=5)

    def removeRepet(self, data):
        if data != self.oldforrepet:
            self.oldforrepet = data
            return data

    def medianMean(self, datas):
        if isinstance(datas,collections.deque):
            datas = list(datas)

        if len(datas) < 5:
            return datas[-1]
        datas.sort()
        datas = datas[1:-1]
        # pdb.set_trace()
        result = sum(datas)/len(datas)
        return result




    def run(self, data):
        data = self.removeRepet(data)
        if data:
            self.queue.append(data)
            get_ = self.medianMean(self.queue)
            if abs(get_ - self.oldbeforcounter)/self.oldbeforcounter > 0.01:
                self.counter = self.counter + 1
            if self.counter > 3:
                self.counter = 0
                self.oldbeforcounter = get_
                return get_
            else:

                return self.oldbeforcounter