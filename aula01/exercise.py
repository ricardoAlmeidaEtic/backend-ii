from time import perf_counter

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    num = 5
    start_time = perf_counter()
    print(f"Factorial of {num} is:", factorial(num))
    end_time = perf_counter()
    print(f"Time taken for calculation: {end_time - start_time:.6f} seconds")
