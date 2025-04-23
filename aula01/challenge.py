from time import perf_counter

def bubblesort(arr):
    start_time = perf_counter()
    print("Unsorted array:", arr)
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True

        if not swapped:
            end_time = perf_counter()
            print(f"Time taken for sorting: {end_time - start_time:.6f} seconds")
            print("Sorted array:", arr)
            return

if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    bubblesort(arr)
