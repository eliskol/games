from multiprocessing import Process, Value, Array, Queue


def f(q: Queue, item):
    q.put(item)


if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=f, args=(q, 'hi'))
    p2 = Process(target=f, args=(q, 'hello'))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(q.get())
    print(q.get())
