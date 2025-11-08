# MatplotlibExample.py
import os
import math
import matplotlib.pyplot as plt

# === Jika kamu mengganti nama file (disarankan) ===
from app_fullcomparison_nskip import FullSortingComparator

# === Jika TIDAK mengganti nama file, gunakan import alternatif ini (hapus 3 baris import di atas):
# import importlib.machinery, importlib.util
# loader = importlib.machinery.SourceFileLoader("nskip", "app-fullcomparison-nskip.py")
# spec = importlib.util.spec_from_loader(loader.name, loader)
# nskip = importlib.util.module_from_spec(spec)
# loader.exec_module(nskip)
# FullSortingComparator = nskip.FullSortingComparator
# ===================================================

def main():
    # Siapkan output folder
    os.makedirs("results", exist_ok=True)

    # Jalankan benchmark
    comparator = FullSortingComparator()

    # Sesuaikan ukuran data agar demo grafik tidak terlalu lama.
    # Jika tetap ingin 50_000, siap-siap lama pada Bubble/Selection.
    data_sizes = [1_000, 10_000, 50_000]
    all_results = comparator.run_comparison(data_sizes)

    # --- Susun data untuk plotting ---
    # Bentuk: {size: {algo: time_ms}}
    results_by_size = {}
    for r in all_results:
        size = r["data_size"]
        algo = r["algorithm"]
        t    = r["time_ms"]
        results_by_size.setdefault(size, {})[algo] = t

    algorithms = ["Selection Sort", "Bubble Sort", "Quick Sort", "Merge Sort", "Heap Sort"]
    sizes = sorted(results_by_size.keys())

    # Siapkan matriks waktu (ms). Jika ada 'Error', jadikan NaN agar tidak mematahkan plot.
    series = {algo: [] for algo in algorithms}
    for s in sizes:
        row = results_by_size[s]
        for algo in algorithms:
            val = row.get(algo, float("nan"))
            if not isinstance(val, (int, float)):
                val = float("nan")
            series[algo].append(val)

    # --- Plot 1: Line chart (log scale) ---
    plt.figure(figsize=(10, 6))
    for algo in algorithms:
        plt.plot(sizes, series[algo], marker="o", label=algo)
    plt.title("Perbandingan Waktu Eksekusi Sorting (ms) — log scale")
    plt.xlabel("Ukuran Data (n)")
    plt.ylabel("Waktu (ms)")
    plt.yscale("log")  # Perbedaan skala jadi lebih terbaca
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.legend()
    line_path = os.path.join("results", "sorting_comparison_line.png")
    plt.savefig(line_path, dpi=150, bbox_inches="tight")
    plt.close()

    # --- Plot 2: Grouped bar chart (log scale) ---
    plt.figure(figsize=(12, 6))
    x = range(len(sizes))
    width = 0.15
    for i, algo in enumerate(algorithms):
        offsets = [xi + (i - len(algorithms)/2)*width + width/2 for xi in x]
        plt.bar(offsets, series[algo], width=width, label=algo)
    plt.title("Perbandingan Waktu Eksekusi Sorting (ms) — Grouped Bars (log scale)")
    plt.xlabel("Ukuran Data (n)")
    plt.ylabel("Waktu (ms)")
    plt.yscale("log")
    plt.xticks(list(x), [f"{s:,}" for s in sizes])
    plt.grid(True, which="both", axis="y", linestyle="--", alpha=0.4)
    plt.legend()
    bar_path = os.path.join("results", "sorting_comparison_bars.png")
    plt.savefig(bar_path, dpi=150, bbox_inches="tight")
    plt.close()

    print("✅ Grafik tersimpan:")
    print(f" - {line_path}")
    print(f" - {bar_path}")
    print("Tip: Gunakan skala log agar gap O(n²) vs O(n log n) mudah terlihat.")

if __name__ == "__main__":
    main()
