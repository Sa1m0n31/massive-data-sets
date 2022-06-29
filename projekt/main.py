import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

users_play_count = pd.read_table('./emzd/projekt/data/kaggle_visible_evaluation_triplets.txt',
                                 names=('user_id', 'track_id', 'play_count'),
                                 delim_whitespace=True)
mask = users_play_count.apply(lambda x: hash(x.user_id) % 10 == 1, axis=1)
sample_by_users = users_play_count[mask]

plt.hist(sample_by_users.play_count, bins=np.linspace(0, 100, 100))
plt.show()
