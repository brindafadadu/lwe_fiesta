import argparse
import numpy as np
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="LWE Sample Generator Script")

    # 1. Add Arguments
    parser.add_argument("--N", type=int, required=True, help="Dimension of the lattice")
    parser.add_argument("--Q", type=int, required=True, help="The modulus")
    parser.add_argument("--rows", type=int, required=True, help="Number of samples (rows)")

    args = parser.parse_args()

    # 2. Calculate log2(Q) as an integer
    # We round it to handle float precision (e.g., 5.9999 -> 6.0)
    log2_q = int(round(np.log2(args.Q)))

    print("--- Configuration Received ---")
    print(f"Dimension (N): {args.N}")
    print(f"Modulus (Q):   {args.Q} (log2: {log2_q})")
    print(f"Rows:          {args.rows}")

    # 3. Handle Directory Creation
    # Pathlib is much cleaner than os.mkdir
    dir_path = Path(f"data/n{args.N}_logq{log2_q}")
    dir_path.mkdir(parents=True, exist_ok=True)

    # 4. Generate A matrix
    # size = (rows, columns)
    A = np.random.randint(0, args.Q, size=(args.rows, args.N), dtype=np.int64)

    # 5. Save the file
    file_name = f"origA_n{args.N}_logq{log2_q}.npy"
    save_full_path = dir_path / file_name
    
    np.save(save_full_path, A)
    
    print(f"--- Success ---")
    print(f"Matrix A saved to: {save_full_path}")
    print(f"Shape: {A.shape}")

if __name__ == "__main__":
    main()
