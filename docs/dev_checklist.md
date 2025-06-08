# Cross-Platform Development Checklist

This guide ensures a smooth development experience across **macOS** and **Windows**.
It covers environment setup, device support, and troubleshooting relevant to this project.

---

## Supported Platforms

- **macOS (M1/M2/M3 and Intel)**
- **Windows 10+ with CUDA-enabled GPU**

---

## Python & Virtual Environment Setup

We recommend using **Python 3.10+**.

```bash
# macOS / Linux / WSL
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Ensure pip is up to date:

```bash
pip install --upgrade pip
```

---

## Install Requirements

Install project dependencies:

```bash
pip install -r requirements.txt
```

---

## Torch installation

### macPS (M1/M2/M3):

Apple Silicon support uses metal backend (MPS).

```bash
pip install torch torchvision torchaudio
```

**MPS will be auto-detected and used if available.**

### Windows (CUDA-Enabled GPU):

Install with CUDA backend (adjust the URL for your CUDA version if needed)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/wh1/cu121
```

**For CPU-only setups, regular `pip install torch` works too.**

---

## `,env` File for Local Overrides

You can override settings without modifying source code by creating a .env file in the project root.

Example:

```env
DEBUG_MODE=True
MAX_HISTORY_TURNS=5
```

These values override the corresponding fields in config/settings.json during runtime.

---

## Running the App

Once everything is installed:

```bash
python main.py
```

---

## Verifying Device Detection

On startup, the app logs the selected PyTorch device (e.g., cuda, mps, or cpu):

```txt
[System] Torch detected device: cuda
```

If you’re not seeing this, check:
  - You’ve installed the correct version of `torch`
  - Your `.env` file (if used) doesn’t override the environment unintentionally

---

## Troubleshooting Tips

| Issue                         | Fix                                                                                                           |
|-------------------------------|---------------------------------------------------------------------------------------------------------------|
| Torch not detecting MPS       | Ensure you’re on **macOS 12.3+** with **Python 3.10+**, and have the latest `pip`-installed **torch**.        |
| CUDA not found on Windows     | Install the correct **torch** wheel via `--index-url https://download.pytorch.org/whl/cu121` (or matching CUDA version). |
| Models not loading            | Verify internet access to Hugging Face or pre-download the models manually into the cache.                   |
| Environment not loading       | Confirm a `.env` file exists in the project root and is readable.                                            |
| Logging not showing           | Check `DEBUG_MODE=True` in `.env` or `config/settings.json`; ensure logging is configured early in `main.py`. |

---

## Linked From

This file is referenced in:

- [README.md](../README.md)
- [CONTRIBUTING.md](../docs/CONTRIBUTING.md)
