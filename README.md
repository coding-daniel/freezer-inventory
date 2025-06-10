# 📦 Freezer Inventory App

[![Run Python Tests](https://github.com/coding-daniel/freezer-inventory/actions/workflows/python-tests.yml/badge.svg)](https://github.com/coding-daniel/freezer-inventory/actions/workflows/python-tests.yml)

A minimal barcode-based inventory tracker built with Python.

- Scan product barcodes manually
- Auto-fetch product names and weights via Open Food Facts API
- Track quantities of household items
- Store inventory locally in a CSV file
- Sync via Dropbox or OneDrive (optional)
- Extensible, testable, and beginner-friendly

---

## 🚀 Quick Start

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
make run

# Run tests
make test
