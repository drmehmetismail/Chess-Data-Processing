"""This script decompresses and parses all .pgn.zst files in a directory, 
and writes all games with eval comments to a .pgn file.
It also writes all bullet games with eval comments to a separate .pgn file."""

import os
import chess.pgn
import zstandard as zstd
import io

def decompress_and_parse(input_directory, output_directory):
    eval_games_count = 0
    bullet_games_count = 0

    evals_file_path = os.path.join(output_directory, 'evals.pgn')
    bullets_file_path = os.path.join(output_directory, 'bullets.pgn')

    with open(evals_file_path, 'w', encoding='utf-8') as evals_file, open(bullets_file_path, 'w', encoding='utf-8') as bullets_file:
        for file in os.listdir(input_directory):
            if file.endswith('.pgn.zst'):
                file_path = os.path.join(input_directory, file)
                with open(file_path, 'rb') as compressed_file:
                    dctx = zstd.ZstdDecompressor()
                    with dctx.stream_reader(compressed_file) as reader:
                        text_stream = io.TextIOWrapper(reader, encoding='utf-8')
                        while True:
                            game = chess.pgn.read_game(text_stream)
                            if game is None:
                                break
                            
                            node = game
                            while node.variations:
                                node = node.variation(0)
                                if '[%eval' in node.comment:
                                    is_bullet = "Bullet" in game.headers.get("Event", "")
                                    output_file = bullets_file if is_bullet else evals_file
                                    output_file.write(str(game) + '\n\n')
                                    if is_bullet:
                                        bullet_games_count += 1
                                    else:
                                        eval_games_count += 1
                                    break

    return eval_games_count, bullet_games_count

def main():
    input_directory = 'input_directory'
    output_directory = 'output_directory'
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    total_eval_games, total_bullet_games = decompress_and_parse(input_directory, output_directory)
    print(f"Total games with eval comments: {total_eval_games}")
    print(f"Total bullet games with eval comments: {total_bullet_games}")

if __name__ == '__main__':
    main()