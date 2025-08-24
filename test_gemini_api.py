#!/usr/bin/env python3
"""
Test script to verify Google Gemini API key
"""

import os
import sys

def test_api_key():
    # Get API key from environment variable or command line argument
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    if not api_key and len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    if not api_key:
        print("ERROR: No API key provided!")
        print("Usage: python test_api_key.py [API_KEY]")
        print("   Or: GOOGLE_API_KEY=your_key_here python test_api_key.py")
        return False
    
    print(f"API Key Length: {len(api_key)}")
    print(f"API Key (first 10 chars): {api_key[:10]}...")
    
    try:
        # Import the Google Generative AI library
        import google.generativeai as genai
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Test the API with a simple request
        print("Testing API connection...")
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Send a simple test prompt
        response = model.generate_content("Say 'Hello, World!' in 10 different languages.")
        
        if response.text:
            print("✓ API Key is valid and working!")
            print("✓ Successfully received response from Gemini API")
            return True
        else:
            print("✗ API Key test failed - no response received")
            return False
            
    except ImportError:
        print("✗ Google Generative AI library not installed")
        print("  Install it with: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"✗ API test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api_key()
    sys.exit(0 if success else 1)