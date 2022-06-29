import pandas as pd
import mmh3
from collections import Counter


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


stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
             "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom",
             "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
             "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about",
             "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
             "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
             "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
             "just", "don", "should", "now"]

tracks_by_artist = pd.read_table('./emzd/projekt/data/musiXmatch-dane_z_id_trackow_i_tworcami.txt', sep='<SEP>', names=('track_id', 'artist', 'track_name'), usecols=[0, 1, 2], engine='python')
words_info = pd.read_table('./emzd/projekt/data/musiXmatch-dane_treningowe.txt', sep=',\d{4,},', names=('track_id', 'word_count'), skiprows=18, engine='python')
words_file = open('./emzd/projekt/data/musiXmatch-dane_treningowe.txt', encoding='utf8')
words_content = words_file.readlines()
words = words_content[17][1:].split(',')

random_artist_songs = tracks_by_artist[tracks_by_artist.artist == 'Michael Jackson'].sample(50)
jackson_songs_info = words_info[words_info.track_id.isin(list(random_artist_songs.track_id))]

bloom = BloomFilter(4000, 3)
similar_songs = []

# Dodawanie slow do filtru
for index, jackson_song in jackson_songs_info.iterrows():
    words_counter = Counter()

    # Wyrzucamy stopwords
    for word_count in jackson_song.word_count.split(','):
        w_index = int(word_count.split(':')[0])-1
        w_count = int(word_count.split(':')[1])

        if words[w_index] not in stopwords:
            words_counter[w_index] = w_count

    # Sortujemy wzgledem ilosci wystapien
    first_10_words_counter = words_counter.most_common()[:10]

    # Dodajemy do filtru Blooma 10 pierwszych slow z kazdej piosenki
    for word_count in first_10_words_counter:
        word_to_update = words[int(word_count[0])-1]
        bloom.update(word_to_update)


# Znajdywanie piosenek podobnych - uzycie filtru
for index, track in words_info.iterrows():
    words_counter = Counter()
    song_similar = True

    # Wyrzucamy stopwords
    for word_count in track.word_count.split(','):
        w_index = int(word_count.split(':')[0]) - 1
        w_count = int(word_count.split(':')[1])

        if words[w_index] not in stopwords:
            words_counter[w_index] = w_count

    # Sortujemy wzgledem ilosci wystapien
    first_10_words_counter = words_counter.most_common()[:10]

    # Sprawdzamy czy 10 pierwszych slow znajduje sie w filtrze Blooma
    for word_count in first_10_words_counter:
        word_to_check = words[int(word_count[0]) - 1]

        if bloom.check(word_to_check) != 1:
            song_similar = False
            break

    # Dodajemy piosenke do zbioru piosenek podobnych
    if song_similar:
        similar_songs.append(track.track_id)


# Wypisujemy podobne piosenki
for song in similar_songs:
    track = tracks_by_artist[tracks_by_artist.track_id == song].iloc[0]
    print(f"{track.artist}, {track.track_name}")