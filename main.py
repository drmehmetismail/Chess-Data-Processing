import os
import subprocess

def run_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_path}: {e}")

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Do not forget to specify input and output directories in each of these scripts:
    scripts = [
        'lichess_evals_extractor.py', 
        'pgn_evaluation_analyzer.py', 
        'json_to_csv_converter.py', 
        'chess_data_analyzer.py'
    ]
    script_paths = [os.path.join(base_path, script) for script in scripts]

    for script_path in script_paths:
        run_script(script_path)

if __name__ == "__main__":
    main()
