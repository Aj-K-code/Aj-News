"""
Test script to verify Google Gemini API key and basic functionality
"""

import os
import sys
import configparser
import google.generativeai as genai

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
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    print("ERROR: GOOGLE_API_KEY not set.")
    print("Please set the GOOGLE_API_KEY environment variable or add it to .env file.")
    sys.exit(1)

try:
    # Configure the API
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Test the API with a simple request
    print("Testing API connection...")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # Send a simple test prompt
    response = model.generate_content("Say 'Hello, World!' in 10 different languages.")
    
    if response.text:
        print("✓ API Key is valid and working!")
        print("✓ Successfully received response from Gemini API")
        print("\nResponse:")
        print(response.text)
        sys.exit(0)
    else:
        print("✗ API Key test failed - no response received")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ API test failed with error: {str(e)}")
    sys.exit(1)