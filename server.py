"""
News Dashboard API Server

This is a simple Flask server that serves the news data to the frontend dashboard.
In production, you would deploy this on a platform like Heroku, Vercel, or similar.

Requirements:
- Python 3.6+
- Flask (pip install flask)
"""

try:
    from flask import Flask, jsonify, send_from_directory
    import os
    import json
    from datetime import datetime, timedelta
    FLASK_AVAILABLE = True
except ImportError:
    print("Flask not available. Running in static mode only.")
    FLASK_AVAILABLE = False
    # Create a mock Flask for static file serving
    class MockApp:
        def __init__(self, *args, **kwargs):
            pass
        def route(self, *args, **kwargs):
            return lambda f: f
    
    Flask = MockApp
    app = MockApp()
    
    def jsonify(data):
        import json
        return json.dumps(data), 200
        
    def send_from_directory(directory, path):
        # Simple static file serving
        if path == 'index.html':
            with open('index.html', 'r') as f:
                return f.read()
        else:
            with open(path, 'r') as f:
                return f.read()

# Serve static files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# Helper function to get latest data file
def get_latest_data_file(category):
    """Get the most recent data file for a category"""
    try:
        # List all files in data directory
        data_files = [f for f in os.listdir('data') if f.endswith(f'{category}.json')]
        if not data_files:
            return None
        
        # Sort by date (filename format: YYYY-MM-DD-category.json)
        data_files.sort(reverse=True)
        latest_file = data_files[0]
        return os.path.join('data', latest_file)
    except Exception as e:
        print(f"Error finding latest {category} file: {e}")
        return None

# API endpoints
@app.route('/api/healthcare')
def get_healthcare_news():
    """Get latest healthcare news"""
    try:
        # Try to get the latest data file
        data_file = get_latest_data_file('healthcare')
        
        if data_file and os.path.exists(data_file):
            # Load data from file
            with open(data_file, 'r') as f:
                data = json.load(f)
        else:
            # Fallback to sample data with new structure
            data = {
                "weekly_top_story": {
                    "headline": "Revolutionary CAR-T Cell Therapy Shows 90% Remission Rate in Pediatric Leukemia",
                    "summary": "A new CAR-T cell therapy targeting pediatric leukemia has demonstrated remarkable efficacy in Phase II trials, with 90% of patients achieving complete remission after six months.",
                    "source": "The Lancet",
                    "importance": 5,
                    "impact_to_me": 5,
                    "category": "Research",
                    "url": "https://www.thelancet.com/article"
                },
                "stories": [
                    {
                        "headline": "FDA Announces New Fast-Track Program for Gene Therapies",
                        "summary": "The FDA has unveiled a new expedited review pathway aimed at accelerating the approval of gene therapies for rare diseases, potentially cutting approval times by up to 50%.",
                        "source": "STAT News",
                        "importance": 5,
                        "impact_to_me": 4,
                        "category": "Policy",
                        "url": "https://www.statnews.com/fda-fast-track"
                    },
                    {
                        "headline": "AI Diagnostic Tool Achieves Radiologist-Level Accuracy",
                        "summary": "A new artificial intelligence system for detecting lung cancer on CT scans has matched or exceeded the diagnostic accuracy of experienced radiologists in a large clinical trial.",
                        "source": "NEJM",
                        "importance": 4,
                        "impact_to_me": 4,
                        "category": "Tech",
                        "url": "https://www.nejm.org/ai-diagnostic"
                    },
                    {
                        "headline": "Telehealth Reimbursement Rules Expanded for Rural Areas",
                        "summary": "CMS has expanded Medicare reimbursement for telehealth services in rural communities, removing geographic restrictions that previously limited access to virtual care.",
                        "source": "Fierce Healthcare",
                        "importance": 4,
                        "impact_to_me": 3,
                        "category": "Policy",
                        "url": "https://www.fiercehealthcare.com/telehealth"
                    }
                ]
            }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/general')
def get_general_news():
    """Get latest general news"""
    try:
        # Try to get the latest data file
        data_file = get_latest_data_file('general')
        
        if data_file and os.path.exists(data_file):
            # Load data from file
            with open(data_file, 'r') as f:
                data = json.load(f)
        else:
            # Fallback to sample data with new structure
            data = {
                "weekly_top_story": {
                    "headline": "Breakthrough in Nuclear Fusion Energy Achieved",
                    "summary": "Scientists at a major research facility have achieved a net energy gain in nuclear fusion, bringing humanity one step closer to unlimited clean energy.",
                    "source": "AP News",
                    "importance": 5,
                    "impact_to_me": 5,
                    "category": "Science",
                    "url": "https://www.apnews.com/fusion-energy"
                },
                "stories": [
                    {
                        "headline": "Quantum Supremacy Claimed by Three Major Tech Companies",
                        "summary": "Google, IBM, and a leading Chinese tech firm have simultaneously announced they've achieved quantum supremacy, solving complex problems in minutes that would take traditional supercomputers millennia.",
                        "source": "The Economist",
                        "importance": 5,
                        "impact_to_me": 5,
                        "category": "Technology",
                        "url": "https://www.economist.com/quantum-supremacy"
                    },
                    {
                        "headline": "Global AI Regulation Framework Agreed by G7 Nations",
                        "summary": "G7 countries have reached a preliminary agreement on a unified framework for AI governance, establishing new standards for transparency and safety in artificial intelligence development.",
                        "source": "Reuters",
                        "importance": 5,
                        "impact_to_me": 4,
                        "category": "Global",
                        "url": "https://www.reuters.com/ai-regulation"
                    },
                    {
                        "headline": "Renewable Energy Investments Surpass Fossil Fuels for First Time",
                        "summary": "Global investment in renewable energy projects has exceeded fossil fuel investments for the first time in history, signaling a major shift in the energy sector's trajectory.",
                        "source": "BBC",
                        "importance": 4,
                        "impact_to_me": 3,
                        "category": "Business",
                        "url": "https://www.bbc.com/renewable-energy"
                    }
                ]
            }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/latest')
