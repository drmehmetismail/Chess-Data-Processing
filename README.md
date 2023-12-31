# Chess Data Processing and Calculating Stats

## Overview
This Python codebase processes chess game data, transforming it from compressed Lichess database files to insightful stats including Game Intelligence, Game Point Loss, and Average Centipawn Loss (ACPL). The pipeline goes through several stages of data extraction, analysis, and conversion.

## Scripts
1. `lichess_evals_extractor.py`: Extracts evaluations from Lichess database files and outputs PGN files.
2. `pgn_evaluation_analyzer.py`: Analyzes PGN files for chess game evaluations and outputs a JSON file.
3. `json_to_csv_converter.py`: Converts JSON data to CSV format for aggregated chess game stats.
4. `chess_data_analyzer.py`: Processes CSV data to calculate and visualize various stats.
5. `main.py`: Main script to run the entire data processing pipeline.

## Usage
Run the `main.py` script to process data through all stages:
