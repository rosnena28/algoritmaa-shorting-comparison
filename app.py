from flask import Flask, render_template, request, jsonify
import time
import random
import csv
import io
import os
from datetime import datetime

app = Flask(__name__)

# Implementasi algoritma sorting manual

def bubble_sort(arr):
    """Bubble Sort implementation"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def selection_sort(arr):
    """Selection Sort implementation"""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def quick_sort(arr):
    """Quick Sort implementation"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    """Merge Sort implementation"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    left = merge_sort(left)
    right = merge_sort(right)
    
    return merge(left, right)

def merge(left, right):
    """Merge function for merge sort"""
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

def test_sorting_algorithm(algorithm, data, algorithm_name):
    """Test sorting algorithm and return execution time"""
    # Copy data to avoid modifying original
    test_data = data.copy()
    
    # Measure execution time
    start_time = time.time()
    sorted_data = algorithm(test_data)
    end_time = time.time()
    
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # Verify sorting is correct
    is_sorted = all(sorted_data[i] <= sorted_data[i + 1] for i in range(len(sorted_data) - 1))
    
    return {
        'algorithm': algorithm_name,
        'time_ms': round(execution_time, 2),
        'data_size': len(data),
        'is_correct': is_sorted
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_data', methods=['POST'])
def generate_data():
    """Generate random data for testing"""
    data_size = int(request.json['size'])
    
    # Generate random data
    random_data = [random.randint(1, 1000000) for _ in range(data_size)]
    
    return jsonify({
        'message': f'Generated {data_size} random numbers',
        'data_size': data_size,
        'sample_data': random_data[:10]  # Return first 10 for preview
    })

@app.route('/upload_data', methods=['POST'])
def upload_data():
    """Handle CSV file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Please upload a CSV file'}), 400
    
    try:
        # Read CSV file
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.reader(stream)
        
        # Extract data (assuming first column contains numbers)
        data = []
        for i, row in enumerate(csv_reader):
            if i == 0:  # Skip header
                continue
            if row:  # Check if row is not empty
                try:
                    data.append(int(float(row[0])))  # Convert to int
                except (ValueError, IndexError):
                    continue
        
        if not data:
            return jsonify({'error': 'No valid numeric data found in CSV'}), 400
        
        return jsonify({
            'message': f'Successfully loaded {len(data)} numbers from CSV',
            'data_size': len(data),
            'sample_data': data[:10]  # Return first 10 for preview
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/run_comparison', methods=['POST'])
def run_comparison():
    """Run sorting algorithms comparison"""
    data_size = int(request.json['data_size'])
    use_uploaded_data = request.json.get('use_uploaded_data', False)
    uploaded_data = request.json.get('uploaded_data', [])
    
    # Prepare test data
    if use_uploaded_data and uploaded_data:
        test_data = uploaded_data
    else:
        test_data = [random.randint(1, 1000000) for _ in range(data_size)]
    
    # Define algorithms to test
    algorithms = [
        (bubble_sort, "Bubble Sort"),
        (selection_sort, "Selection Sort"), 
        (quick_sort, "Quick Sort"),
        (merge_sort, "Merge Sort")
    ]
    
    results = []
    
    # Test each algorithm
    for algorithm, name in algorithms:
        if data_size > 10000 and name == "Bubble Sort":
            # Skip bubble sort for large datasets (too slow)
            results.append({
                'algorithm': name,
                'time_ms': 'Timeout',
                'data_size': data_size,
                'is_correct': 'Skipped'
            })
            continue
            
        result = test_sorting_algorithm(algorithm, test_data, name)
        results.append(result)
    
    return jsonify({
        'results': results,
        'data_size': data_size,
        'test_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/run_multiple_tests', methods=['POST'])
def run_multiple_tests():
    """Run tests for multiple data sizes"""
    test_sizes = [1000, 10000, 50000]
    all_results = []
    
    for size in test_sizes:
        # Generate test data for this size
        test_data = [random.randint(1, 1000000) for _ in range(size)]
        
        algorithms = [
            (quick_sort, "Quick Sort"),
            (merge_sort, "Merge Sort"),
            (selection_sort, "Selection Sort")
        ]
        
        size_results = {'data_size': size, 'results': []}
        
        for algorithm, name in algorithms:
            if size == 50000 and name == "Selection Sort":
                # Skip selection sort for 50k (too slow)
                size_results['results'].append({
                    'algorithm': name,
                    'time_ms': 'Timeout',
                    'is_correct': 'Skipped'
                })
                continue
                
            result = test_sorting_algorithm(algorithm, test_data, name)
            size_results['results'].append(result)
        
        all_results.append(size_results)
    
    return jsonify({
        'multiple_results': all_results,
        'test_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)