# LWE Benchmarking & Replication Wrapper

This repository contains our attempt to improve the dataset generation and attack execution for Machine Learning-based cryptanalysis of the Learning with Errors (LWE) problem.

## Acknowledgments and Core Codebase

**This project is built entirely upon the foundational open-source release by Facebook Research.** All credit for the core ML architectures and attack mechanics belongs to the original authors.

- **Original Repository:** [facebookresearch/LWE-benchmarking](https://github.com/facebookresearch/LWE-benchmarking/)

---

## Environment Setup

### Phase 1: Conda Environment Setup

We would need to setup conda to resolve dependencies for the attacks to work.

#### 1. Install Miniconda (If not already installed)

Run these commands in your Linux terminal to download and install Miniconda from scratch:

```bash
# Create a directory for the installer
mkdir -p ~/miniconda3

# Download the latest Linux installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh

# Run the installer silently
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

# Clean up the installation file
rm -rf ~/miniconda3/miniconda.sh

# Initialize conda for bash and zsh shells
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```

> ⚠️ **Important:** After running the above, **close and reopen your terminal** (or run `source ~/.bashrc`) to apply the Conda initialization. You should see `(base)` appear at the start of your command prompt.

#### 2. Create the Lattice Environment

Instead of installing packages manually, we will use the pre-configured environment file provided in the repository. This sets up the `lattice_env` with all necessary deep learning and math dependencies for the SALSA, Cool & Cruel, and uSVP attacks. This step may be slow.

```bash
# Ensure you are in the root directory of the repository
# Create the environment from the provided YAML file
conda env create -f environment/environment.yml

# Activate the environment
conda activate lattice_env
```

---

### Phase 2: Installing Flatter (Lattice Reduction)

The post-processing phase of the attacks relies on `flatter`, a high-performance C++ library for lattice reduction.

Please follow the official installation and build instructions on the Flatter GitHub repository:

- [keeganryan/flatter](https://github.com/keeganryan/flatter) — GitHub Repository

Clone the repository and run the 6 commands mentioned in its README under Installation Guidelines. Install any dependancies it asks you to install.

> ⚠️ **Important:** After building `flatter`, ensure the executable is correctly symlinked or added to your system's `PATH` (e.g., `/usr/local/bin/`) so that it can be executed globally by typing `flatter` in the terminal.

---

##  Data Generation Pipeline

Instead of running complex base commands manually, we provide interactive helper scripts in the `scripts/` directory to generate data and launch attacks seamlessly.

---

### Step 1: Generate Matrix A

The first step is to generate the uniform distribution matrix $A$. Usually, the number of rows ($m$) is generally taken to be $4 \times n$, but this can be adjusted to test different redundancy thresholds.

```bash
python3 scripts/generate_A.py --N <n_val> --Q <q_val> --rows <num_rows>
```

 **Output:** `data/n{n_val}logq{logqval}/origA_n{n_val}logq{logqval}.npy`

---

### Step 2: Preprocess the Dataset

The Transformer model requires data to be formatted into specific `data.prefix` files. This script handles that conversion.

```bash
python3 scripts/run_preproc.py
```

- **Interactive Prompts:** The script will ask for necessary setup info.
- **Reload Data:** Provide the absolute or relative path to the `.npy` file generated in Step 1.
- **Continuous Generation:** This process runs in an infinite loop to build massive datasets required for ML training. Stop the process safely with `CTRL + C` once enough samples are generated.
- **Dump_path:**  Note the `dump_path` you provide. Its advised to just use the data/n*_logq* directory.

>  **Pro-Tip:** Check the sample count in another terminal using:
> ```bash
> wc -l <dump_path>/data.prefix
> ```

---

### Step 3: Format the Task (A and b)

This step formats the preprocessed data into specific target vectors (`train_A.npy`, `train_b.npy`, etc.) tailored for your chosen attack.

```bash
python3 scripts/genAb.py
```

- **RLWE:** Set to `0` for standard LWE attacks.
- **Actions:**
  - Type `secrets` if you are preparing data for a standard SALSA attack.
  - Type `describe` if you want to learn number of cruel bits for the Cool & Cruel attack.
- **Dump Path:** Its advised to create an additional folder like a 'ready' folder in the data/n**_logq*/ directory and use that.
- **Processed Dump Path:** Use the <experiment_name> folder from the last step in the data/n**_logq*/ directory.
---

Keep in mind the scripts are data path sensitive and will only work properly if you use the correct directory structure.

## Executing the Attacks

Once your dataset is fully generated and preprocessed, you can launch the attacks. We provide interactive runners for standard architectures as well as optimized paths for consumer GPUs.

---

### 1. SALSA Attack (Standard)

This runs the baseline encoder-only Transformer model for secret recovery.

```bash
python3 scripts/run_salsa.py
```

- **Task:** When prompted for the task, explicitly type `lwe`.
- Follow the remaining interactive prompts to provide your dataset path and ML hyperparameters.

---

### 2. SALSA Optimised (FlashAttention)

This runs the optimized encoder-only Transformer model with FlashAttention for improved performance on consumer GPUs.

```bash
python3 scripts/run_salsa_opt.py
```

- Use similar parameters as the standard SALSA attack above.

---

### 3. Cool & Cruel Attack

This attack attempts targeted bit recovery based on the cruel bits identified during preprocessing.

```bash
python3 scripts/run_cc.py
```
- **Cruel Bits:** When prompted, ensure the number of cruel bits you input exactly matches the number calculated and output during the `genAb.py` formatting step using describe as the actions.
