#!/bin/bash
# Test Google Gemini API Key

echo "Testing Google Gemini API Key..."

# Check if API key is provided as argument
if [ $# -eq 0 ]; then
    echo "Usage: ./test_api.sh YOUR_API_KEY"
    echo "   Or: GOOGLE_API_KEY=your_key_here ./test_api.sh"
    exit 1
fi

# Use provided API key or environment variable
API_KEY=${1:-$GOOGLE_API_KEY}

if [ -z "$API_KEY" ]; then
    echo "ERROR: No API key provided!"
    exit 1
fi

# Export the API key as environment variable
export GOOGLE_API_KEY="$API_KEY"

# Run the Python test script
python3 test_gemini_api.py