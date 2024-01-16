# Inputs a CSV generated from csv_to_player_stats.py and outputs a CSV with the normalized_gi column
# using the linear function obtained from the normalize_player_stats.py 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def normalize_gi(data, column_name):
    col = data[column_name]
    # Original linear function: normalized_avg_gi = 142.3271 + 27.8988 * avg_gi
    normalized_col = 142.33 + 27.90 * col
    return normalized_col

def visualize_distribution(data, column_name, title):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    sns.histplot(data[column_name], kde=True)
    plt.title(f'Histogram of {column_name}')


def main(file_path, output_dir):
    data = pd.read_csv(file_path)

    # Normalize avg_gis
    columns = ['avg_gi', 'avg_white_gi', 'avg_black_gi']
    normalized_gi = normalize_gi(data, column_name='avg_gi')
    data.insert(data.columns.get_loc('avg_gi') + 1, 'normalized_gi', normalized_gi)
    normalized_white_gi = normalize_gi(data, column_name='avg_white_gi')
    data.insert(data.columns.get_loc('avg_gi') + 2, 'normalized_white_gi', normalized_white_gi)
    normalized_black_gi = normalize_gi(data, column_name='avg_black_gi')
    data.insert(data.columns.get_loc('avg_gi') + 3, 'normalized_black_gi', normalized_black_gi)
    
    # Visualize the distribution of avg_gi and normalized_avg_gi
    # visualize_distribution(data, 'avg_gi', 'Original avg_gi Distribution')
    # visualize_distribution(data, 'normalized_gi', 'Normalized GI Distribution')

    # Save the updated DataFrame to the specified output directory
    output_file_path = os.path.join(output_dir, 'normalized_dataset.csv')
    data.to_csv(output_file_path, index=False)
    print(f"Normalization completed. Results saved to '{output_file_path}'.")
    
if __name__ == "__main__":
    # File paths and parameters
    file_path = ''
    output_dir = ''
    main(file_path, output_dir)
