"""
Simple test script to verify the news dashboard server is working correctly.
"""

import requests
import time

def test_server():
    """Test the server endpoints"""
    base_url = "http://localhost:5000"
    
    print("Testing news dashboard server...")
    
    # Test main page
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✓ Main page loads correctly")
        else:
            print(f"✗ Main page failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Failed to load main page: {e}")
        return
    
    # Test healthcare API
    try:
        response = requests.get(f"{base_url}/api/healthcare")
        if response.status_code == 200:
            data = response.json()
            if "daily_take" in data and "stories" in data:
                print("✓ Healthcare API returns valid data")
            else:
                print("✗ Healthcare API response missing required fields")
        else:
            print(f"✗ Healthcare API failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Failed to test healthcare API: {e}")
    
    # Test general API
    try:
        response = requests.get(f"{base_url}/api/general")
        if response.status_code == 200:
            data = response.json()
            if "daily_take" in data and "stories" in data:
                print("✓ General API returns valid data")
            else:
                print("✗ General API response missing required fields")
        else:
            print(f"✗ General API failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Failed to test general API: {e}")

if __name__ == "__main__":
    test_server()