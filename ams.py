import random
from collections import Counter


def get_unique_letters_from_stream(stream):
    unique_letters = []
    for letter in stream:
        if letter not in unique_letters:
            unique_letters.append(letter)

    return unique_letters


class AMS:
    def __init__(self, stream, k, random_points_in_time):
        self.stream_length = k
        self.stream = stream
        self.random_points_in_time = random_points_in_time
        self.unique_letters = get_unique_letters_from_stream(stream)

    def second_moment(self):
        letter_counter = {}
        for letter in self.stream:
            if letter_counter.get(letter):
                letter_counter[letter] += 1
            else:
                letter_counter[letter] = 1

        second_moment_value = 0
        for val in letter_counter.values():
            second_moment_value += val ** 2

        return second_moment_value

    def get_letter_index(self, letter):
        for l, index in zip(self.unique_letters, range(len(self.unique_letters))):
            if l == letter:
                return index

    def single_estimation(self, count):
        return len(self.stream) * (2 * count - 1)

    def estimate(self):
        letter_counter = []
        letters_to_trace = []
        for letter, index in zip(self.stream, range(len(self.stream))):
            if index in self.random_points_in_time:
                letters_to_trace.append(letter)
                letter_counter.append(1)
            elif letter in letters_to_trace:
                for c, c_index in zip(letter_counter, range(len(letter_counter))):
                    if letters_to_trace[c_index] == letter:
                        letter_counter[c_index] += 1

        estimations = list(map(self.single_estimation, letter_counter))

        if len(estimations) != 0:
            return round(sum(estimations) / len(estimations))
        else:
            return 0


def get_number_of_unique_letters_in_stream(stream):
    return len(set(list(stream)))


data = 'abcbdacdabdcaabafdfsfdafafasdsfadsgdfasgdfasdgaf'
estimations = []
n = 3

ams = AMS(data, n, map(lambda x: 1, range(n)))
true_second_moment = ams.second_moment()

# run estimations in loop 100 times
for i in range(100):
    random_times = random.choices(range(len(data)), k=n)
    ams = AMS(data, n, random_times)
    estimations.append(ams.estimate())

estimations.sort()
median_of_estimations = estimations[round(len(estimations)/2)]
print(f"estymacja: {median_of_estimations}")
print(f"prawdziwy drugi moment: {true_second_moment}")