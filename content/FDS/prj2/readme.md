### README.md

# Project 2: A+B with Binary Search Trees

This project implements an efficient solution to the "Two Sum" problem in the context of two Binary Search Trees (BSTs). The program constructs BSTs from input data, performs iterative pre-order traversals, and identifies unique pairs $(A, B)$ such that $A + B = N$ using binary search on sorted keys.

## 1. Directory Structure
```text
.
├── main.c              # Source code
├── run.sh              # Automation script for macOS/Linux
├── run.bat             # Automation script for Windows
├── test1.in ~ test7.in # Input test cases
└── output/             # Folder where generated results (.out) will be stored
```

## 2. Compilation and Execution

### Option A: Using Automation Scripts
The project includes scripts to compile and batch-run all test cases automatically.

*   **For macOS/Linux:**
    1. Open your terminal in the project directory.
    2. Grant execution permission: `chmod +x run.sh`
    3. Execute the script: `./run.sh`
*   **For Windows:**
    1. Simply double-click `run.bat` or run it in the Command Prompt (CMD).

The scripts will automatically compile your `main.c`, create an `output/` folder, and generate the corresponding result files (`output/test1.out` ~ `output/test7.out`).

---

### Option B: Manual Execution (Emergency/Debugging)
If the scripts fail or you need to test a specific file manually, follow these steps:

1. **Compile the program:**
   ```bash
   gcc main.c -o main -O2 -Wall
   ```
   *(On Windows, you might prefer `gcc main.c -o main.exe -O2 -Wall`)*

2. **Run the program with a specific input file:**
   *   **macOS/Linux:**
       ```bash
       ./main < test1.in > output/test1.out
       ```
   *   **Windows (Command Prompt):**
       ```cmd
       main.exe < test1.in > output\test1.out
       ```

3. **Check the results:**
   The output file will be saved in the `output/` folder. You can open it with any text editor to verify the correctness.

---

## 3. Testing Methodology (Summary for Chapter 3)
Our testing strategy ensures full compliance with the rubric requirements:

*   **Comprehensive Tests (Test 1, 2):** Covers general cases with multiple solutions and scenarios with no solutions.
*   **Smallest Scale (Test 3):** Tests the program's boundary behavior with single-node trees.
*   **Project 2 Logic (Test 4):** Ensures correct deduplication of $A$ in $T1$ while preserving independent symmetric pairs (e.g., $1+2$ and $2+1$).
*   **Extreme Structure (Test 5):** Uses a left-skewed (linked-list-like) tree to verify that the **iterative stack traversal** avoids `Stack Overflow` errors common in recursive solutions.
*   **Extreme Values (Test 6, 7):** Validates the use of `long long` for handling large boundaries ($\pm 2 \times 10^9$) and correct handling of cross-sign arithmetic (Zero-sum).

---
*Note: Ensure you have `gcc` installed in your system PATH before running the scripts.*

### 4. Performance Analysis (Additional)
The project includes an empirical performance analysis script `measure_time.py`. 
* **Prerequisites**: `matplotlib` (`pip install matplotlib`).
* **Usage**:
    1. Compile the program: `gcc main.c -o main -O2`
    2. Run the measurement script: `python3 measure_time.py`
    3. This will generate a **`time_plot.png`** in your directory, visualizing the execution time across different input scales (from $10^2$ to $2 \times 10^5$ nodes). This plot provides empirical evidence that the algorithm performs with high efficiency, consistent with its $O(N \log N)$ theoretical complexity.
