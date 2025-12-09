# mace_les_cof

MACE with Latent Ewald Summation (LES) for long-range interactions in COF systems.

## Prerequisites

Before starting, you need to install **pixi**, which is a tool that manages all the required software packages for this project.

### Installing Pixi

**On Linux or macOS:**

Open a terminal and run:

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

After installation, close and reopen your terminal, or run:

```bash
source ~/.bashrc
```

**On Windows:**

Download and run the installer from: https://pixi.sh/install

**Verify installation:**

To check if pixi is installed correctly, run:

```bash
pixi --version
```

You should see a version number. If you get an error, make sure pixi is in your PATH.

## Step-by-Step Setup

### Step 1: Navigate to the project directory

Open a terminal and go to the project folder:

```bash
cd /path/to/mace_les_cof
```

(Replace `/path/to/mace_les_cof` with the actual path to this folder on your computer)

### Step 2: Install the environment

This will download and install all required packages (this may take 5-10 minutes):

```bash
pixi install
```

**What this does:** Downloads Python, PyTorch, MACE, LES, and all other dependencies needed for calculations.

### Step 3: Verify installation

Test that everything is installed correctly:

```bash
pixi run test-imports
```

You should see: `All packages imported successfully!`

If you see any errors, see the Troubleshooting section below.

## Using the Relaxation Script

The main script for relaxing structures is `relax_structure.py`.

### Step 1: Edit the configuration

Open `relax_structure.py` in a text editor and modify these lines at the top:

```python
CIF_FILE = "COF-999_OH.cif"           # Your input CIF file
MODEL_PATH = "SPICE_small_vf.model"   # Path to your MACE model
OUTPUT_FILE = "COF-999_OH_relaxed.cif"  # Output filename
KEEP_CELL_FIXED = True                # True = keep cell fixed, False = optimize cell
FMAX = 0.05                            # Force convergence (eV/Å)
MAX_STEPS = 100                        # Maximum optimization steps
```

**Important settings:**
- `CIF_FILE`: Change this to your input structure file
- `KEEP_CELL_FIXED`: 
  - `True` = Only optimize atomic positions, keep cell parameters fixed
  - `False` = Optimize both atomic positions and cell parameters
- `FMAX`: Lower values (e.g., 0.01) = more accurate but slower. Default 0.05 is usually good.
- `MAX_STEPS`: Maximum number of optimization steps before stopping

### Recommended Settings for Scientific Publications

For publication-quality results, use stricter convergence criteria:

**For most structures:**
```python
FMAX = 0.01          # Stricter force convergence (0.01 eV/Å)
MAX_STEPS = 500      # Allow more steps for convergence
```

**For high-precision calculations:**
```python
FMAX = 0.001         # Very strict convergence (0.001 eV/Å)
MAX_STEPS = 1000     # Allow many steps for difficult cases
```

**For quick preliminary calculations:**
```python
FMAX = 0.05          # Standard convergence (0.05 eV/Å)
MAX_STEPS = 200      # Reasonable limit for most cases
```

**Guidelines:**
- **FMAX = 0.01 eV/Å** is typically sufficient for most publications and provides a good balance between accuracy and computational cost
- **FMAX = 0.001 eV/Å** is recommended for high-precision studies or when comparing with experimental data
- **MAX_STEPS = 500** is usually sufficient; increase to 1000 if convergence is difficult
- Always check that `Converged: True` in the output; if not, increase `MAX_STEPS` or check for issues with the structure

### Step 2: Run the relaxation

```bash
pixi run python relax_structure.py
```

Or simply:

```bash
pixi run relax
```

**What this does:** 
- Reads your CIF file
- Loads the MACE-LES model
- Optimizes the structure to minimize forces
- Saves the relaxed structure to the output file

### Step 3: Check the results

The script will print:
- Initial and final energy
- Maximum forces before and after optimization
- Number of optimization steps
- Whether convergence was achieved

The relaxed structure is saved to the file specified in `OUTPUT_FILE`.

## Running Python Scripts

To run any Python script in this environment:

```bash
pixi run python your_script.py
```

**Note:** You don't need to activate the environment separately. The `pixi run` command automatically uses the correct environment.

## Activating the Environment (Optional)

If you want to work interactively in Python, you can activate the environment:

```bash
pixi shell
```

This opens a shell with all packages available. Type `exit` to leave.

## GPU Acceleration (CUDA)

If you have an NVIDIA GPU and want to use it for faster calculations:

```bash
pixi run -e cuda python relax_structure.py
```

**Note:** Make sure you have CUDA drivers installed on your system. The script will automatically use CPU if CUDA is not available.

## Included Packages

- **mace-torch**: Machine learning interatomic potentials (from ChengUCB/mace with LES support)
- **les**: Latent Ewald Summation for long-range electrostatics
- **ase**: Atomic Simulation Environment (for structure manipulation)
- **pymatgen**: Python Materials Genomics (for materials analysis)

## Troubleshooting

### "pixi: command not found"

- Make sure pixi is installed (see Installing Pixi section)
- Close and reopen your terminal
- On Linux/macOS, try: `source ~/.bashrc`

### "All packages imported successfully!" fails

- Try running `pixi install` again
- Check your internet connection (packages need to be downloaded)
- Make sure you're in the project directory

### Script can't find the CIF file

- Make sure the CIF file is in the same directory as `relax_structure.py`
- Check that the filename in `CIF_FILE` matches exactly (case-sensitive)
- Use the full path if the file is elsewhere: `CIF_FILE = "/full/path/to/file.cif"`

### Script can't find the model file

- Make sure `SPICE_small_vf.model` (or your model file) is in the project directory
- Or use the full path: `MODEL_PATH = "/full/path/to/model.model"`

### Out of memory errors

- Reduce `MAX_STEPS` to a smaller number (e.g., 50)
- Use CPU instead of GPU: set `DEVICE = "cpu"` in the script
- For very large structures, you may need a computer with more RAM

## References

- [MACE](https://github.com/ACEsuit/mace) - Main MACE repository
- [MACE with LES](https://github.com/ChengUCB/mace) - MACE fork with LES support
- [LES](https://github.com/ChengUCB/les) - Latent Ewald Summation library
- [LES training scripts](https://github.com/ChengUCB/les_fit) - Training examples
