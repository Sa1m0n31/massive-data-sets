import random

class AMS:
    def __init__(self, stream, t1, t2, t3):
        self.stream_length = len(stream)
        self.stream = stream
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3

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

    def single_estimation(self, count):
        return self.stream_length * (2 * count - 1)

    def estimate(self):
        letter_counter = [0, 0, 0]
        for letter, index in zip(self.stream, range(self.stream_length)):
            if letter == 'a' and index >= self.t1:
                letter_counter[0] += 1
            elif letter == 'b' and index >= self.t2:
                letter_counter[1] += 1
            elif letter == 'c' and index >= self.t3:
                letter_counter[2] += 1

        estimations = list(map(self.single_estimation, letter_counter))
        return round(sum(estimations) / len(estimations))


data = 'abcbdacdabdcaab'
estimations = []

ams = AMS(data, 1, 1, 1)
true_second_moment = ams.second_moment()

# run estimations in loop 100 times
for i in range(100):
    random_points_in_time = random.choices(range(len(data)), k=3)
    ams = AMS(data, random_points_in_time[0], random_points_in_time[1], random_points_in_time[2])
    estimations.append(ams.estimate())

estimations.sort()
median_of_estimations = estimations[round(len(estimations)/2)]
print(f"estimation: {median_of_estimations}")
print(f"real second moment: {true_second_moment}")