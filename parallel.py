import pandas as pd
import time
import multiprocessing as mp
import os
import math

def heavy_computation(row):
    """
    Simulates a CPU-intensive computational workload.
    Takes a row and performs repeated math calculations.
    """
    val = row['salary']
    for _ in range(150): # Iterate to burn CPU cycles
        val = (val * 1.01) - (val * 0.005)
    return val

def process_chunk(chunk):
    """
    Function to process a single data chunk in a separate process.
    """
    if chunk.empty:
        return chunk
        
    # Filter dataset
    filtered = chunk[chunk['salary'] > 50000].copy()
    
    # -------------------------------------------------------------
    # Apply CPU-intensive heavy computation in parallel worker
    # -------------------------------------------------------------
    filtered['computed_value'] = filtered.apply(heavy_computation, axis=1)
    
    # Sort chunk by age and id
    sorted_chunk = filtered.sort_values(by=['age', 'id'])
    return sorted_chunk

def process_parallel(filename="dataset.csv", num_cores=4):
    """
    Simulates parallel database query processing with heavy operations.
    Sets default processes to 4.
    """
    start_time = time.time()
    
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None, 0, 0
        
    if df.empty:
        return df, time.time() - start_time, 0
    
    # Split dataset into chunks based on number of available cores
    chunk_size = math.ceil(len(df) / num_cores)
    chunks = [df.iloc[i : i + chunk_size] for i in range(0, len(df), chunk_size)]
    
    # Use multiprocessing.Pool safely
    with mp.Pool(processes=num_cores) as pool:
        # Map chunks to the worker function safely
        results = pool.map(process_chunk, chunks)
        
    # Merge all chunked results
    if results:
        merged_df = pd.concat(results)
        # Final sort since chunks were processed independently
        final_sorted_df = merged_df.sort_values(by=['age', 'id']).reset_index(drop=True)
    else:
        final_sorted_df = pd.DataFrame(columns=df.columns)
        
    end_time = time.time()
    execution_time = end_time - start_time
    
    return final_sorted_df, execution_time, len(final_sorted_df)

if __name__ == "__main__":
    # Ensure safe multiprocessing execution block
    result, exec_time, rows = process_parallel()
    if result is not None:
        print(f"Parallel Execution Time: {exec_time:.4f} sec | Rows processed: {rows}")
