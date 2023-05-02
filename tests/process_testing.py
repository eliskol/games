import multiprocessing as mp


def test_func(num):
    return (num**123) % 7


# bruh = mp.Process(target=test_func, args=('this',))
# bruh2 = mp.Process(target=test_func, args=('that',))
# bruh3 = mp.Process(target=test_func, args=('other',))

# bruh.start()
# bruh2.start()
# bruh3.start()

pool = mp.Pool()
result1 = pool.apply_async(test_func, [12341])
result2 = pool.apply_async(test_func, [2398173])
answer1 = result1.get()
answer2 = result2.get()
print(answer1, answer2)

# how i'd use this:
#    calculate heuristic values two at a time, unless there's a bottleneck somewhere else
#    might be a bottleneck at layer generation? (which part, exactly, would cause a bottleneck?)
