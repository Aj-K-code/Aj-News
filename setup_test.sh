#!/bin/bash

echo "=== The Signal - News Dashboard Setup and Test ==="
echo

echo "1. Checking directory structure..."
if [ ! -d "/home/aj/news-dashboard" ]; then
  echo "ERROR: Project directory not found"
  exit 1
fi

cd /home/aj/news-dashboard

echo "2. Checking required files..."
REQUIRED_FILES=("index.html" "css/styles.css" "js/main.js" "server.py" "backend.py" "requirements.txt" "README.md")
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "ERROR: Required file $file not found"
    exit 1
  fi
done

echo "✓ All required files present"

echo "3. Checking data directory..."
if [ ! -d "data" ]; then
  echo "Creating data directory..."
  mkdir data
fi

echo "4. Checking sample data files..."
SAMPLE_FILES=("data/2025-08-23-healthcare.json" "data/2025-08-23-general.json")
for file in "${SAMPLE_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "Note: Sample data file $file not found (will be created by backend script)"
  fi
done

echo "5. Verifying GitHub Pages workflow..."
if [ ! -f ".github/workflows/pages.yml" ]; then
  echo "ERROR: GitHub Pages workflow not found"
  exit 1
fi

echo "✓ GitHub Pages workflow present"

echo
echo "=== Setup Complete ==="
echo
echo "To run and test the application:"
echo
echo "1. For local testing with sample data only:"
echo "   python3 simple_server.py"
echo "   Then open http://localhost:8000 in your browser"
echo
echo "2. For full functionality with Perplexity API:"
echo "   pip3 install -r requirements.txt"
echo "   export PERPLEXITY_API_KEY='your-api-key-here'"
echo "   python3 backend.py"
echo "   python3 server.py"
echo "   Then open http://localhost:5000 in your browser"
echo
echo "3. For GitHub Pages deployment:"
echo "   - Push to your GitHub repository"
echo "   - Enable GitHub Pages in repository settings"
echo "   - The site will be available at https://<username>.github.io/<repository>/"
echo
echo "To add your Perplexity API key:"
echo "1. Get an API key from https://www.perplexity.ai/"
echo "2. Set it as an environment variable:"
echo "   export PERPLEXITY_API_KEY='your-actual-api-key-here'"
echo "3. Run the backend script to fetch real data:"
echo "   python3 backend.py"