import random

def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def bozo_sort(arr, verbose=False):
    arr = arr.copy()
    iterations = 0
    while not is_sorted(arr):
        iterations += 1
        if verbose:
            print(f"Iteration {iterations}: {arr}")
        
        i = random.randint(0, len(arr) - 1)
        j = random.randint(0, len(arr) - 1)
        arr[i], arr[j] = arr[j], arr[i]
    
    if verbose:
        print(f"Final iteration {iterations}: {arr}")
    
    return arr

if __name__ == "__main__":
    data = [3, 1, 4, 5, 2]
    print("Original array:", data)
    sorted_data = bozo_sort(data, verbose=True)
    print("Sorted array:", sorted_data)


"""
def generate_random_array(max_length, max_value=100):
    '''
    Generate a random array with a random length up to max_length,
    containing random integers from 0 to max_value.
    '''
    length = random.randint(1, max_length)
    return [random.randint(0, max_value) for _ in range(length)]

# Example usage
max_length = 10
random_array = generate_random_array(max_length)
print("Random array:", random_array)
print("Sorted random array:", bozo_sort(random_array))
"""

