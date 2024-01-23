"""This script analyzes chess game data, calculates various statistics (including sums, medians, and averages), 
and generates a final DataFrame with player statistics, sorted by the average gi score in descending order.
This script does what csv_to_player_stats.py does except that it does not consider adjusted_white_gi and adjusted_black_gi column."""

import pandas as pd
import sys
import os
import glob

def combine_csv_files(input_dir, output_filename='combined.csv'):
    csv_files = glob.glob(os.path.join(input_dir, '*.csv'))
    combined_df = pd.DataFrame()

    for file in csv_files:
        df = pd.read_csv(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    output_path = os.path.join(input_dir, output_filename)
    combined_df.to_csv(output_path, index=False)
    print(f"Combined CSV created at {output_path}")
    return output_path

# Functions
def read_csv(file_path):
    return pd.read_csv(file_path)

def check_dataframe(df, df_name):
    print(f"Columns in {df_name}: {df.columns}")

def calculate_sum(df, group_col, value_col, prefix):
    sums = df.groupby(group_col).agg({value_col: 'sum'}).reset_index()
    sums.columns = ['Player', f'{prefix}_sum']
    return sums

def calculate_games(df, player_col):
    game_count = df[player_col].value_counts().reset_index()
    game_count.columns = ['Player', f'{player_col}_games']
    return game_count

def calculate_total_games(white_games, black_games):
    total_games = pd.merge(white_games, black_games, on='Player', how='outer').fillna(0)
    total_games['total_game_count'] = total_games['White_games'] + total_games['Black_games']
    return total_games

def calculate_total_moves(df):
    # Summing up the moves made by each player as White and Black
    white_moves = calculate_sum(df, 'White', 'white_move_number', 'white_move')
    black_moves = calculate_sum(df, 'Black', 'black_move_number', 'black_move')
    total_moves = pd.merge(white_moves, black_moves, on='Player', how='outer').fillna(0)
    total_moves['total_moves'] = total_moves['white_move_sum'] + total_moves['black_move_sum']
    return total_moves[['Player', 'total_moves']]

def calculate_statistics(df, value_col):
    stats = df.groupby('Player').agg(median=(value_col, 'median'), 
                                     var=(value_col, 'var'), 
                                     std=(value_col, 'std')).reset_index()
    return stats.rename(columns={'median': f'{value_col}_median', 
                                 'var': f'{value_col}_var', 
                                 'std': f'{value_col}_std'})

def merge_dataframes(dfs, merge_on='Player'):
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=merge_on, how='outer').fillna(0)
    return merged_df

def calculate_averages(player_stats):
    player_stats['avg_gi'] = player_stats['total_gi_sum'] / player_stats['total_game_count']
    player_stats['avg_gpl'] = player_stats['total_gpl_sum'] / player_stats['total_game_count']
    player_stats['avg_acpl'] = player_stats['total_acpl_sum'] / player_stats['total_game_count']
    return player_stats

def save_to_csv(df, file_path):
    df.to_csv(file_path, index=False)

# Main Functionality
def main(csv_all_games_path, player_stats_output_dir):
    if not os.path.exists(csv_all_games_path):
        print(f"File not found: {csv_all_games_path}")
        return
    df = read_csv(csv_all_games_path)
    # check_dataframe(df, "Initial DataFrame")

    # Calculating Sums
    white_gi_sum = calculate_sum(df, 'White', 'white_gi', 'white_gi')
    black_gi_sum = calculate_sum(df, 'Black', 'black_gi', 'black_gi')
    white_gpl_sum = calculate_sum(df, 'White', 'white_gpl', 'white_gpl')
    black_gpl_sum = calculate_sum(df, 'Black', 'black_gpl', 'black_gpl')
    white_acpl_sum = calculate_sum(df, 'White', 'white_acpl', 'white_acpl')
    black_acpl_sum = calculate_sum(df, 'Black', 'black_acpl', 'black_acpl')

    # Calculating Game Counts
    white_games = calculate_games(df, 'White')
    black_games = calculate_games(df, 'Black')
    total_games = calculate_total_games(white_games, black_games)
    total_moves = calculate_total_moves(df)
    
    # Calculating Statistics
    combined_df = pd.concat([
        df[['White', 'white_gi', 'white_gpl', 'white_acpl']].rename(columns={'White': 'Player', 'white_gi': 'gi', 'white_gpl': 'gpl', 'white_acpl': 'acpl'}),
        df[['Black', 'black_gi', 'black_gpl', 'black_acpl']].rename(columns={'Black': 'Player', 'black_gi': 'gi', 'black_gpl': 'gpl', 'black_acpl': 'acpl'})
    ])
    gi_stats = calculate_statistics(combined_df, 'gi')
    gpl_stats = calculate_statistics(combined_df, 'gpl')
    acpl_stats = calculate_statistics(combined_df, 'acpl')

    # Merging DataFrames
    sums = [white_gi_sum, black_gi_sum, white_gpl_sum, black_gpl_sum, white_acpl_sum, black_acpl_sum]
    total_sums = merge_dataframes(sums + [total_games, total_moves])
    total_sums['total_gi_sum'] = total_sums['white_gi_sum'] + total_sums['black_gi_sum']
    total_sums['total_gpl_sum'] = total_sums['white_gpl_sum'] + total_sums['black_gpl_sum']
    total_sums['total_acpl_sum'] = total_sums['white_acpl_sum'] + total_sums['black_acpl_sum']

    player_stats = merge_dataframes([total_sums, gi_stats, gpl_stats, acpl_stats])

    # Calculating Averages
    player_stats = calculate_averages(player_stats)

    # Reordering columns
    columns_order = ['Player', 'avg_gi', 'avg_gpl', 'avg_acpl', 'total_game_count', 'total_moves', 'gi_median', 'gpl_median', 'acpl_median', 'gi_std', 'gpl_std', 'acpl_std'] + [col for col in player_stats.columns if col not in ['Player', 'avg_gi', 'avg_gpl', 'avg_acpl', 'total_game_count', 'total_moves', 'gi_median', 'gpl_median', 'acpl_median', 'gi_std', 'gpl_std', 'acpl_std']]
    player_stats = player_stats[columns_order]

    # Ensure the output directory exists
    if not os.path.exists(player_stats_output_dir):
        os.makedirs(player_stats_output_dir)

    # Define the output CSV file path within the output directory
    output_file_path = os.path.join(player_stats_output_dir, 'player_stats.csv')

    # Sorting and Saving
    player_stats = player_stats.sort_values(by='avg_gi', ascending=False)
    save_to_csv(player_stats, output_file_path)


if __name__ == "__main__":
    # If multiple CSVs in a directory, then uncomment the following two lines.
    # input_dir = ''
    # csv_all_games_path = combine_csv_files(input_dir, output_filename='combined.csv')
    if len(sys.argv) < 3:
        print("Usage: python csv_to_player_stats.py <csv_all_games_path> <player_stats_output_dir>")
        sys.exit(1)

    csv_all_games_path = sys.argv[1]
    player_stats_output_dir = sys.argv[2]
    main(csv_all_games_path, player_stats_output_dir)
