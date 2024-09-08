.PHONY: test clean

LOG_LEVEL=DEBUG
PYPOE := $(shell poetry env info -e)

# Run the unit tests
test:
	sudo -E LOG_LEVEL=$(LOG_LEVEL) $(PYPOE) -m unittest discover -s tests 

# Clean up any Python cache files
clean:
	find . -name '__pycache__' -exec rm -rf {} +

