---
draft: true
---

# Search Algorithm Performance Analysis

This project benchmarks the performance of **Sequential Search** and **Binary Search** algorithms (both Iterative and Recursive versions). The project investigates the worst-case scenario where the target element does not exist in the array.

## Key Features
- **Algorithm Implementations**: Four search variants implemented in C.
- **Robust Timing Engine**: Uses dynamic repetition factor ($K$) to average out hardware noise and timer inaccuracies, ensuring $\ge 10\%$ measurement precision.
- **Complexity Analysis**: Includes theoretical $\mathcal{O}(N)$ vs $\mathcal{O}(\log N)$ derivations and empirical hardware noise discussion.
- **Visualizations**: Python-generated plots comparing growth rates and demonstrating recursion overhead.

## File Structure
- `prj1.c`: Core source code for algorithms and performance testing.
- `output.txt`: Raw terminal output from the C program (data source).
- `huatu.py`: Python script to parse data, generate Excel reports, and create high-quality plots.
- `report.pdf`: The final compiled LaTeX report.
- `README.md`: Project documentation.
File Tree
```
document\
	report.pdf
code\
	readme.md
	prj1.c
	output.txt
	huatu.py

```
## How to Run
1. **Compile & Run (C)**:
```bash
   gcc -O0 prj1.c -o prj1
   ./prj1 > output.txt
```

2.**Process Data & Visualize (Python)**:

```
# Ensure dependencies are installed: pandas, openpyxl, matplotlib, and output.txt exists.
python huatu.py
```

This script will generate Search_Performance_Results.xlsx and plot_all.png / plot_binary.png automatically.
This plotting script is not core code so I use Chinese comment.