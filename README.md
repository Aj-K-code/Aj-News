# AJ's News in a Flash - Daily Briefing

<p align="center">
  <a href="https://aj-k-code.github.io/Aj-News/">
    <img src="https://img.shields.io/badge/LIVE%20DEMO-Visit%20Site-red?style=for-the-badge&logo=github&logoColor=white" alt="Live Demo">
  </a>
</p>

<p align="center">
  <a href="https://aj-k-code.github.io/Aj-News/">
    <img src="https://img.shields.io/badge/%F0%9F%9A%80%20CLICK%20HERE%20TO%20VIEW%20LIVE%20SITE%20%E2%9A%A1-000000?style=for-the-badge&logo=firefox&logoColor=FF7139" alt="Click here to view live site">
  </a>
</p>

<p align="center">
  <a href="https://aj-k-code.github.io/Aj-News/">
    <img src="https://img.shields.io/badge/%F0%9F%94%A5%20VIEW%20LIVE%20DEMO%20%E2%9A%A1-4CAF50?style=for-the-badge&logo=googlechrome&logoColor=white" alt="View Live Demo">
  </a>
</p>

---

A modern, minimalist dashboard that delivers the most important news in under 60 seconds - personalized for AJ. This project provides a clean interface for viewing curated healthcare and general news with visual indicators for importance and personal impact.

## 🔗 Live Demo

**View the live site:** [https://aj-k-code.github.io/Aj-News/](https://aj-k-code.github.io/Aj-News/)

> ⚡ **Note:** The site updates daily with fresh news content at 5:00 AM UTC

## Features

- **Dual Views**: Toggle between Healthcare and General News
- **Weekly Top Story**: Highlight of the most significant story from the past week
- **Essential Daily News**: 1-3 most important stories from the last 24 hours
- **Visual Ratings**: Importance (stars) and Impact (signal strength bars) with realistic scoring
- **Direct Links**: All stories include links to original sources
- **No-Scroll Design**: Entire dashboard designed to be readable without scrolling
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, animated interface with skeleton loading states
- **Category Tags**: Color-coded categories for quick scanning
- **API Integration**: Connects to Perplexity AI for real-time news curation
- **GitHub Pages Deployment**: Ready for easy deployment
- **Caching**: Data cached daily to minimize API calls

## Prerequisites

- Python 3.6+
- Node.js and npm (for local testing server, optional)

## Setup and Testing

### Quick Start (Sample Data Mode)

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd news-dashboard
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```bash
   python server.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

### Using Perplexity API (Optional)

To use the Perplexity API for real data:

1. Get an API key from [Perplexity AI](https://www.perplexity.ai/)

2. Set the API key as an environment variable:
   ```bash
   export PERPLEXITY_API_KEY="your-api-key-here"
   ```
   
   On Windows:
   ```cmd
   set PERPLEXITY_API_KEY=your-api-key-here
   ```

3. Install the required dependency:
   ```bash
   pip install requests
   ```

4. Run the backend script to fetch data:
   ```bash
   python backend.py
   ```

5. Start the server:
   ```bash
   python server.py
   ```

### Testing the Application

1. **Local Testing**:
   - Follow the steps above to run locally
   - Toggle between Healthcare and General News tabs
   - Verify that data loads correctly

2. **Without API Key**:
   - The application will automatically fall back to sample data
   - All UI elements should work correctly
   - No configuration needed

3. **With API Key**:
   - Data will be fetched from Perplexity API
   - Real-time news will be displayed
   - Files will be saved to the `data/` directory

## Deployment to GitHub Pages

This project is configured to automatically deploy to GitHub Pages using GitHub Actions. To set it up:

1. Fork this repository or create a new repository with these files

2. Go to your repository settings on GitHub

3. Navigate to "Pages" in the left sidebar

4. Under "Source", select "GitHub Actions"

5. The deployment workflow will automatically run and deploy your site

6. Your site will be available at `https://<your-username>.github.io/<repository-name>/`

Note: The first deployment may take a few minutes. After that, the site will automatically update whenever you push changes to the main branch.

## Automatic Daily Updates

This repository includes GitHub Actions workflows that automatically fetch new news data once per day and deploy the site to GitHub Pages.

### Deployment Workflow
- Automatically runs on pushes to the main branch
- Deploys the static site to GitHub Pages

### News Update Workflow
- Runs daily at 5:00 AM UTC (12:00 AM EST)
- Uses the Perplexity API to fetch healthcare and general news
- Saves the data as JSON files in the `data/` directory
- Automatically updates an index file to track available data files
- Commits and pushes the updated files to your repository

To enable automatic updates:

1. Get a Perplexity API key from [Perplexity AI](https://www.perplexity.ai/)
2. In your GitHub repository, go to Settings > Secrets and variables > Actions
3. Create a new repository secret named `PERPLEXITY_API_KEY` with your API key as the value
4. The workflows will run automatically at the scheduled time

This approach ensures that:
- Only one API call is made per day (not per user visit)
- All users see the same up-to-date content
- API costs are minimized
- The dashboard loads quickly for all users
- The site works completely statically on GitHub Pages without any backend

## Perplexity Prompts

### Healthcare News Prompt

```
Act as an expert healthcare industry analyst. Generate a daily briefing for a busy healthcare professional.
Aggregate the most significant healthcare stories from the last 24 hours and the top story from the last week.
CRITICAL: Focus ONLY on news from the last 7 days. Search for genuinely recent developments in healthcare.

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
1. "weekly_top_story": The single most important healthcare story from the past week (must be from the last 7 days, NOT older)
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
- "url": A REAL, VERIFIABLE URL to the original article (NOT a placeholder)

IMPORTANT: 
1. All URLs must be real, working links to actual news articles published within the specified timeframes.
2. Do NOT include news from before last week, even if it seems important.
3. Focus on genuinely recent developments in healthcare.
4. Use the Perplexity API to search for and verify current news stories.
```

### General News Prompt

```
Act as a world news synthesizer. Generate a daily briefing for a well-informed individual who wants to stay updated on major global developments but avoid day-to-day political drama.
Aggregate the most significant global news stories from the last 24 hours and the top story from the last week.
CRITICAL: Focus ONLY on news from the last 7 days. Search for genuinely recent developments in global news.

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
1. "weekly_top_story": The single most important global news story from the past week (must be from the last 7 days, NOT older)
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
- "url": A REAL, VERIFIABLE URL to the original article (NOT a placeholder)

IMPORTANT:
1. All URLs must be real, working links to actual news articles published within the specified timeframes.
2. Do NOT include news from before last week, even if it seems important.
3. Focus on genuinely recent developments in global news.
4. Use the Perplexity API to search for and verify current news stories.
```

## Project Structure

```
news-dashboard/
├── index.html          # Main HTML file
├── css/styles.css      # Styling
├── js/main.js          # Frontend JavaScript
├── server.py           # Flask backend server
├── backend.py          # Perplexity API integration script
├── requirements.txt    # Python dependencies
├── data/               # Directory for storing news data files
├── .github/workflows/  # GitHub Actions for deployment and updates
└── README.md           # This file
```

## Technologies Used

- HTML5
- CSS3 (with modern features like CSS variables and flexbox/grid)
- JavaScript (Vanilla ES6+)
- Python/Flask (Backend)
- Google Fonts (Inter and Space Grotesk)
- Font Awesome icons
- Perplexity AI (News Curation)
- GitHub Actions (Deployment and Daily Updates)

## License

MIT License