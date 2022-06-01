def read_dataset(fname):
    file_iter = open(fname, 'r')
    data = []
    for line in file_iter:
        data.append(line.strip().strip(',').split(','))
    return data


def apriori(data, k, support):
    # zliczamy wystepowanie pojedynczych elementów
    supposed = {}
    for row in data:
        for entry in row:
            if entry not in supposed.keys():
                supposed[entry] = 0
            supposed[entry] += 1

    # wybieramy elementy częste (te, których liczba wystąpień jest większa lub równa support)
    frequentitems = [[] for _ in range(k)]
    for entry in supposed.keys():
        if supposed[entry] >= support:
            frequentitems[0].append(set([entry]))

    # tworzenie krotek o rozmiarach od 2 do k i wybieranie z nich zbiorów częstych
    # iterujemy po i = 1,...,k żeby spośród zbiorów częstych o rozmiarze i, utworzyć
    # krotki o rozmiarze i+1 i szukać wśród nich zbiorów częstych
    for i in range(1, k):
        # tworzenie krotek o rozmiarze i+1
        supposedlist = []
        for fi in frequentitems[i - 1]:
            for fi0 in frequentitems[0]:
                funion = fi.union(fi0)
                if len(funion) == i + 1:
                    supposedlist.append(funion)

        # zliczanie ilości wystąpień krotki w danych
        # +1 jeśli wszystkie elementy krotki wystąpują w "wierszu"
        counterlist = [0 for _ in supposedlist]
        for row in data:
            for item in range(len(supposedlist)):
                if supposedlist[item].issubset(set(row)):
                    counterlist[item] += 1

        # wybieranie elementów częstych
        for m in range(len(counterlist)):
            if counterlist[m] >= support:
                if supposedlist[m] not in frequentitems[i]:  # żeby w zbiorach częstych nie było powtórek
                    frequentitems[i].append(supposedlist[m])
        # print(frequentitems[i])

    return frequentitems[k - 1]


data = read_dataset('DATASET.csv')
k = 4
result = apriori(data, k, 10)
print(result)