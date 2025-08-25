"""
News Dashboard Backend Script

This script fetches news data from Google Gemini API and stores it for the dashboard.
Schedule this to run daily (e.g., using cron) to keep your dashboard updated.

Requirements:
- Python 3.6+
- google-generativeai library (pip install google-generativeai)
"""

import google.generativeai as genai
import json
import os
import configparser
from datetime import datetime

def load_env_file(filepath):
    \"\"\"Load environment variables from a .env file\"\"\"
    if not os.path.exists(filepath):
        return
    
    config = configparser.ConfigParser()
    # Read the file as a single section
    with open(filepath, 'r') as f:
        config.read_string('[DEFAULT]\\n' + f.read())
    
    # Set environment variables if they're not already set
    for key, value in config['DEFAULT'].items():
        if not os.environ.get(key.upper()):
            os.environ[key.upper()] = value

# Load .env file if it exists
env_file = os.path.join(os.path.dirname(__file__), '.env')
load_env_file(env_file)

# Configuration
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')  # Set your API key as an environment variable
genai.configure(api_key=GOOGLE_API_KEY)

# Check if API key is set
if not GOOGLE_API_KEY:
    print("WARNING: GOOGLE_API_KEY not set. Using sample data only.")
    print("To use the Google Gemini API, set the GOOGLE_API_KEY environment variable.")
else:
    print("GOOGLE_API_KEY is set. Will attempt to fetch real data from Google Gemini API.")

# Healthcare prompt
HEALTHCARE_PROMPT = """
Act as an expert healthcare industry analyst. Generate a daily briefing for a busy healthcare professional.
Aggregate the most significant healthcare stories from the last 24 hours and the top story from the last week.

The output MUST be a valid JSON object with the following structure:
{
  "weekly_top_story": {
    "headline": "The headline of the most important story from the past week",
    "summary": "A concise, one-sentence summary explaining what happened and why it matters",
    "source": "The name of the news source",
    "importance": 5,
    "impact_to_me": 5,
    "category": "Research",
    "url": "https://example.com/article"
  },
  "stories": [
    {
      "headline": "The headline of a significant story from the last 24 hours",
      "summary": "A concise, one-sentence summary explaining what happened and why it matters",
      "source": "The name of the news source",
      "importance": 4,
      "impact_to_me": 3,
      "category": "Policy",
      "url": "https://example.com/article"
    }
  ]
}

Instructions:
1. "weekly_top_story": The single most important healthcare story from the past week (can be from any time in the past 7 days)
2. "stories": An array of 1-3 objects representing the most significant healthcare stories from the last 24 hours

For each story in "stories":
- "headline": The original story headline
- "summary": A concise, one-sentence summary explaining what happened and why it matters
- "source": The name of the news source
- "importance": An integer from 1 to 5, rating the story's overall significance:
   * 5 - Exceptional global significance (e.g., cure for major disease, breakthrough technology that will change everything)
   * 4 - Major significance (e.g., important policy changes, significant scientific advancement)
   * 3 - Moderate significance (e.g., notable industry developments, regional policy changes)
   * 2 - Minor significance (e.g., company announcements, small regulatory changes)
   * 1 - Minimal significance (e.g., minor updates, routine news)
- "impact_to_me": An integer from 1 to 5, rating the story's direct relevance and potential impact on a healthcare professional:
   * 5 - Direct and significant impact on practice/patients
   * 4 - Important for professional development/awareness
   * 3 - Moderate relevance to work
   * 2 - Minor relevance or indirect impact
   * 1 - Minimal professional relevance
- "category": A single-word category from the following list: "Policy", "Pharma", "Research", "Tech", "Business"
- "url": A URL to the original article

Make sure to provide valid URLs for all articles. Use your knowledge of recent healthcare news to provide accurate information.
"""

