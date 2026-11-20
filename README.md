# Page Replacement Algorithm Visualizer

A complete Python Tkinter GUI project for Operating Systems page replacement algorithms.

## Included algorithms
- FIFO (First-In, First-Out)
- LRU (Least Recently Used)
- Optimal
- LFU (Least Frequently Used)
- MFU (Most Frequently Used)
- Second Chance
- Clock
- MRU (Most Recently Used)
- Random

## Features
- Dark, coloured GUI
- Custom page reference string and frame count
- Step-by-step frame memory visualization
- Page hit / page fault indicators
- Replaced-page details
- Complete simulation trace table
- Hit/fault counts and percentages
- Previous, next, first and last step controls
- Compare all algorithms in one table
- Export simulation trace to CSV
- No external Python packages required

## Run on Windows
1. Extract the ZIP file.
2. Open the extracted `Page_Replacement_Visualizer` folder.
3. Open PowerShell or Command Prompt in that folder.
4. Run:

```bash
python main.py
```

If `python` is not recognized, try:

```bash
py main.py
```

## Example input
- Reference string: `7 0 1 2 0 3 0 4 2 3 0 3 2`
- Frame count: `3`
- Algorithm: `FIFO`

You can separate page numbers using spaces or commas.

## Project files
- `main.py` - application entry point
- `algorithms.py` - page replacement simulation logic
- `visualizer.py` - GUI, visualization, comparison and CSV export
