import random
import time
import sys

def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def generate_random_array(size, lower_bound, upper_bound):
    return [random.randint(lower_bound, upper_bound) for _ in range(size)]

def bozo_sort(arr, verbose=False, max_iterations=10000):
    arr = arr.copy()
    iterations = 0
    while not is_sorted(arr):
        iterations += 1
        if iterations > max_iterations:
            raise RuntimeError(f"Sorting failed after {max_iterations} iterations")
            
        if verbose:
            print(f"Iteration {iterations}: {arr}")
        
        i = random.randint(0, len(arr) - 1)
        j = random.randint(0, len(arr) - 1)
        arr[i], arr[j] = arr[j], arr[i]
    
    if verbose:
        print(f"Final iteration {iterations}: {arr}")
    
    return arr, iterations

def tester(trials, a_size, lower_bound, upper_bound, max_iterations=100000):
    if trials <= 0 or a_size <= 0:
        raise ValueError("Trials and array size must be positive")
    if lower_bound >= upper_bound:
        raise ValueError("Upper bound must be greater than lower bound")

    times = []
    iterations_list = []
    failed_sorts = 0

    for i in range(trials):
        arr = generate_random_array(a_size, lower_bound, upper_bound)
        try:
            start = time.time()
            sorted_arr, iterations = bozo_sort(arr, max_iterations=max_iterations)
            end = time.time()
            
            if not is_sorted(sorted_arr):
                failed_sorts += 1
                continue
                
            times.append(end - start)
            iterations_list.append(iterations)
            
        except RuntimeError:
            failed_sorts += 1
            continue

    if not times:
        return "All sorting attempts failed"

    avg_time = sum(times) / len(times)
    avg_iterations = sum(iterations_list) / len(iterations_list)
    
    return {
        "total_time": sum(times),
        "average_time": avg_time,
        "average_iterations": avg_iterations,
        "successful_sorts": trials - failed_sorts,
        "failed_sorts": failed_sorts
    }

if __name__ == "__main__":
    size = 5
    lower_bound = 0
    upper_bound = 100
    trial_counts = [10, 100, 1000, 10000, 100000]
    
    print("\nBozoSort Performance Test Suite")
    print("=" * 50)
    print(f"Array Size: {size}")
    print(f"Value Range: [{lower_bound}, {upper_bound}]")
    print("=" * 50)
    
    total_suite_start = time.time()
    
    for trials in trial_counts:
        print(f"\nRunning {trials} trials...")
        test_start = time.time()
        results = tester(trials, size, lower_bound, upper_bound)
        test_end = time.time()
        
        print(f"\nResults for {trials} trials:")
        print("-" * 30)
        for key, value in results.items():
            print(f"{key}: {value}")
        print(f"Total test time: {test_end - test_start:.2f} seconds")
    
    total_suite_end = time.time()
    print("\n" + "=" * 50)
    print(f"Total suite execution time: {total_suite_end - total_suite_start:.2f} seconds")
