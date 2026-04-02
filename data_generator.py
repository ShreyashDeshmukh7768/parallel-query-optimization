"""
pip install pandas matplotlib

Execution Instruction:
Step 1:
python data_generator.py
"""
import pandas as pd
import random
import string

def generate_dataset(num_rows=1000000, filename="dataset.csv"):
    """
    Generates a CSV dataset with simulated employee records.
    """
    print(f"Generating dataset with {num_rows} rows...")
    
    departments = ["IT", "HR", "Sales", "Finance"]
    
    # Create random data
    data = {
        "id": range(1, num_rows + 1),
        "name": [''.join(random.choices(string.ascii_letters, k=8)) for _ in range(num_rows)],
        "age": [random.randint(18, 60) for _ in range(num_rows)],
        "salary": [random.randint(20000, 100000) for _ in range(num_rows)],
        "department": [random.choice(departments) for _ in range(num_rows)]
    }
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    
    print(f"Dataset successfully saved to {filename}")

if __name__ == "__main__":
    # You can change the number of rows here
    generate_dataset(num_rows=500000)
