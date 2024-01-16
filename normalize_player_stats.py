# Inputs a CSV generated from csv_to_player_stats.py and outputs a CSV that includes normalized gi stats
# and prints the linear function to obtain normalized gi for a given raw gi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def normalize_column(data, column_name, new_mean=100, new_std=15):
    col = data[column_name]
    original_mean = col.mean()
    original_std = col.std()
    normalized_col = new_std * ((col - original_mean) / original_std) + new_mean
    return normalized_col, original_mean, original_std

def visualize_distribution(data, column_name, title):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    sns.histplot(data[column_name], kde=True)
    plt.title(f'Histogram of {column_name}')

# linear function for normalized GI
# normalized_avg_gi = a * avg_gi + b
def calculate_normalized_avg_gi(mu, sd):
    # Calculate b and a using the given formulas
    b = -15 * mu / sd + 100
    a = (100 - b) / mu
    # normalized_avg_gi = a * avg_gi + b
    # return slope = a and intercept = b
    return a, b


def main(file_path, min_games_played, min_gpl, output_dir):
    data = pd.read_csv(file_path)

    # Filter rows based on min_games_played and min_gpl
    data = data[(data['total_game_count'] >= min_games_played) & (data['avg_gpl'] >= min_gpl)]

    # Normalize avg_gi
    normalized_avg_gi, original_mean, original_std = normalize_column(data, 'avg_gi')
    data.insert(data.columns.get_loc('avg_gi') + 1, 'normalized_avg_gi', normalized_avg_gi)

    # Visualize the distribution of avg_gi and normalized_avg_gi
    # visualize_distribution(data, 'avg_gi', 'Original avg_gi Distribution')
    # visualize_distribution(data, 'normalized_avg_gi', 'Normalized avg_gi Distribution')

    # Output linear regression model parameters
    slope, intercept = calculate_normalized_avg_gi(original_mean, original_std)
    print("original_mean: ", original_mean)
    print("original_std: ", original_std)
    # Print the formula
    print(f"normalized_avg_gi = {slope:.4f} * avg_gi + {intercept:.4f}")

    # Calculate and print for specific values of avg_gi
    # print("normalized_avg_gi = ", slope * 0.75 + intercept)

    # Save the updated DataFrame to the specified output directory
    output_file_path = os.path.join(output_dir, 'normalized_dataset_player_stats.csv')
    data.to_csv(output_file_path, index=False)
    print(f"Normalization completed. Results saved to '{output_file_path}'.")
    
if __name__ == "__main__":
    # File paths and parameters
    file_path = ''
    # set min_games_played and min_gpl values
    min_games_played = 10
    min_gpl = 0
    output_dir = ''
    main(file_path, min_games_played, min_gpl, output_dir)
