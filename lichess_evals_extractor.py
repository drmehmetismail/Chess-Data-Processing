"""This script efficiently decompresses and parses all .pgn.zst files in a directory, 
and writes all games with eval comments to a .pgn file.
"""

import re
import sys
import os
import zstandard as zstd

def extract_games(file_path, chunk_size=1024 * 1024 * 10):  # Default to 10 MB chunks
    dctx = zstd.ZstdDecompressor()
    with open(file_path, 'rb') as fh:
        with dctx.stream_reader(fh) as reader:
            previous_data = ''
            while True:
                chunk = reader.read(chunk_size)
                if not chunk:
                    break

                try:
                    data = previous_data + chunk.decode('utf-8')
                    games = re.split(r'\n\n(?=\[Event)', data)
                    if len(games) > 1:
                        yield from games[:-1]
                        previous_data = games[-1]
                    else:
                        previous_data = data

                except UnicodeDecodeError:
                    # Skip this chunk and move on to the next one
                    previous_data = ''
                    continue

            if previous_data:
                yield previous_data


def filter_and_save_games(input_directory, output_directory, max_file_size):
    file_index = 1
    current_file_size = 0
    output_file = None

    zst_files = [f for f in os.listdir(input_directory) if f.endswith('.zst')]
    for zst_file in zst_files:
        full_path = os.path.join(input_directory, zst_file)
        print(full_path)
        for game in extract_games(full_path):
            if "[%eval" in game and "Bullet" not in game:
                if not output_file or current_file_size >= max_file_size:
                    if output_file:
                        output_file.close()
                    output_filename = os.path.join(output_directory, f'games_with_eval_no_bullet{file_index}.pgn')
                    output_file = open(output_filename, 'w')
                    file_index += 1
                    print("file_index: ", file_index)
                    current_file_size = 0

                output_file.write(game + '\n\n')
                current_file_size += len(game.encode('utf-8'))

        if output_file:
            output_file.close()
            output_file = None

def main(input_directory, output_directory, max_file_size):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    filter_and_save_games(input_directory, output_directory, max_file_size
                          
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python lichess_evals_extractor.py <input_directory> <output_directory> <max_file_size>")
        sys.exit(1)
    input_directory = r"C:\Users\k1767099\_LichessDB\Output2"
    output_directory = r"C:\Users\k1767099\_LichessDB\Output2"
    max_file_size = 1024 * 1024 * 100  # Default 100 MB, can be modified

    main(input_directory, output_directory, max_file_size)