def get_latest_news():
    """Get both healthcare and general news"""
    try:
        # In a real implementation, you would fetch the latest data
        # For now, we'll return sample data for both with new structure
        healthcare_data = {
            "weekly_top_story": {
                "headline": "Revolutionary CAR-T Cell Therapy Shows 90% Remission Rate in Pediatric Leukemia",
                "summary": "A new CAR-T cell therapy targeting pediatric leukemia has demonstrated remarkable efficacy in Phase II trials, with 90% of patients achieving complete remission after six months.",
                "source": "The Lancet",
                "importance": 5,
                "impact_to_me": 5,
                "category": "Research",
                "url": "https://www.thelancet.com/article"
            },
            "stories": [
                {
                    "headline": "FDA Announces New Fast-Track Program for Gene Therapies",
                    "summary": "The FDA has unveiled a new expedited review pathway aimed at accelerating the approval of gene therapies for rare diseases, potentially cutting approval times by up to 50%.",
                    "source": "STAT News",
                    "importance": 5,
                    "impact_to_me": 4,
                    "category": "Policy",
                    "url": "https://www.statnews.com/fda-fast-track"
                },
                {
                    "headline": "AI Diagnostic Tool Achieves Radiologist-Level Accuracy",
                    "summary": "A new artificial intelligence system for detecting lung cancer on CT scans has matched or exceeded the diagnostic accuracy of experienced radiologists in a large clinical trial.",
                    "source": "NEJM",
                    "importance": 4,
                    "impact_to_me": 4,
                    "category": "Tech",
                    "url": "https://www.nejm.org/ai-diagnostic"
                },
                {
                    "headline": "Telehealth Reimbursement Rules Expanded for Rural Areas",
                    "summary": "CMS has expanded Medicare reimbursement for telehealth services in rural communities, removing geographic restrictions that previously limited access to virtual care.",
                    "source": "Fierce Healthcare",
                    "importance": 4,
                    "impact_to_me": 3,
                    "category": "Policy",
                    "url": "https://www.fiercehealthcare.com/telehealth"
                }
            ]
        }
        
        general_data = {
            "weekly_top_story": {
                "headline": "Breakthrough in Nuclear Fusion Energy Achieved",
                "summary": "Scientists at a major research facility have achieved a net energy gain in nuclear fusion, bringing humanity one step closer to unlimited clean energy.",
                "source": "AP News",
                "importance": 5,
                "impact_to_me": 5,
                "category": "Science",
                "url": "https://www.apnews.com/fusion-energy"
            },
            "stories": [
                {
                    "headline": "Quantum Supremacy Claimed by Three Major Tech Companies",
                    "summary": "Google, IBM, and a leading Chinese tech firm have simultaneously announced they've achieved quantum supremacy, solving complex problems in minutes that would take traditional supercomputers millennia.",
                    "source": "The Economist",
                    "importance": 5,
                    "impact_to_me": 5,
                    "category": "Technology",
                    "url": "https://www.economist.com/quantum-supremacy"
                },
                {
                    "headline": "Global AI Regulation Framework Agreed by G7 Nations",
                    "summary": "G7 countries have reached a preliminary agreement on a unified framework for AI governance, establishing new standards for transparency and safety in artificial intelligence development.",
                    "source": "Reuters",
                    "importance": 5,
                    "impact_to_me": 4,
                    "category": "Global",
                    "url": "https://www.reuters.com/ai-regulation"
                },
                {
                    "headline": "Renewable Energy Investments Surpass Fossil Fuels for First Time",
                    "summary": "Global investment in renewable energy projects has exceeded fossil fuel investments for the first time in history, signaling a major shift in the energy sector's trajectory.",
                    "source": "BBC",
                    "importance": 4,
                    "impact_to_me": 3,
                    "category": "Business",
                    "url": "https://www.bbc.com/renewable-energy"
                }
            ]
        }
        
        return jsonify({
            "healthcare": healthcare_data,
            "general": general_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__' and FLASK_AVAILABLE:
    app.run(debug=True, host='0.0.0.0', port=5000)
elif __name__ == '__main__':
    print("Flask not available. Please install Flask to run the server:")
    print("pip install flask")
    print("\nFor GitHub Pages deployment, simply serve the static files directly.")