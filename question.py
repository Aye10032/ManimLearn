import math


def basel(n: int) -> float:
    _sum = 0.0
    for i in range(1, n + 1):
        _sum += 1 / (i ** 2)

    return _sum


reference = math.pi ** 2 / 6
result = basel(100000)
print(f'Q1: approximation={result}, loss={reference - result}')


def cal_sqrt(n: int, depth: int) -> float:
    if depth == 1:
        return n + 1
    else:
        return (n + cal_sqrt(n + 1, depth - 1)) ** 0.5


result = cal_sqrt(1, 100)
print(f'Q2: {result}')
