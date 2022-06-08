import os
import textwrap
import random
import mmh3


class MinHash:
    def __init__(self, doc_catalog_path, doc_to_search):
        self.docs = list(map(lambda x : os.path.join(os.getcwd(), 'emzd', 'documents', x), os.listdir(doc_catalog_path)))
        self.doc_to_search = doc_to_search
        self.shinglets = []
        self.signatures = []
        self.prime = 4294967311

    def jaccarda_compare(self, doc1_index, doc2_index):
        doc1 = self.shinglets[doc1_index]
        doc2 = self.shinglets[doc2_index]

        doc_sum = doc1.union(doc2)
        doc_intersection = doc1.intersection(doc2)
        return len(doc_intersection) / len(doc_sum)

    def min_hash_compare(self, doc1_index, doc2_index):
        signature1 = self.signatures[doc1_index]
        signature2 = self.signatures[doc2_index]

        similarity = 0

        for s1, s2 in zip(signature1, signature2):
            if s1 == s2:
                similarity += 1

        return similarity / 100

    def shingling(self, doc):
        doc_content = open(doc, encoding='utf-8').read()
        doc_shinglets = textwrap.wrap(doc_content, 5)
        self.shinglets.append(set(doc_shinglets))

    def shingling_all(self):
        for doc in self.docs:
            self.shingling(doc)

    def get_list_of_random_values(self, n):
        rand_list = []

        while n > 0:
            rand = random.randint(0, 100000)

            while rand in rand_list:
                rand = random.randint(0, 100000)

            rand_list.append(rand)
            n -= 1

        return rand_list

    def get_number_of_all_shinglets(self):
        big_set = set()
        for s in self.shinglets:
            new_set = set(s)
            big_set = big_set.union(new_set)

        return len(big_set)

    def get_all_shinglets(self):
        big_set = set()
        for s in self.shinglets:
            big_set = big_set.union(set(s))

        return big_set

    def minhash(self):
        a_values = self.get_list_of_random_values(100)
        b_values = self.get_list_of_random_values(100)

        N = self.get_number_of_all_shinglets()
        shinglets = self.get_all_shinglets()

        #print(shinglets)


        #print(">>>>", N, self.prime)

        signatures = [[self.prime + 1 for a in range(100)] for x in self.docs]

        # matrix
        matrix = []
        for r in shinglets:
            new_row = []
            for doc_index in range(len(self.docs)):
                if r in self.shinglets[doc_index]:
                    new_row.append(1)
                else:
                    new_row.append(0)

            matrix.append(new_row)
        import pandas as pd
        print(matrix)
        print(pd.DataFrame(matrix).head())
        exit()
        # min-hash
        for r in range(len(shinglets)):
            hash_values = []

            for i in range(100):
                hash_values.append(((a_values[i] * r + b_values[i]) % self.prime) % N)
            print(">>>",len(hash_values))

            for doc_index in range(len(self.docs)):
                if matrix[r][doc_index] == 1:
                    for j in range(100):
                        if hash_values[j] < signatures[doc_index][j]:
                            #print(hash_values[j], signatures[doc_index][j])

                            signatures[doc_index][j] = hash_values[j]


        print(signatures)
        self.signatures = signatures


min_hash = MinHash('./emzd/documents', open('./emzd/doc_to_search.txt'))

# Podzial dokumentow na shinglety
min_hash.shingling_all()

number_of_docs = len(min_hash.docs)

# Porownanie wszystkich dokumentow za pomoca indeksu Jaccarda
print("INDEX JACCARDA")
for i in range(number_of_docs):
    for j in range(i+1, number_of_docs):
        print(f"Dokumenty {i+1} i {j+1} sa podobne: {min_hash.jaccarda_compare(i, j)}")

# MinHash
min_hash.minhash()

# Porownanie wszystkich dokumentow za pomoca sygnatur MinHash
print('MIN HASH')
for i in range(number_of_docs):
    for j in range(i+1, number_of_docs):
        print(f"Dokumenty {i+1} i {j+1} sa podobne: {min_hash.min_hash_compare(i, j)}")