# Makefile for FreezerInventoryApp

.PHONY: run test freeze clean

# Run the main application
run:
	@python src/freezer_inventory/main.py

# Run all tests using pytest
test:
	@pytest

# Update requirements.txt with current environment
freeze:
	@pip freeze > requirements.txt

# Remove __pycache__ and test artifacts
clean:
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@rm -f inventory/test_inventory.csv
