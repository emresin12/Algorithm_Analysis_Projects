import math
import random
import datetime


def my_func(N, is_random=True, fill=None):
    arr = []
    if is_random:
        for a in range(N):
            arr.append(random.randint(0, 3))
    else:
        for a in range(N):
            arr.append(fill)
    before = datetime.datetime.now()
    arr2 = [0, 0, 0, 0, 0]
    for i in range(0, N):
        if arr[i] == 0:
            for t1 in range(i, N):
                p1 = pow(t1, 1 / 2)
                x1 = N + 1
                while x1 >= 1:
                    x1 = math.floor(x1 / 2)
                    arr2[i % 5] = arr2[i % 5] + 1
        elif arr[i] == 1:
            for t2 in range(N, 0, -1):
                for p2 in range(1, N + 1):
                    x2 = N + 1
                    while x2 > 0:
                        x2 = math.floor(x2 / 2)
                        arr2[i % 5] = arr2[i % 5] + 1
        elif arr[i] == 2:
            for t3 in range(1, N + 1):
                x3 = t3 + 1
                for p3 in range(0, pow(t3, 2)):
                    arr2[i % 5] = arr2[i % 5] + 1
    after = datetime.datetime.now()
    diff = after - before
    return diff.total_seconds()


different_n_values = [1, 5, 10, 25, 50, 75, 100, 150, 200, 250]
for n in different_n_values:
    fill0 = my_func(N=n, is_random=False, fill=0)
    print(f"Case: best Size:{n} Elapsed Time: {fill0}")
    fill2 = my_func(N=n, is_random=False, fill=2)
    print(f"Case: worst Size:{n} Elapsed Time: {fill2}")
    random1 = my_func(N=n, is_random=True)
    random2 = my_func(N=n, is_random=True)
    random3 = my_func(N=n, is_random=True)
    random_avg = round((random1 + random2 + random3) / 3, 6)
    print(f"Case: average Size:{n} Elapsed Time: {random_avg}")
