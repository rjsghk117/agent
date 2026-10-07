def fibonacci_sequence(n):
    fib_sequence = [1, 1]
    while len(fib_sequence) < n:
        next_value = fib_sequence[-1] + fib_sequence[-2]
        fib_sequence.append(next_value)
    return fib_sequence

# 피보나치 수열의 처음 10개 항 출력
print(fibonacci_sequence(10))