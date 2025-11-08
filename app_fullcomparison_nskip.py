import time
import random
import sys
from datetime import datetime

# Increase recursion limit for large datasets
sys.setrecursionlimit(100000)

class FullSortingComparator:
    def __init__(self):
        self.results = []
    
    # SELECTION SORT dengan progress indicator
    def selection_sort(self, arr):
        n = len(arr)
        for i in range(n):
            # Progress indicator untuk data besar
            if n > 10000 and i % 1000 == 0:
                progress = (i / n) * 100
                print(f"   Selection Sort progress: {progress:.1f}%", end='\r')
            
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr
    
    # BUBBLE SORT dengan optimisasi
    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n):
            # Progress indicator
            if n > 5000 and i % 500 == 0:
                progress = (i / n) * 100
                print(f"   Bubble Sort progress: {progress:.1f}%", end='\r')
            
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            # Jika tidak ada swap, array sudah sorted
            if not swapped:
                break
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
            print(f"   🔄 Menjalankan {algorithm_name}...")
            start_time = time.time()
            sorted_data = algorithm(test_data)
            end_time = time.time()
            
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            is_correct = self.verify_sorted(sorted_data)
            
            # Clear progress line
            print(' ' * 50, end='\r')
            
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
        print("🚀 MEMULAI PERBANDINGAN ALGORITMA SORTING - TANPA SKIP")
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
                # TIDAK ADA SKIP - semua algoritma dijalankan
                if size >= 10000 and name in ["Bubble Sort", "Selection Sort"]:
                    print(f"   ⏳ {name} mungkin membutuhkan waktu lama...")
                
                result = self.test_algorithm(algorithm, test_data, name, size)
                size_results.append(result)
                
                if result['status'] == 'Completed':
                    print(f"   ✅ {name}: {result['time_ms']:>12,.1f} ms")
                else:
                    print(f"   ❌ {name}: {result['status']}")
            
            all_results.extend(size_results)
            self.display_size_summary(size_results, size)
        
        return all_results
    
    def display_size_summary(self, results, data_size):
        """Display summary for a specific data size"""
        print(f"\n📈 RINGKASAN {data_size:,} DATA:")
        print("-" * 70)
        print(f"{'ALGORITMA':<15} {'WAKTU (ms)':<15} {'STATUS':<15} {'HASIL':<10}")
        print("-" * 70)
        
        for result in results:
            time_display = f"{result['time_ms']:,.1f} ms" if isinstance(result['time_ms'], (int, float)) else result['time_ms']
            status = result['status']
            result_icon = "✅" if result['is_correct'] else "❌"
            
            print(f"{result['algorithm']:<15} {str(time_display):<15} {status:<15} {result_icon:<10}")
    
    def display_comparison_table(self, all_results):
        """Display final comparison table - TANPA SKIP"""
        print(f"\n{'='*100}")
        print("📊 TABEL PERBANDINGAN AKHIR - SEMUA ALGORITMA DIJALANKAN")
        print(f"{'='*100}")
        
        # Organize results by data size
        results_by_size = {}
        for result in all_results:
            size = result['data_size']
            if size not in results_by_size:
                results_by_size[size] = []
            results_by_size[size].append(result)
        
        # Header
        header = f"{'DATA SIZE':<12} {'Selection Sort':<18} {'Bubble Sort':<18} {'Quick Sort':<18} {'Merge Sort':<18} {'Heap Sort':<18}"
        print(header)
        print("-" * 102)
        
        # Data rows - semua algoritma ditampilkan
        sizes = sorted(results_by_size.keys())
        for size in sizes:
            results = results_by_size[size]
            times = {r['algorithm']: r['time_ms'] for r in results}
            
            row = f"{size:<12,} "
            for algo in ["Selection Sort", "Bubble Sort", "Quick Sort", "Merge Sort", "Heap Sort"]:
                time_val = times.get(algo, 'N/A')
                if isinstance(time_val, (int, float)):
                    if time_val < 1000:
                        row += f"{time_val:>10.1f} ms   "
                    else:
                        row += f"{time_val:>10,.0f} ms   "
                else:
                    row += f"{str(time_val):>18} "
            print(row)
    
    def display_performance_analysis(self, all_results):
        """Display performance analysis and insights"""
        print(f"\n{'='*80}")
        print("🔍 ANALISIS PERFORMANCE DETAIL")
        print(f"{'='*80}")
        
        results_by_size = {}
        for result in all_results:
            size = result['data_size']
            if size not in results_by_size:
                results_by_size[size] = []
            results_by_size[size].append(result)
        
        for size in sorted(results_by_size.keys()):
            print(f"\n📈 ANALISIS UNTUK {size:,} DATA:")
            print("-" * 60)
            
            results = results_by_size[size]
            valid_results = [r for r in results if isinstance(r['time_ms'], (int, float))]
            
            if valid_results:
                fastest = min(valid_results, key=lambda x: x['time_ms'])
                slowest = max(valid_results, key=lambda x: x['time_ms'])
                
                print(f"⚡ Tercepat: {fastest['algorithm']} ({fastest['time_ms']:,.1f} ms)")
                print(f"🐢 Terlambat: {slowest['algorithm']} ({slowest['time_ms']:,.1f} ms)")
                
                if len(valid_results) > 1:
                    speed_ratio = slowest['time_ms'] / fastest['time_ms']
                    print(f"📏 Rasio Kecepatan: {speed_ratio:,.1f}x lebih cepat")
                    
                    # Tampilkan semua perbandingan
                    print(f"\n📊 PERBANDINGAN DETAIL:")
                    for result in valid_results:
                        ratio = result['time_ms'] / fastest['time_ms']
                        print(f"   {result['algorithm']:<15}: {result['time_ms']:>10,.1f} ms ({ratio:>5.1f}x lebih lambat)")
            
            print("\n📚 KOMPLEKSITAS ALGORITMA:")
            complexities = {
                "Selection Sort": "O(n²) - Quadratic",
                "Bubble Sort": "O(n²) - Quadratic", 
                "Quick Sort": "O(n log n) - Linearithmic (average)",
                "Merge Sort": "O(n log n) - Linearithmic", 
                "Heap Sort": "O(n log n) - Linearithmic"
            }
            for algo, comp in complexities.items():
                print(f"   {algo:<15}: {comp}")
    
    def save_results_to_file(self, all_results, filename="full_sorting_comparison.txt"):
        """Save results to a text file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("HASIL PERBANDINGAN LENGKAP ALGORITMA SORTING - TANPA SKIP\n")
            f.write("=" * 60 + "\n")
            f.write(f"Tanggal Test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            results_by_size = {}
            for result in all_results:
                size = result['data_size']
                if size not in results_by_size:
                    results_by_size[size] = []
                results_by_size[size].append(result)
            
            for size in sorted(results_by_size.keys()):
                f.write(f"\nDATA SIZE: {size:,}\n")
                f.write("-" * 50 + "\n")
                for result in results_by_size[size]:
                    time_display = f"{result['time_ms']:,.1f} ms" if isinstance(result['time_ms'], (int, float)) else result['time_ms']
                    status_icon = "✓" if result['is_correct'] else "✗"
                    f.write(f"{result['algorithm']:<15} : {time_display:<15} | {status_icon} {result['status']}\n")
        
        print(f"\n💾 Hasil lengkap disimpan dalam file: {filename}")

def main():
    """Main function to run the full comparison"""
    comparator = FullSortingComparator()
    
    # Data sizes to test
    data_sizes = [1000, 10000, 50000]
    
    print("🔬 PERBANDINGAN LENGKAP: SEMUA ALGORITMA DIJALANKAN")
    print("TIDAK ADA YANG DISKIP - termasuk Selection & Bubble Sort untuk 50K data!")
    print("=" * 80)
    
    # Warning untuk user
    print("\n⚠️  PERHATIAN: Test ini mungkin memakan waktu lama")
    print("   Terutama untuk Selection Sort dan Bubble Sort dengan 50,000 data")
    print("   Silakan tunggu dengan sabar...\n")
    
    # Run comparison
    all_results = comparator.run_comparison(data_sizes)
    
    # Display results
    comparator.display_comparison_table(all_results)
    comparator.display_performance_analysis(all_results)
    comparator.save_results_to_file(all_results)
    
    print(f"\n🎉 PERBANDINGAN LENGKAP SELESAI!")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💡 Insight: Algoritma O(n²) sangat tidak efisien untuk data besar!")

if __name__ == "__main__":
    main()