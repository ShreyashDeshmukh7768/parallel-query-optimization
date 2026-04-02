import pandas as pd
import time

def heavy_computation(row):
    """
    Simulates a CPU-intensive computational workload.
    Takes a row and performs repeated math calculations.
    """
    val = row['salary']
    for _ in range(150): # Iterate to burn CPU cycles
        val = (val * 1.01) - (val * 0.005)
    return val

def process_sequential(filename="dataset.csv"):
    """
    Simulates sequential database query processing with heavy operations.
    """
    start_time = time.time()
    
    # Load dataset using pandas
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None, 0, 0
    
    # Apply filter: salary > 50000
    # Use .copy() to avoid SettingWithCopy warning when adding a new column
    filtered_df = df[df['salary'] > 50000].copy()
    
    # -------------------------------------------------------------
    # Appling CPU-intensive heavy computation sequentially
    # -------------------------------------------------------------
    filtered_df['computed_value'] = filtered_df.apply(heavy_computation, axis=1)
    
    # Sort by age (and id to ensure stable and consistent sorting)
    sorted_df = filtered_df.sort_values(by=['age', 'id'])
    
    # Record end time
    end_time = time.time()
    execution_time = end_time - start_time
    
    return sorted_df, execution_time, len(sorted_df)

if __name__ == "__main__":
    result, exec_time, rows = process_sequential()
    if result is not None:
        print(f"Sequential Execution Time: {exec_time:.4f} sec | Rows processed: {rows}")
