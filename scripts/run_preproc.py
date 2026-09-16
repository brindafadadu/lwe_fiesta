import os
import subprocess

def interactive_run():
    print("--- LWE Preprocessing Wizard ---")
    
    # Define inputs and their defaults
    n = input("Enter N (e.g., 80): ") or "80"
    q = input("Enter Q (e.g., 113): ") or "113"
    
    dump_path = input("Enter dump_path (default: ./preproc_data) (adviced to store under data directory with apt folder name): ") or "./preproc_data"
    
    exp_name = input(f"Enter exp_name (default: R_A_{n}_7_debug): ") or f"R_A_{n}_7_debug"
    
    workers = input("Enter number of workers (default: 5): ") or "5"
    
    # Path to the data to reload
    default_data = f"./data/benchmark_paper_data/n80_logq7/origA_n80_logq7.npy"
    reload_data = input(f"Enter reload_data path(where the origA*.npy file is present) (default: {default_data}): ") or default_data
    
    thresholds = input('Enter thresholds (default: "0.783,0.783001,0.7831") (lookup code to understand): ') or "0.783,0.783001,0.7831"
    
    lll_penalty = input("Enter lll_penalty (default: 10): ") or "10"

    # Construct the command list
    command = [
        "python3", "src/generate/preprocess.py",
        "--N", n,
        "--Q", q,
        "--dump_path", dump_path,
        "--exp_name", exp_name,
        "--num_workers", workers,
        "--reload_data", reload_data,
        "--thresholds", thresholds,
        "--lll_penalty", lll_penalty
    ]

    print("\n--- Executing Command ---")
    print(" ".join(command))
    print("-------------------------\n")

    # Run the script
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("Error: Could not find 'src/generate/preprocess.py'. Make sure you are in the project root.")
    except subprocess.CalledProcessError as e:
        print(f"The script crashed with error: {e}")

if __name__ == "__main__":
    interactive_run()
