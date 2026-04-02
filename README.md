# 🚀 Parallel Query Optimization Dashboard

## 🧠 Overview

This project demonstrates how the same data-processing task behaves under **sequential** and **parallel execution**. It compares their performance and shows how parallel processing can significantly reduce execution time for computationally intensive workloads.

The system processes a large dataset, applies query-like operations, and measures execution time to evaluate performance differences.

---

## ⚙️ How It Works

### 1️⃣ Data Preparation

* A large dataset is generated (hundreds of thousands to millions of rows)
* Each row contains structured attributes such as:

  * ID
  * Age
  * Salary
  * Department
* The dataset is loaded into memory for processing

---

### 2️⃣ Query Simulation

A query-like operation is applied to the dataset:

* Filter rows based on a condition (e.g., salary threshold)
* Perform CPU-intensive computation on each row
* Sort the processed results

This simulates real-world data processing workflows.

---

## 🔹 Sequential Execution

* The entire dataset is processed step-by-step using a **single process**
* Operations are performed in order:

  1. Filtering
  2. Computation
  3. Sorting

### Characteristics:

* Uses only one CPU core
* Execution time increases with dataset size and workload
* No parallelism involved

---

## 🔹 Parallel Execution

Parallel execution distributes the workload across multiple processes.

### Step 1: Data Splitting

* Dataset is divided into multiple chunks
* Each chunk is assigned to a separate process

### Step 2: Concurrent Processing

Each process performs:

* Filtering
* Computation
* Local sorting

### Step 3: Result Merging

* Processed chunks are combined
* Final sorting ensures correct global order

### Characteristics:

* Utilizes multiple CPU cores
* Reduces overall execution time
* Improves performance for heavy workloads

---

## ⚡ Performance Comparison

The system measures:

* Sequential execution time
* Parallel execution time

### Speedup Formula:

[
Speedup = \frac{Sequential\ Time}{Parallel\ Time}
]

---

## 🧠 Key Insight

* **Sequential execution** processes data linearly using one core
* **Parallel execution** divides the workload and processes data simultaneously

---

## ⚠️ Important Behavior

* For **lightweight operations**:

  * Parallel execution may be slower due to overhead
  * Overhead includes process creation, communication, and merging

* For **CPU-intensive workloads**:

  * Parallel execution significantly improves performance
  * Better utilization of available CPU cores

---

## 📊 Output Example

```
Dataset Size: 500000 rows

Sequential Execution Time: 1.30 sec
Parallel Execution Time:   0.73 sec

Speedup: 1.78x

Results Match: True
```

---

## 🎯 Conclusion

This system highlights how distributing workloads across multiple processes can improve performance. While parallel execution introduces overhead, it becomes highly efficient when handling large datasets and computationally intensive operations, making it a powerful approach for optimizing data processing tasks.

---
