import pandas as pd
import mmh3
import seaborn as sns

class BloomFilter:
    def __init__(self, N, k):
        self.S = [0] * N
        self.N = N
        self.k = k

    def update(self, el):
        for i in range(self.k):
            self.S[mmh3.hash(el, i) % self.N] = 1

    def check(self, el):
        for i in range(self.k):
            if not self.S[mmh3.hash(el, i) % self.N]:
                return 0
        return 1

data_to_update = pd.read_csv('./sample_data/bloom_filter_update.txt', names=['word']).word
data_to_check = pd.read_csv('./sample_data/bloom_filter_check.txt', names=['word']).word

all_false_positives = []
all_false_negatives = []
all_true_positives = []
all_true_negatives = []

# check for different number of hash functions
for hash_func in range(1, 21):
    bloom = BloomFilter(4000, hash_func)
    bloom_results = []
    false_positives = 0
    true_positives = 0
    false_negatives = 0
    true_negatives = 0

    # update
    for el in data_to_update:
        bloom.update(el)

    # check
    for el in data_to_check:
        bloom_result = bloom.check(el)
        bloom_results.append(bloom_result)

    # check efficiency
    for check_el, i in zip(data_to_check, range(len(data_to_check))):
        for update_el in data_to_update:
            if update_el == check_el:
                if bloom_results[i] == 1:
                    true_positives += 1
                else:
                    false_negatives += 1
                break
        if bloom_results[i] == 1:
            false_positives += 1
        else:
            true_negatives += 1

    all_true_positives.append(true_positives)
    all_true_negatives.append(true_negatives)
    all_false_positives.append(false_positives)
    all_false_negatives.append(false_negatives)

# plot of number of false positives by number of hash functions
false_positives_plot = sns.lineplot(x=range(1,21), y=all_false_positives)
false_positives_plot.set_xlabel('Number of hash functions')
false_positives_plot.set_ylabel('Number of false positives')