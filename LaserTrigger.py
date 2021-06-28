import time, random


def shoot(n, r):
    st = time.time()
    r = 1 / r
    for i in range(n):
        time.sleep(r)
    end = time.time() - st
    print('Time taken within shoot(): ', str(end)[:6], 's')
    print('Expected rep rate: ' + str(1/r) + ' Hz, actual rep rate: ' + str(1/ (end / n))[:5] + '\n')

    return True
