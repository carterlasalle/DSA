import random
import time

def binary_search_recursive(arr, target, low, high):
    if low > high:
        return -1, 1  # Element not found, 1 step taken
    
    mid = (low + high) // 2
    steps = 1
    
    if arr[mid] == target:
        return mid, steps
    elif arr[mid] > target:
        result, more_steps = binary_search_recursive(arr, target, low, mid - 1)
        return result, steps + more_steps
    else:
        result, more_steps = binary_search_recursive(arr, target, mid + 1, high)
        return result, steps + more_steps

def ternary_search(arr, target):
    def ternary_search_recursive(low, high):
        if low > high:
            return -1, 1  # Element not found, 1 step taken
        
        third = (high - low) // 3
        mid1 = low + third
        mid2 = high - third
        steps = 1
        
        if arr[mid1] == target:
            return mid1, steps
        if arr[mid2] == target:
            return mid2, steps
        
        if target < arr[mid1]:
            result, more_steps = ternary_search_recursive(low, mid1 - 1)
        elif target > arr[mid2]:
            result, more_steps = ternary_search_recursive(mid2 + 1, high)
        else:
            result, more_steps = ternary_search_recursive(mid1 + 1, mid2 - 1)
        
        return result, steps + more_steps
    
    return ternary_search_recursive(0, len(arr) - 1)

def compare_search_algorithms(arr_size=1000, num_runs=10):
    arr = sorted(random.sample(range(arr_size * 10), arr_size))
    
    binary_times = []
    binary_steps = []
    ternary_times = []
    ternary_steps = []
    
    for _ in range(num_runs):
        target = random.choice(arr)
        
        # Binary Search
        start = time.time()
        _, steps = binary_search_recursive(arr, target, 0, len(arr) - 1)
        end = time.time()
        binary_times.append(end - start)
        binary_steps.append(steps)
        
        # Ternary Search
        start = time.time()
        _, steps = ternary_search(arr, target)
        end = time.time()
        ternary_times.append(end - start)
        ternary_steps.append(steps)
    
    print(f"Average Binary Search Time: {sum(binary_times) / num_runs:.6f} seconds")
    print(f"Average Binary Search Steps: {sum(binary_steps) / num_runs:.2f}")
    print(f"Average Ternary Search Time: {sum(ternary_times) / num_runs:.6f} seconds")
    print(f"Average Ternary Search Steps: {sum(ternary_steps) / num_runs:.2f}")

# Run the comparison
compare_search_algorithms()