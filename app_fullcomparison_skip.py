import time
import random
import sys
from datetime import datetime

# Increase recursion limit for large datasets in Quick Sort
sys.setrecursionlimit(100000)

class SortingComparator:
    def __init__(self):
        self.results = []
    
    # SELECTION SORT
    def selection_sort(self, arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr
    
    # BUBBLE SORT  
    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    # QUICK SORT
    def quick_sort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self.quick_sort(left) + middle + self.quick_sort(right)
    
    # MERGE SORT
    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        
        left = self.merge_sort(left)
        right = self.merge_sort(right)
        
        return self.merge(left, right)
    
    def merge(self, left, right):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    # HEAP SORT
    def heap_sort(self, arr):
        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n and arr[left] > arr[largest]:
                largest = left
                
            if right < n and arr[right] > arr[largest]:
                largest = right
                
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)
        
        n = len(arr)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)
        
        # Extract elements from heap
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            heapify(arr, i, 0)
        
        return arr
    
    def generate_test_data(self, size):
        """Generate random test data"""
        return [random.randint(1, 1000000) for _ in range(size)]
    
    def verify_sorted(self, arr):
        """Verify if array is correctly sorted"""
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    
    def test_algorithm(self, algorithm, data, algorithm_name, data_size):
        """Test a single algorithm and return results"""
        test_data = data.copy()
        
        try:
            start_time = time.time()
            sorted_data = algorithm(test_data)
            end_time = time.time()
            
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            is_correct = self.verify_sorted(sorted_data)
            
            return {
                'algorithm': algorithm_name,
                'time_ms': round(execution_time, 2),
                'data_size': data_size,
                'is_correct': is_correct,
                'status': 'Completed'
            }
            
        except Exception as e:
            return {
                'algorithm': algorithm_name,
                'time_ms': 'Error',
                'data_size': data_size,
                'is_correct': False,
                'status': f'Error: {str(e)}'
            }
    
    def run_comparison(self, data_sizes=[1000, 10000, 50000]):
        """Run comparison for all algorithms on given data sizes"""
        print("🚀 MEMULAI PERBANDINGAN ALGORITMA SORTING")
        print("=" * 80)
        
        all_results = []
        
        for size in data_sizes:
            print(f"\n📊 MENGUJI DENGAN {size:,} DATA...")
            print("-" * 60)
            
            # Generate test data once for consistent comparison
            test_data = self.generate_test_data(size)
            
            algorithms = [
                (self.selection_sort, "Selection Sort"),
                (self.bubble_sort, "Bubble Sort"),
                (self.quick_sort, "Quick Sort"),
                (self.merge_sort, "Merge Sort"),
                (self.heap_sort, "Heap Sort")
            ]
            
            size_results = []
            
            for algorithm, name in algorithms:
                # Skip slow algorithms for large datasets
                if size >= 10000 and name in ["Bubble Sort", "Selection Sort"]:
                    result = {
                        'algorithm': name,
                        'time_ms': 'Skipped',
                        'data_size': size,
                        'is_correct': True,
                        'status': 'Skipped (too slow)'
                    }
                    size_results.append(result)
                    print(f"⏭️  {name}: Skipped (terlalu lambat untuk data besar)")
                    continue
                
                print(f"🔄 Menjalankan {name}...")
                result = self.test_algorithm(algorithm, test_data, name, size)
                size_results.append(result)
                
                if result['status'] == 'Completed':
                    print(f"✅ {name}: {result['time_ms']:>8} ms")
                else:
                    print(f"❌ {name}: {result['status']}")
            
            all_results.extend(size_results)
            self.display_size_summary(size_results, size)
        
        return all_results
    
    def display_size_summary(self, results, data_size):
        """Display summary for a specific data size"""
        print(f"\n📈 RINGKASAN {data_size:,} DATA:")
        print("-" * 70)
        print(f"{'ALGORITMA':<15} {'WAKTU (ms)':<12} {'STATUS':<20} {'HASIL':<10}")
        print("-" * 70)
        
        for result in results:
            time_display = f"{result['time_ms']:,}" if isinstance(result['time_ms'], (int, float)) else result['time_ms']
            status = result['status']
            result_icon = "✅" if result['is_correct'] else "❌"
            
            print(f"{result['algorithm']:<15} {str(time_display):<12} {status:<20} {result_icon:<10}")
    
    def display_comparison_table(self, all_results):
        """Display final comparison table"""
        print(f"\n{'='*80}")
        print("📊 TABEL PERBANDINGAN AKHIR")
        print(f"{'='*80}")
        
        # Organize results by data size
        results_by_size = {}
        for result in all_results:
            size = result['data_size']
            if size not in results_by_size:
                results_by_size[size] = []
            results_by_size[size].append(result)
        
        # Header
        header = f"{'DATA SIZE':<12} {'Selection Sort':<15} {'Bubble Sort':<15} {'Quick Sort':<15} {'Merge Sort':<15} {'Heap Sort':<15}"
        print(header)
        print("-" * 87)
        
        # Data rows
        sizes = sorted(results_by_size.keys())
        for size in sizes:
            results = results_by_size[size]
            times = {r['algorithm']: r['time_ms'] for r in results}
            
            row = f"{size:<12,} "
            for algo in ["Selection Sort", "Bubble Sort", "Quick Sort", "Merge Sort", "Heap Sort"]:
                time_val = times.get(algo, 'N/A')
                if isinstance(time_val, (int, float)):
                    row += f"{time_val:>13,.1f} ms "
                else:
                    row += f"{str(time_val):>15} "
            print(row)
    
    def display_performance_analysis(self, all_results):
        """Display performance analysis and insights"""
        print(f"\n{'='*80}")
        print("🔍 ANALISIS PERFORMANCE")
        print(f"{'='*80}")
        
        results_by_size = {}
        for result in all_results:
            size = result['data_size']
            if size not in results_by_size:
                results_by_size[size] = []
            results_by_size[size].append(result)
        
        for size in sorted(results_by_size.keys()):
            print(f"\n📈 ANALISIS UNTUK {size:,} DATA:")
            print("-" * 50)
            
            results = results_by_size[size]
            valid_results = [r for r in results if isinstance(r['time_ms'], (int, float))]
            
            if valid_results:
                fastest = min(valid_results, key=lambda x: x['time_ms'])
                slowest = max(valid_results, key=lambda x: x['time_ms'])
                
                print(f"⚡ Tercepat: {fastest['algorithm']} ({fastest['time_ms']:,} ms)")
                print(f"🐢 Terlambat: {slowest['algorithm']} ({slowest['time_ms']:,} ms)")
                
                if len(valid_results) > 1:
                    speed_ratio = slowest['time_ms'] / fastest['time_ms']
                    print(f"📏 Rasio Kecepatan: {speed_ratio:.1f}x lebih cepat")
            
            # Complexity analysis
            print("\n📚 KOMPLEKSITAS ALGORITMA:")
            print("Selection Sort: O(n²) - Quadratic")
            print("Bubble Sort:    O(n²) - Quadratic") 
            print("Quick Sort:     O(n log n) - Linearithmic (average case)")
            print("Merge Sort:     O(n log n) - Linearithmic")
            print("Heap Sort:      O(n log n) - Linearithmic")
    
    def save_results_to_file(self, all_results, filename="sorting_comparison_results.txt"):
        """Save results to a text file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("HASIL PERBANDINGAN ALGORITMA SORTING\n")
            f.write("=" * 50 + "\n")
            f.write(f"Tanggal Test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            results_by_size = {}
            for result in all_results:
                size = result['data_size']
                if size not in results_by_size:
                    results_by_size[size] = []
                results_by_size[size].append(result)
            
            for size in sorted(results_by_size.keys()):
                f.write(f"\nDATA SIZE: {size:,}\n")
                f.write("-" * 40 + "\n")
                for result in results_by_size[size]:
                    time_display = f"{result['time_ms']:,} ms" if isinstance(result['time_ms'], (int, float)) else result['time_ms']
                    f.write(f"{result['algorithm']:<15} : {time_display:<15} | {result['status']}\n")
        
        print(f"\n💾 Hasil disimpan dalam file: {filename}")

def main():
    """Main function to run the comparison"""
    comparator = SortingComparator()
    
    # Data sizes to test
    data_sizes = [1000, 10000, 50000]
    
    print("🔬 PERBANDINGAN SELECTION SORT vs ALGORITMA LAIN")
    print("Ukuran data: 1,000 | 10,000 | 50,000")
    print("=" * 80)
    
    # Run comparison
    all_results = comparator.run_comparison(data_sizes)
    
    # Display results
    comparator.display_comparison_table(all_results)
    comparator.display_performance_analysis(all_results)
    comparator.save_results_to_file(all_results)
    
    print(f"\n🎉 PERBANDINGAN SELESAI!")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()