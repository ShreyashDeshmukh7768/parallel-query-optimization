"""
pip install pandas matplotlib

Execution Instructions:
Step 1:
python data_generator.py

Step 2:
python main.py

Step 3 (optional):
python graph.py
"""
import os
import pandas as pd
from sequential import process_sequential
from parallel import process_parallel

def main():
    filename = "dataset.csv"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        print("Please run `python data_generator.py` first.")
        return

    # Check total dataset size
    print("Loading dataset to find its size...")
    df = pd.read_csv(filename)
    dataset_size = len(df)

    # 1. Sequential execution
    print("\nRunning Sequential Execution...")
    seq_result, seq_time, seq_rows = process_sequential(filename)
    
    # 2. Parallel execution
    print("Running Parallel Execution...")
    par_result, par_time, par_rows = process_parallel(filename)
    
    # Ensure correct types and indexes for comparison
    if seq_result is not None and par_result is not None:
        seq_result = seq_result.reset_index(drop=True)
        par_result = par_result.reset_index(drop=True)
        
        # Verify correctness: Check if row count and actual data match exactly
        results_match = seq_result.equals(par_result)
    else:
        results_match = False

    # 3. Print Final Summary properly formatted
    print("\n" + "="*50)
    print(f"Dataset Size: {dataset_size} rows\n")
    
    print(f"Sequential Execution Time: {seq_time:.4f} sec")
    print(f"Parallel Execution Time:   {par_time:.4f} sec\n")
    
    if par_time > 0:
        speedup = seq_time / par_time
        print(f"Speedup: {speedup:.2f}x\n")
    else:
        print("Speedup: N/A\n")
        
    print(f"Results Match: {results_match}")
    print("="*50)

if __name__ == "__main__":
    main()
