#!/bin/bash

# RoofSpec Matcher Setup Script
# This script helps you set up the application quickly

echo "========================================="
echo "RoofSpec Matcher - Setup Script"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.10+ is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo ""
echo "Step 1: Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

echo ""
echo "Step 3: Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "Step 4: Setting up environment file..."
if [ -f ".env" ]; then
    echo ".env file already exists. Skipping..."
else
    cp .env.example .env
    echo "✅ .env file created from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit the .env file and add your API key!"
    echo "   You can use: nano .env"
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API key (OpenAI or Anthropic)"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the application: streamlit run app.py"
echo ""
echo "For testing PDF extraction: python test_extraction.py your_file.pdf"
echo ""