# General news prompt
GENERAL_NEWS_PROMPT = """
Act as a world news synthesizer. Generate a daily briefing for a well-informed individual who wants to stay updated on major global developments but avoid day-to-day political drama.
Aggregate the most significant global news stories from the last 24 hours and the top story from the last week.

The output MUST be a valid JSON object with the following structure:
{
  "weekly_top_story": {
    "headline": "The headline of the most important story from the past week",
    "summary": "A concise, one-sentence summary explaining the event and its broader implications",
    "source": "The name of the news source",
    "importance": 5,
    "impact_to_me": 5,
    "category": "Science",
    "url": "https://example.com/article"
  },
  "stories": [
    {
      "headline": "The headline of a significant story from the last 24 hours",
      "summary": "A concise, one-sentence summary explaining the event and its broader implications",
      "source": "The name of the news source",
      "importance": 4,
      "impact_to_me": 3,
      "category": "Technology",
      "url": "https://example.com/article"
    }
  ]
}

Instructions:
1. "weekly_top_story": The single most important global news story from the past week (can be from any time in the past 7 days)
2. "stories": An array of 1-3 objects representing the most significant global news stories from the last 24 hours

For each story in "stories":
- "headline": The original story headline
- "summary": A concise, one-sentence summary explaining the event and its broader implications
- "source": The name of the news source
- "importance": An integer from 1 to 5, rating the story's global significance:
   * 5 - Exceptional global significance (e.g., major geopolitical events, groundbreaking scientific discoveries)
   * 4 - Major significance (e.g., important international agreements, significant technological advances)
   * 3 - Moderate significance (e.g., notable economic shifts, regional developments)
   * 2 - Minor significance (e.g., company news, local developments)
   * 1 - Minimal significance (e.g., routine updates, minor announcements)
- "impact_to_me": An integer from 1 to 5, rating the story's potential impact on a typical person's life, finances, or worldview:
   * 5 - Direct and significant impact on daily life/finances
   * 4 - Important for general awareness and planning
   * 3 - Moderate relevance to personal life
   * 2 - Minor relevance or indirect impact
   * 1 - Minimal personal relevance
- "category": A single-word category from the following list: "Technology", "Business", "Science", "Global", "Culture"
- "url": A URL to the original article

Make sure to provide valid URLs for all articles. Use your knowledge of recent global news to provide accurate information.
"""

def fetch_news_gemini(prompt, filename):
    """Fetch news from Google Gemini API and save to file"""
    # If no API key, return None to use sample data
    if not GOOGLE_API_KEY:
        return None
    
    try:
        print(f"Fetching data from Google Gemini API...")
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        
        # Extract and parse JSON
        content = response.text
        
        # Parse JSON (Gemini sometimes includes markdown formatting)
        if content.startswith('```json'):
            content = content[7:]  # Remove ```json
        if content.endswith('```'):
            content = content[:-3]  # Remove ```
        
        # Parse and validate JSON
        news_data = json.loads(content)
        
        # Validate required fields
        required_fields = ['weekly_top_story', 'stories']
        for field in required_fields:
            if field not in news_data:
                raise ValueError(f"Invalid response format: missing required field '{field}'")
        
        # Save to file with today's date
        with open(filename, 'w') as f:
            json.dump(news_data, f, indent=2)
            
        print(f"Successfully saved {filename}")
        return news_data
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response content: {content}")
        return None
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def main():
    """Main function to fetch both healthcare and general news"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch healthcare news
    print("Fetching healthcare news...")
    healthcare_file = f"data/{today}-healthcare.json"
    healthcare_data = fetch_news_gemini(HEALTHCARE_PROMPT, healthcare_file)
    
    # If API call failed, save sample data
    if healthcare_data is None:
        print("Using sample healthcare data...")
        with open(healthcare_file, 'w') as f:
            json.dump(sample_healthcare_data(), f, indent=2)
        print(f"Saved sample data to {healthcare_file}")
    
    # Fetch general news
    print("Fetching general news...")
    general_file = f"data/{today}-general.json"
    general_data = fetch_news_gemini(GENERAL_NEWS_PROMPT, general_file)
    
    # If API call failed, save sample data
    if general_data is None:
        print("Using sample general data...")
        with open(general_file, 'w') as f:
            json.dump(sample_general_data(), f, indent=2)
        print(f"Saved sample data to {general_file}")
    
    print("News fetching complete!")

def sample_healthcare_data():
    """Return sample healthcare data with the new structure"""
    return {
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
                "importance": 4,
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
                "importance": 3,
                "impact_to_me": 3,
                "category": "Policy",
                "url": "https://www.fiercehealthcare.com/telehealth"
            }
        ]
    }

def sample_general_data():
    """Return sample general data with the new structure"""
    return {
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
                "importance": 4,
                "impact_to_me": 4,
                "category": "Technology",
                "url": "https://www.economist.com/quantum-supremacy"
            },
            {
                "headline": "Global AI Regulation Framework Agreed by G7 Nations",
                "summary": "G7 countries have reached a preliminary agreement on a unified framework for AI governance, establishing new standards for transparency and safety in artificial intelligence development.",
                "source": "Reuters",
                "importance": 4,
                "impact_to_me": 3,
                "category": "Global",
                "url": "https://www.reuters.com/ai-regulation"
            },
            {
                "headline": "Renewable Energy Investments Surpass Fossil Fuels for First Time",
                "summary": "Global investment in renewable energy projects has exceeded fossil fuel investments for the first time in history, signaling a major shift in the energy sector's trajectory.",
                "source": "BBC",
                "importance": 4,
                "impact_to_me": 4,
                "category": "Business",
                "url": "https://www.bbc.com/renewable-energy"
            }
        ]
    }

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    main()