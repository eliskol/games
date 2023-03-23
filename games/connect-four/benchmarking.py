import time

example_game_state = [[1, 0, 0, 2, 0, 0, 1],
                      [2, 1, 0, 1, 0, 0, 1],
                      [1, 2, 0, 2, 2, 2, 2],
                      [1, 1, 2, 1, 2, 1, 1],
                      [2, 1, 2, 1, 2, 2, 2],
                      [1, 2, 1, 2, 1, 2, 1]]

comprehension_times = []
filter_times = []
indexes = [[i, j] for i in range(6) for j in range(7)]
for _ in range(10000):
    start = time.time()
    filled_in_spaces = [[i, j] for [i, j] in indexes if example_game_state[i][j] != 0]
    end = time.time()
    comprehension_times.append(end - start)
    start = time.time()
    filled_in_spaces2 = list(filter(lambda index: example_game_state[index[0]][index[1]] != 0, indexes))
    end = time.time()
    filter_times.append(end - start)
    assert filled_in_spaces == filled_in_spaces2

print('comprehension', sum(comprehension_times) / len(comprehension_times))
print('filter', sum(filter_times) / len(filter_times))
print('filter' if sum(comprehension_times) / len(comprehension_times) > sum(filter_times) / len(filter_times) else 'comp')

# list comprehension is faster, but it probably won't matter; the times are on the scale of 1e-6