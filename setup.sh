#!/bin/bash

# Exit on error
set -e

echo "Setting up the project environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r python/requirements.txt

# Optional: Upgrade pip
pip install --upgrade pip

echo ""
echo "Setup complete! You can activate the virtual environment with:"
echo "source venv/bin/activate"
echo ""
echo "To deactivate the virtual environment when you're done, run:"
echo "deactivate" 