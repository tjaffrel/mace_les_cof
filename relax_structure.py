#!/usr/bin/env python
"""
Relax a structure using MACE-LES model.
Run with: pixi run python relax_structure.py
"""

import torch
from ase.io import read, write
from ase.optimize import LBFGS
from ase.filters import ExpCellFilter
from mace.calculators import MACECalculator

CIF_FILE = "COF-999_OH.cif"
MODEL_PATH = "SPICE_small_vf.model"
OUTPUT_FILE = "COF-999_OH_relaxed_volume.cif"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = "float32"
FMAX = 0.05  # Force convergence criterion in eV/Å
MAX_STEPS = 20
KEEP_CELL_FIXED = False  # Set to True to keep cell fixed, False to optimize cell

atoms = read(CIF_FILE)

calculator = MACECalculator(
    model_paths=MODEL_PATH,
    device=DEVICE,
    default_dtype=DTYPE
)

if DEVICE == "cuda":
    torch.cuda.empty_cache()

atoms.calc = calculator

initial_energy = atoms.get_potential_energy()
initial_fmax = abs(atoms.get_forces()).max()

# Geometry optimization
if not KEEP_CELL_FIXED:
    atoms = ExpCellFilter(atoms)
    print(f"Optimizing with cell (fmax={FMAX} eV/Å)...")
else:
    print(f"Optimizing positions only, cell fixed (fmax={FMAX} eV/Å)...")

opt = LBFGS(atoms, logfile="-")
converged = opt.run(fmax=FMAX, steps=MAX_STEPS)

# Get final atoms if ExpCellFilter was used
if not KEEP_CELL_FIXED:
    atoms = atoms.atoms

final_energy = atoms.get_potential_energy()
final_fmax = abs(atoms.get_forces()).max()

print(f"Energy: {initial_energy:.6f} -> {final_energy:.6f} eV (Δ={final_energy-initial_energy:.6f} eV)")
print(f"Max force: {initial_fmax:.6f} -> {final_fmax:.6f} eV/Å, Steps: {opt.nsteps}, Converged: {converged}")

write(OUTPUT_FILE, atoms)

if DEVICE == "cuda":
    torch.cuda.empty_cache()

print("Done!")

