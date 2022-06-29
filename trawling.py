from itertools import combinations
import networkx as nx
from collections import Counter

G = nx.karate_club_graph()

# Zamieniamy graf na koszyki
buckets = []

for v in list(G.nodes):
  bucket = []
  for edge in G.edges(v):
    bucket.append(edge[1])

  buckets.append(bucket)

frequent_sets = Counter()

# Przechodzimy po koszykach i zliczamy ilosc wystapien zbiorow 3-elementowych
for b, bucket_index in zip(buckets, range(len(buckets))):
  if len(b) > 2:
    all_threes_in_bucket = list(combinations(b, 3))
    for three in all_threes_in_bucket:
      frequent_sets[three] += 1


# Wybieramy zbiory, ktore wystapily co najmniej dwa razy
supported_sets = {k: v for k, v in frequent_sets.items() if v >= 2}

# Wynik
result = { k for k in supported_sets.keys() }
print(result)
print(len(result))