def fibonacci(qt: int):
    fibo = []
    fibo.append(1)
    last_fib = 2
    for num in range(0, qt-1):
        fib = last_fib + num
        fibo.append(fib)
        last_fib = fib
    return fibo
