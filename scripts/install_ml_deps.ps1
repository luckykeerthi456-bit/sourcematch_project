# PowerShell helper to install ML dependencies for SourceMatch on Windows
# Run this inside the activated venv (PowerShell):
#   . .\venv\Scripts\Activate.ps1
#   .\scripts\install_ml_deps.ps1

Write-Host "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

Write-Host "Installing CPU-only PyTorch wheels (from pytorch.org)..."
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio

Write-Host "Installing sentence-transformers and other Python requirements..."
python -m pip install sentence-transformers
python -m pip install -r requirements-backend.txt

Write-Host "Done. If the model needs to be downloaded, run the preload script: python scripts/preload_model.py"
