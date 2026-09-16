import subprocess
import os
from pathlib import Path

def get_input(prompt, default):
    user_val = input(f"{prompt} (default: {default}): ").strip()
    return user_val if user_val else default

def main():
    print("--- ❄️🔥 Cool and Cruel (CC) Attack Control Center ---")

    # 1. PATH CONFIGURATION
    # The path should be the folder containing your generated samples and secrets
    data_path = get_input("Data path", "data/n32_logq7/binary_secrets_h3_4/")
    dump_path = get_input("Path to save logs/checkpoints", "./cc_logs")
    exp_name = get_input("Experiment Name", "cc_n32_test")

    # 2. BRUTE FORCE (CRUEL) PARAMETERS
    # IMPORTANT: Run the 'describe' action first to find this value!
    bf_dim = get_input("BF Dimension (Cruel Bits found via 'describe')", "32")
    min_bf_hw = get_input("Min Hamming Weight for BF search", "1")
    max_bf_hw = get_input("Max Hamming Weight for BF search", "3")

    # 3. SECRET PARAMETERS
    secret_type = get_input("Secret type (binary/ternary)", "binary")
    full_hw = get_input("Full Hamming Weight of the secret", "3")
    
    # 4. ATTACK HYPERPARAMETERS
    # greedy_max_data: How many samples to use for the attack
    # secret_window: Usually N + some buffer (e.g., if N=32, window=40)
    greedy_data = get_input("Max samples to use (greedy_max_data)", "100000")
    batch_size = get_input("Batch size for search", "10000")
    sec_window = get_input("Secret window size", "40")
    
    # 5. TECHNICAL FLAGS
    # mlwe_k: Set to 1 for standard LWE
    # compile_bf: 1 to use a compiled brute-force (faster), 0 for python
    mlwe_k = get_input("MLWE K (0 for standard LWE)", "0")
    compile_bf = get_input("Use Compiled BF? (1=Yes, 0=No)", "0")

    # Build the Command
    command = [
        "python3", "src/cruel_cool/main.py",
        "--path", data_path,
        "--exp_name", exp_name,
        "--dump_path", dump_path,
        "--bf_dim", bf_dim,
        "--min_bf_hw", min_bf_hw,
        "--max_bf_hw", max_bf_hw,
        "--secret_type", secret_type,
        "--full_hw", full_hw,
        "--greedy_max_data", greedy_data,
        "--batch_size", batch_size,
        "--secret_window", sec_window,
        "--mlwe_k", mlwe_k,
        "--compile_bf", compile_bf,
        "--keep_n_tops", "1",
        "--seed", "0"
    ]

    print("\n--- Cruel and Cool Command ---")
    print(" ".join(command))
    print("------------------------------\n")

    confirm = input("Execute Attack? (y/n): ").lower()
    if confirm == 'y':
        try:
            Path(dump_path).mkdir(parents=True, exist_ok=True)
            subprocess.run(command, check=True)
            print("\n✅ Attack sequence finished!")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Attack failed. Check if bf_dim matches your data.")
    else:
        print("Aborted.")

if __name__ == "__main__":
    main()
