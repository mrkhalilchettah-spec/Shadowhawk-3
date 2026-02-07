#!/bin/bash

# Setup Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r api/requirements.txt

# Setup Go dependencies
cd engine
go mod tidy
cd ..

echo "Setup complete. You can now start the API and Engine manually."
echo "Don't forget to set up your .env file and PostgreSQL/Redis."
