import pandas as pd
import numpy as np
import os
from scipy.optimize import curve_fit

def logistic_function(x, L, k, x0):
    try:
        return L / (1 + np.exp(-k * (x - x0)))
    except OverflowError:
        return float('inf')

def normalize_column(data, column_name, mean=100, std_dev=15):
    col = data[column_name]
    normalized_col = (col - col.mean()) / col.std() * std_dev + mean
    return normalized_col

def fit_logistic_function(x, y):
    # Adjusted initial parameter guesses: [1.1 * max(y), 1, median(x)]
    initial_guesses = [max(y) * 1.3, 1, np.median(x)]    
    try:
        params, _ = curve_fit(logistic_function, x, y, p0=initial_guesses)
        return params
    except RuntimeError:
        print("Error - curve fitting failed")
        return [0, 0, 0]

def main(file_path, min_games_played, min_gpl, output_dir):
    data = pd.read_csv(file_path)

    # Filter rows based on min_games_played and min_gpl
    data = data[(data['total_game_count'] >= min_games_played) & (data['avg_gpl'] >= min_gpl)]
    
    # Normalize avg_gi
    data['normalized_avg_gi'] = normalize_column(data, 'avg_gi')

    # Fit logistic function
    params = fit_logistic_function(data['avg_gi'], data['normalized_avg_gi'])

    if all(param == 0 for param in params):
        print("Failed to fit logistic function.")
        return

    # Output the logistic function parameters
    print(f"Fitted Logistic Function: L / (1 + exp(-k * (x - x0)))")
    print(f"Where L = {params[0]}, k = {params[1]}, x0 = {params[2]}")

    # Predict using logistic function
    data['predicted_normalized_avg_gi'] = data['avg_gi'].apply(lambda x: logistic_function(x, *params))

    # Save the updated DataFrame to the specified output directory
    output_file_path = os.path.join(output_dir, 'normalized_dataset_min-100.csv')
    data.to_csv(output_file_path, index=False)
    print("Normalization and fitting completed. Results saved to 'normalized_dataset.csv'.")

if __name__ == "__main__":
    # Load CSV
    file_path = r'C:\Users\k1767099\Downloads\Lichess_stats\player_stats.csv'
    min_games_played = 100
    min_gpl = 0.1
    output_dir = r'C:\Users\k1767099\Downloads\Lichess_stats'
    main(file_path, min_games_played, min_gpl, output_dir)
