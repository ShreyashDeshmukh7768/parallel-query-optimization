import os
import matplotlib.pyplot as plt
from parallel import process_parallel

def generate_graph():
    filename = "dataset.csv"
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        print("Please run `python data_generator.py` first.")
        return

    # Typical core counts to test
    cores_to_test = [1, 2, 4]
    
    # See if device has more cores to also plot
    max_cores = os.cpu_count() or 4
    if max_cores > 4 and max_cores not in cores_to_test:
        cores_to_test.append(max_cores)

    execution_times = []

    print("Running performance tests with different core counts...")
    for cores in cores_to_test:
        print(f"Testing parallel execution with {cores} core(s)...")
        _, exec_time, _ = process_parallel(filename, num_cores=cores)
        execution_times.append(exec_time)
        print(f"  Time taken: {exec_time:.4f} sec")

    # Generate X-Y line plot
    plt.figure(figsize=(8, 5))
    plt.plot(cores_to_test, execution_times, marker='o', linestyle='-', color='indigo', linewidth=2)
    
    plt.title('Parallel Execution Time vs. Number of Cores')
    plt.xlabel('Number of CPU Cores')
    plt.ylabel('Execution Time (seconds)')
    
    # Ensure graph ticks align perfectly with core numbers
    plt.xticks(cores_to_test)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Save Graph Image
    output_image = "performance_graph.png"
    plt.savefig(output_image, bbox_inches='tight')
    print(f"\nExecution graph successfully saved as '{output_image}'.")
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    generate_graph()
