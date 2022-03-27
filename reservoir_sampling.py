import pandas as pd
from random import randint


class ReservoirSampling:
    def __init__(self, sc):
        self.SAMPLE_COUNT = sc
        self.sample = []
        self.idx = 0

    def update(self, new_sample):
        self.idx += 1

        if self.idx < self.SAMPLE_COUNT:
            self.sample.append(new_sample)
        else:
            r = randint(0, self.idx)

            if r < self.SAMPLE_COUNT:
                self.sample[r - 1] = new_sample


logs = pd.read_table('./log.txt', sep=' ', names=('a', 'b'))
rs = ReservoirSampling(100)

for index, row in logs.iterrows():
    rs.update(row)

print(rs.sample)