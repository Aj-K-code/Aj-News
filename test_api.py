"""
Test script to verify Perplexity API key and basic functionality
"""

import os
import sys
import configparser
import requests

def load_env_file(filepath):
    """Load environment variables from a .env file"""
    if not os.path.exists(filepath):
        return
    
    config = configparser.ConfigParser()
    # Read the file as a single section
    with open(filepath, 'r') as f:
        config.read_string('[DEFAULT]\n' + f.read())
    
    # Set environment variables if they're not already set
    for key, value in config['DEFAULT'].items():
        if not os.environ.get(key.upper()):
            os.environ[key.upper()] = value

# Load .env file if it exists
env_file = os.path.join(os.path.dirname(__file__), '.env')
load_env_file(env_file)

# Get API key from environment variable
PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')

if not PERPLEXITY_API_KEY:
    print("ERROR: PERPLEXITY_API_KEY not set.")
    print("Please set the PERPLEXITY_API_KEY environment variable or add it to .env file.")
    sys.exit(1)

try:
    # Test the API with a simple request
    print("Testing API connection...")
    
    # Perplexity API endpoint
    url = "https://api.perplexity.ai/chat/completions"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Data payload
    data = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, World!' in 5 different languages."}
        ]
    }
    
    # Make the API request
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    if response.status_code == 200:
        print("✓ API Key is valid and working!")
        print("✓ Successfully received response from Perplexity API")
        print("\nResponse:")
        content = response.json()["choices"][0]["message"]["content"]
        print(content)
        sys.exit(0)
    else:
        print(f"✗ API Key test failed - status code: {response.status_code}")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ API test failed with error: {str(e)}")
    sys.exit(1)