import subprocess
import os
from pathlib import Path

def get_input(prompt, default):
    user_val = input(f"{prompt} (default: {default}): ").strip()
    return user_val if user_val else default

def main():

    # 1. PATHS & LOGGING
    data_path = get_input("Data path (where A and b are) ", "./testn80/binary_secrets_h5_6/")
    exp_name = get_input("Experiment Name (for logs)", "salsa_demo")
    dump_path = get_input("Log/Checkpoint Dump Path", "./salsa_logs")

    # 2. CRYPTO PARAMETERS
    secret_seed = get_input("Secret Seed (which secret do u wanna attack in case you had multiple secret seeds)", "0")
    rlwe = get_input("Is this RLWE? (1=Yes, 0=No)", "0") # Matches your previous choice
    task = get_input("Task (can choose lwe for normal lwe)", "lwe")
    hamming = get_input("Target Hamming Weight", "5")
    a_shift = get_input("A_shift (preprocessing parameter useless for normal lwe(used in mlwe))", "42")

    # 3. TRANSFORMER ARCHITECTURE (The "Model Capacity")
    n_heads = get_input("Number of Attention Heads", "8")
    n_layers = get_input("Number of Encoder Layers", "4")
    emb_dim = get_input("Embedding Dimension", "256")
    dist_size = get_input("Distinguisher Size", "64")

    # 4. TRAINING HYPERPARAMETERS
    train_bs = get_input("Training Batch Size", "64")
    val_bs = get_input("Validation Batch Size", "128")
    
    # Base/Bucket determine how integers are tokenized for the transformer
    base = get_input("Encoding Base", "1")
    bucket = get_input("Bucket Size", "1")

    # 5. SPECIAL FEATURES (SALSA FRESCA improvements)
    angular = get_input("Use Angular Embeddings? (true/false)", "true")
    dx_dist = get_input("Use DX Distinguisher? (true/false)", "true")

    # Build the Command
    command = [
        "python3", "src/salsa_test/train_and_recover.py",
        "--data_path", data_path,
        "--exp_name", exp_name,
        "--secret_seed", secret_seed,
        "--rlwe", rlwe,
        "--task", task,
        "--angular_emb", angular,
        "--dxdistinguisher", dx_dist,
        "--hamming", hamming,
        "--A_shift", a_shift,
        "--train_batch_size", train_bs,
        "--val_batch_size", val_bs,
        "--n_enc_heads", n_heads,
        "--n_enc_layers", n_layers,
        "--enc_emb_dim", emb_dim,
        "--base", base,
        "--bucket_size", bucket,
        "--dump_path", dump_path,
        "--distinguisher_size", dist_size
    ]

    print("\n--- Command Ready to Fire ---")
    print(" ".join(command))
    print("-----------------------------\n")

    confirm = input("Start Training? (y/n): ").lower()
    if confirm == 'y':
        try:
            # Ensure log directory exists
            Path(dump_path).mkdir(parents=True, exist_ok=True)
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Training failed. Check if your GPU is available or if N matches the data.")
    else:
        print("Aborted.")

if __name__ == "__main__":
    main()
