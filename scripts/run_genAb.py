import subprocess
from pathlib import Path

def get_input(prompt, default):
    user_val = input(f"{prompt} (default: {default}): ").strip()
    return user_val if user_val else default

def main():
    print("--- LWE Secret & Sample Generation Wizard ---")

    # 1. Path Configuration
    # We use .resolve() to ensure the script finds the data regardless of where you are
    proc_dump = get_input("Enter path of PREPROCESSED data (usually in data directory with apt directory used during preprocessing)", "./preproc_data")
    out_dump = get_input("Enter path to STORE final samples (usually again in the data directory into a deeper folder)", "./test_results")

    # 2. Lattice Parameters
    n = get_input("Enter N", "80")
    rlwe = get_input("Is this RLWE? (1 for Yes, 0 for No)", "0")
    
    # 3. Secret Distribution Parameters
    secret_type = get_input("Secret type (binary/ternary/gaussian)", "binary")
    min_h = get_input("Min Hamming Weight", "5")
    max_h = get_input("Max Hamming Weight", "6")
    num_seeds = get_input("Number of secret seeds (no. of secrets you wanna generate)", "10")
    
    # 4. Action
    action = get_input("Action to perform (secrets/describe)", "secrets")

    # Construct the command
    command = [
        "python3", "src/generate/generate_A_b.py",
        "--processed_dump_path", str(Path(proc_dump).resolve()),
        "--dump_path", str(Path(out_dump).resolve()),
        "--N", n,
        "--rlwe", rlwe,
        "--min_hamming", min_h,
        "--max_hamming", max_h,
        "--secret_type", secret_type,
        "--num_secret_seeds", num_seeds,
        "--actions", action
    ]

    print("\n--- Command to be Executed ---")
    print(" ".join(command))
    print("------------------------------\n")

    confirm = input("Run this command? (y/n): ").lower()
    if confirm == 'y':
        try:
            subprocess.run(command, check=True)
            print("\n✅ Generation Complete!")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Script failed with error: {e}")
    else:
        print("Aborted.")

if __name__ == "__main__":
    main()
