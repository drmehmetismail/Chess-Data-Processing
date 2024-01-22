"""
This Python script recursively modifies each JSON file by adding 'adjusted_white_gi' and 'adjusted_black_gi' keys based on given formulas.
The formula gives different weights to the intelligence scores achieved against opponents with lower rating.
"""

import os
import json
import math

def expected_score(elo, opponent_elo):
    return 1 / (1 + 10 ** ((opponent_elo - elo) / 400))

def calculate_adjusted_gi(gi, elo, opponent_elo):
    return gi - (1 - 2 * expected_score(elo, opponent_elo)) * abs(gi)

def process_json_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)

    for key, game in data.items():
        white_elo = int(game["WhiteElo"])
        black_elo = int(game["BlackElo"])
        game["adjusted_white_gi"] = calculate_adjusted_gi(game["white_gi"], white_elo, 2800)
        game["adjusted_black_gi"] = calculate_adjusted_gi(game["black_gi"], black_elo, 2800)

    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    input_directory = ""
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.json'):
                process_json_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
