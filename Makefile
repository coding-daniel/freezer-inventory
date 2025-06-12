# Run the main CLI app
run-cli:
	python src/freezer_inventory/main.py

# Run the Flask web server
run:
	python src/web/api.py

# Run tests using pytest
test:
	pytest tests

# Format with black (optional)
format:
	black src tests

# Install dependencies
install:
	pip install -r requirements.txt

# Clean up Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -name "*.pyc" -delete

# Force semantic-release dry-run (for testing locally)
dry-release:
	npx semantic-release --dry-run
