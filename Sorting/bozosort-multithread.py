import random
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import threading
import signal
from collections import deque
import datetime
import multiprocessing

class ProgressTracker:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.successful = 0
        self.failed = 0
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.completion_times = deque(maxlen=50)  # Track last 50 trials
        self.last_update_time = self.start_time
        
    def increment(self, failed=False):
        with self.lock:
            current_time = time.time()
            if self.current > 0:  # Skip first trial
                self.completion_times.append(current_time - self.last_update_time)
            self.last_update_time = current_time
            
            self.current += 1
            if failed:
                self.failed += 1
            else:
                self.successful += 1
            self._print_progress()
    
    def _calculate_eta(self):
        if len(self.completion_times) < 5:  # Need some data for accurate prediction
            return "calculating..."
        
        # Use exponential moving average of recent completion times
        alpha = 0.3  # Smoothing factor
        avg_time = sum(self.completion_times) / len(self.completion_times)
        if len(self.completion_times) > 1:
            recent_time = self.completion_times[-1]
            avg_time = alpha * recent_time + (1 - alpha) * avg_time
        
        remaining_trials = self.total - self.current
        estimated_seconds = remaining_trials * avg_time
        
        # Format time remaining instead of absolute ETA
        if estimated_seconds < 60:
            return f"{estimated_seconds:.0f}s"
        elif estimated_seconds < 3600:
            minutes = estimated_seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = estimated_seconds / 3600
            return f"{hours:.1f}h"
    
    def _print_progress(self):
        bar_length = 30
        filled_length = int(bar_length * self.current / self.total)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        percent = self.current / self.total * 100
        eta = self._calculate_eta()
        
        sys.stdout.write(
            f'\r[{bar}] {self.current}/{self.total} {percent:.1f}% '
            f'({self.successful}/{self.current} successful) '
            f'Remaining: {eta}'
        )
        sys.stdout.flush()

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

def run_single_trial(args):
    a_size, lower_bound, upper_bound, max_iterations, progress_tracker = args
    arr = generate_random_array(a_size, lower_bound, upper_bound)
    try:
        start = time.time()
        sorted_arr, iterations = bozo_sort(arr, max_iterations=max_iterations)
        end = time.time()
        
        if not is_sorted(sorted_arr):
            progress_tracker.increment(failed=True)
            return None
            
        progress_tracker.increment(failed=False)
        return {
            "time": end - start,
            "iterations": iterations,
            "success": True
        }
        
    except RuntimeError:
        progress_tracker.increment(failed=True)
        return None

def parallel_tester(trials, a_size, lower_bound, upper_bound, max_iterations=100000, max_workers=None):
    if trials <= 0 or a_size <= 0:
        raise ValueError("Trials and array size must be positive")
    if lower_bound >= upper_bound:
        raise ValueError("Upper bound must be greater than lower bound")

    if max_workers is None:
        # Use number of CPU cores + 1 for optimal performance
        max_workers = min(multiprocessing.cpu_count() + 1, trials)

    progress_tracker = ProgressTracker(trials)
    args_list = [(a_size, lower_bound, upper_bound, max_iterations, progress_tracker)] * trials
    results = []
    
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = list(executor.map(run_single_trial, args_list))
            
            times = []
            iterations_list = []
            
            for result in futures:
                if result is not None:
                    times.append(result["time"])
                    iterations_list.append(result["iterations"])
        
        print()  # New line after progress bar
        
        if not times:
            return {
                "total_time": 0,
                "average_time": 0,
                "average_iterations": 0,
                "successful_sorts": 0,
                "failed_sorts": progress_tracker.failed,
                "status": "All sorting attempts failed"
            }

        return {
            "total_time": sum(times),
            "average_time": sum(times) / len(times),
            "average_iterations": sum(iterations_list) / len(iterations_list),
            "successful_sorts": progress_tracker.successful,
            "failed_sorts": progress_tracker.failed,
            "status": "Completed successfully"
        }
    
    except KeyboardInterrupt:
        print("\nCancelling... Please wait for current trials to complete...")
        return {
            "status": "Cancelled by user",
            "successful_sorts": progress_tracker.successful,
            "failed_sorts": progress_tracker.failed,
            "completed_trials": progress_tracker.current
        }

if __name__ == "__main__":
    size = 5
    lower_bound = 0
    upper_bound = 100
    trial_counts = [10, 100, 1000, 10000, 100000]
    
    print("\nMultithreaded BozoSort Performance Test Suite")
    print("=" * 50)
    print(f"Array Size: {size}")
    print(f"Value Range: [{lower_bound}, {upper_bound}]")
    print("=" * 50)
    
    try:
        total_suite_start = time.time()
        
        for trials in trial_counts:
            print(f"\nRunning {trials} trials...")
            test_start = time.time()
            results = parallel_tester(trials, size, lower_bound, upper_bound)
            test_end = time.time()
            
            print(f"\nResults for {trials} trials:")
            print("-" * 30)
            for key, value in results.items():
                print(f"{key}: {value}")
            print(f"Total test time: {test_end - test_start:.2f} seconds")
            
            if results["status"] == "Cancelled by user":
                break
        
        total_suite_end = time.time()
        print("\n" + "=" * 50)
        print(f"Total suite execution time: {total_suite_end - total_suite_start:.2f} seconds")
    
    except KeyboardInterrupt:
        print("\nTest suite interrupted by user")
        sys.exit(0)
