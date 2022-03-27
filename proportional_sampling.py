import pandas as pd

logs = pd.read_table('./log.txt', sep=' ', names=('a', 'b'))
naive = logs.sample(frac=0.1)
print(naive)

mask = logs.apply(lambda x: hash(x.a) % 10 == 1, axis=1)
sample = logs[mask]
print(sample)