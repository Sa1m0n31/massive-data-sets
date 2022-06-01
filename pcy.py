from itertools import combinations
from bitarray import bitarray
import mmh3

# Dane
P = ('m', 'c', 'p', 'b', 'j')
k1 = ('m', 'c', 'b')
k2 = ('m', 'p', 'j')
k3 = ('m', 'b')
k4 = ('c', 'j')
k5 = ('m', 'p', 'b')
k6 = ('m', 'c', 'b', 'j')
k7 = ('c', 'b', 'j')
k8 = ('b', 'c')
K = (k1, k2, k3, k4, k5, k6, k7, k8)


def PCY(data, support):
    c1 = {}
    hash_table = {}
    # PIERWSZY PRZEBIEG
    for basket in data:
        # Zliczamy kandydatow do jednoelementowych zbiorow czestych
        for item in basket:
            if item in c1:
                c1[item] += 1
            else:
                c1[item] = 1

        # haszujemy wszystkie pary elementow
        for p in list(combinations(basket, 2)):
            hash_value = mmh3.hash(str(p), 10) % 100
            if hash_value in hash_table:
                hash_table[hash_value] += 1
            else:
                hash_table[hash_value] = 1

    # Wybieramy elementy czeste
    l1 = []
    for candidate_key, candidate_value in c1.items():
        if candidate_value >= support:
            l1.append(candidate_key)

    # Zamieniamy slownik ze zliczeniami na bitmape
    hash_bitmap = bitarray()
    for i in range(100):
        if i in hash_table:
            if hash_table[i] >= support:
                hash_bitmap.append(1)
            else:
                hash_bitmap.append(0)
        else:
            hash_bitmap.append(0)

    # DRUGI PRZEBIEG
    second_hash_table = {}
    for basket in data:
        for pair in list(combinations(basket, 2)): # lecimy tylko po parach, ktore sa w koszyku
            if hash_bitmap[mmh3.hash(str(pair), 10) % 100] == 1:
                if set(pair).issubset(set(l1)):
                    # Haszujemy po raz drugi
                    hash_value = mmh3.hash(str(pair), 20) % 100
                    if hash_value in second_hash_table:
                        second_hash_table[hash_value] += 1
                    else:
                        second_hash_table[hash_value] = 1


    # Zamieniamy drugie hasze na bitmape
    second_hash_bitmap = bitarray()
    for i in range(100):
        if i in second_hash_table:
            if second_hash_table[i] >= support:
                second_hash_bitmap.append(1)
            else:
                second_hash_bitmap.append(0)
        else:
            second_hash_bitmap.append(0)

    # TRZECI PRZEBIEG
    c2 = {}
    for basket in data:
        # Zliczamy pary tylko jesli: i oraz j naleza do l1, (i, j) haszuja sie do czestego kubelka w pierwszym i drugim haszowaniu
        for pair in list(combinations(basket, 2)):
            if (hash_bitmap[mmh3.hash(str(pair), 10) % 100] == 1) and (second_hash_bitmap[mmh3.hash(str(pair), 20) % 100] == 1):
                if set(pair).issubset(set(l1)):
                    if pair in c2:
                        c2[pair] += 1
                    else:
                        c2[pair] = 1

    # Wybieramy pary czeste
    l2 = []
    for candidate_key, candidate_value in c2.items():
        if candidate_value >= support:
            l2.append(candidate_key)

    def is_pair_in_l2(pr):
        for el in l2:
            if el == pr:
                return True

        return False

    def all_pairs_belongs_to_l2(tr):
        all_pairs = list(combinations(tr, 2))
        pairs_counter = 0
        for pr in all_pairs:
            if is_pair_in_l2(pr):
                pairs_counter += 1

        return pairs_counter == 3

    # CZWARTY PRZEBIEG - zliczamy kandydatow na zbiory czeste trzyelementowe
    c3 = {}
    for basket in data:
        threes_in_basket = list(combinations(basket, 3))
        for three in threes_in_basket:
            if set(three[0]).issubset(l1) and set(three[1]).issubset(l1) and set(three[2]).issubset(l1):
                if all_pairs_belongs_to_l2(three):
                    if three in c3:
                        c3[three] += 1
                    else:
                        c3[three] = 1

    # Wybieramy zbiory czeste
    l3 = []
    for candidate_key, candidate_value in c3.items():
        if candidate_value >= support:
            l3.append(candidate_key)

    print(f"L1: {l1}")
    print(f"L2: {l2}")
    print(f"L3: {l3}")


PCY(K, 3)