# Chess Data Processing and Calculating Stats

## Overview
This Python codebase processes chess game data, transforming it from compressed Lichess database files to insightful stats including Game Intelligence (GI), Game Point Loss (GPL), and Average Centipawn Loss (ACPL). The pipeline goes through several stages of data extraction, analysis, and conversion.

## Scripts
1. `evaluated_games_extractor.py`: Extracts games with evaluations from .zst files (e.g. from Lichess Open database) and outputs PGN files.
2. `pgn_evaluation_analyzer.py`: Analyzes PGN files for chess game evaluations and outputs a JSON file.
3. `json_to_csv_converter.py`: Converts JSON data to CSV format for aggregated chess game stats.
4. `csv_to_player_stats.py`: Inputs the CSV file generated by json_to_csv_converter.py and outputs a CSV with player-specific stats.
5. `chess_stats_summarizer.py`: Inputs the CSV file generated by json_to_csv_converter.py and outputs a summary stats.
6. `main.py`: Main script to run the entire data processing pipeline.

## Additional scripts

7. `split_large_pgn.py`: # Splits large PGN file into smaller files based on size and content
8. `pgn_evaluation_fast_analyzer.py`: The stats are simpler and the script works faster than the pgn_evaluation_analyzer.py.
9. `player_stats_summarizer.py`: Inputs the CSV file generated by csv_to_player_stats.py and outputs a summary stats.
10. `normalize_gi.py`: Inputs a CSV generated from csv_to_player_stats.py and outputs a CSV with the normalized_gi column using the linear function initially obtained from the normalize_player_stats.py. This script can be used independently for any dataset.
11. `normalize_player_stats.py`: Inputs a CSV generated from csv_to_player_stats.py and outputs a CSV that includes normalized gi stats and prints the linear function to obtain normalized gi for a given raw gi. Use this script to double check the linear function initially obtained: normalized_gi = 142.33 + 27.90 * gi
12. `json_adjust_gi.py`: Modifies JSON files by adding 'adjusted_white_gi' and 'adjusted_black_gi' which are weighted by the opponents' rating.



## Usage
Run the `main.py` script to process data through all stages:

## Reference
For more information, see https://doi.org/10.48550/arXiv.2302.13937

## Citation
Please cite the following paper if you find this helpful.
```
@article{ismail2023human,
  title={Human and Machine: Practicable Mechanisms for Measuring Performance in Partial Information Games},
  author={Ismail, Mehmet S},
  journal={arXiv preprint arXiv:2302.13937},
  year={2023}
}
```
