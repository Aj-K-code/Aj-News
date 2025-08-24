import os
import sys

# Simulate GitHub Actions environment
if len(sys.argv) > 1 and sys.argv[1] == "simulate-github":
    os.environ['GOOGLE_API_KEY'] = 'simulated-key'
    print("Simulating GitHub Actions environment with API key")

print("GOOGLE_API_KEY environment variable:")
api_key = os.environ.get('GOOGLE_API_KEY', 'NOT SET')
print(f"Value: {api_key[:10] if api_key != 'NOT SET' else api_key}{'...' if len(api_key) > 10 else ''}")
print(f"Length: {len(api_key)}")

# Test importing the Google Generative AI library
try:
    import google.generativeai as genai
    print("Google Generative AI library imported successfully")
except ImportError as e:
    print(f"Failed to import Google Generative AI library: {e}")