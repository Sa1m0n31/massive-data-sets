import pandas as pd
import numpy as np
from random import randint
import seaborn as sns

# load data
logs = pd.from_csv('data.txt')

# naive
sample_naive = logs.sample(frac=0.1)
print(sample_naive)
# print(sns.histplot(sample_naive))

# hash sampling
sample_hash = logs[lambda x: hash(x) % 10 == 1]
print(sample_hash)
# print(sns.histplot(sample_hash))