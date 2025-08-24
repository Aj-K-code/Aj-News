// API endpoint configuration
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
  ? 'http://localhost:5000' 
  : ''; // For GitHub Pages, use relative paths

// Sample healthcare data for testing (fallback) with more realistic ratings
const sampleHealthcareData = {
  "weekly_top_story": {
    "headline": "Revolutionary CAR-T Cell Therapy Shows 90% Remission Rate in Pediatric Leukemia",
    "summary": "A new CAR-T cell therapy targeting pediatric leukemia has demonstrated remarkable efficacy in Phase II trials, with 90% of patients achieving complete remission after six months.",
    "source": "The Lancet",
    "importance": 5, // Reserved for major breakthroughs like this
    "impact_to_me": 5, // Direct impact on healthcare professionals
    "category": "Research",
    "url": "https://www.thelancet.com/article"
  },
  "stories": [
    {
      "headline": "FDA Announces New Fast-Track Program for Gene Therapies",
      "summary": "The FDA has unveiled a new expedited review pathway aimed at accelerating the approval of gene therapies for rare diseases, potentially cutting approval times by up to 50%.",
      "source": "STAT News",
      "importance": 4, // Significant but not world-changing
      "impact_to_me": 4, // Important for healthcare professionals
      "category": "Policy",
      "url": "https://www.statnews.com/fda-fast-track"
    },
    {
      "headline": "AI Diagnostic Tool Achieves Radiologist-Level Accuracy",
      "summary": "A new artificial intelligence system for detecting lung cancer on CT scans has matched or exceeded the diagnostic accuracy of experienced radiologists in a large clinical trial.",
      "source": "NEJM",
      "importance": 4, // Technologically significant
      "impact_to_me": 4, // Relevant to medical professionals
      "category": "Tech",
      "url": "https://www.nejm.org/ai-diagnostic"
    },
    {
      "headline": "Telehealth Reimbursement Rules Expanded for Rural Areas",
      "summary": "CMS has expanded Medicare reimbursement for telehealth services in rural communities, removing geographic restrictions that previously limited access to virtual care.",
      "source": "Fierce Healthcare",
      "importance": 3, // Important but not groundbreaking
      "impact_to_me": 3, // Moderate impact on healthcare professionals
      "category": "Policy",
      "url": "https://www.fiercehealthcare.com/telehealth"
    }
  ]
};

// Sample general news data for testing (fallback) with more realistic ratings
const sampleGeneralData = {
  "weekly_top_story": {
    "headline": "Breakthrough in Nuclear Fusion Energy Achieved",
    "summary": "Scientists at a major research facility have achieved a net energy gain in nuclear fusion, bringing humanity one step closer to unlimited clean energy.",
    "source": "AP News",
    "importance": 5, // Reserved for major breakthroughs like this
    "impact_to_me": 5, // Significant impact on everyone
    "category": "Science",
    "url": "https://www.apnews.com/fusion-energy"
  },
  "stories": [
    {
      "headline": "Quantum Supremacy Claimed by Three Major Tech Companies",
      "summary": "Google, IBM, and a leading Chinese tech firm have simultaneously announced they've achieved quantum supremacy, solving complex problems in minutes that would take traditional supercomputers millennia.",
      "source": "The Economist",
      "importance": 4, // Significant technological advancement
      "impact_to_me": 4, // Will affect tech industry and future developments
      "category": "Technology",
      "url": "https://www.economist.com/quantum-supremacy"
    },
    {
      "headline": "Global AI Regulation Framework Agreed by G7 Nations",
      "summary": "G7 countries have reached a preliminary agreement on a unified framework for AI governance, establishing new standards for transparency and safety in artificial intelligence development.",
      "source": "Reuters",
      "importance": 4, // Important policy development
      "impact_to_me": 3, // Moderate impact on general population
      "category": "Global",
      "url": "https://www.reuters.com/ai-regulation"
    },
    {
      "headline": "Renewable Energy Investments Surpass Fossil Fuels for First Time",
      "summary": "Global investment in renewable energy projects has exceeded fossil fuel investments for the first time in history, signaling a major shift in the energy sector's trajectory.",
      "source": "BBC",
      "importance": 4, // Significant economic/environmental shift
      "impact_to_me": 4, // Affects everyone long-term
      "category": "Business",
      "url": "https://www.bbc.com/renewable-energy"
    }
  ]
};

// DOM Elements
const healthTab = document.getElementById('health-tab');
const generalTab = document.getElementById('general-tab');
const newsGrid = document.getElementById('news-grid');
const currentDateElement = document.getElementById('current-date');
const weeklyCard = document.getElementById('weekly-card');

// Set current date
const now = new Date();
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
currentDateElement.textContent = now.toLocaleDateString('en-US', options);

// Tab switching functionality
healthTab.addEventListener('click', () => {
  setActiveTab('healthcare');
});

generalTab.addEventListener('click', () => {
  setActiveTab('general');
});

function setActiveTab(tab) {
  // Update tab buttons
  if (tab === 'healthcare') {
    healthTab.classList.add('active');
    generalTab.classList.remove('active');
  } else {
    generalTab.classList.add('active');
    healthTab.classList.remove('active');
  }
  
  // Load appropriate data
  loadData(tab);
}

// Generate star ratings (adjusted for more realistic scoring)
function generateStars(rating) {
  let stars = '';
  // Adjust ratings: 5 is reserved for truly exceptional events
  const adjustedRating = rating >= 5 ? 5 : rating <= 1 ? 1 : rating;
  for (let i = 1; i <= 5; i++) {
    stars += `<span class="star ${i <= adjustedRating ? 'filled' : ''}"><i class="fas fa-star"></i></span>`;
  }
  return stars;
}

// Generate impact bars (adjusted for more realistic scoring)
function generateImpactBar(rating) {
  let bars = '';
  // Adjust ratings: 5 is reserved for truly exceptional events
  const adjustedRating = rating >= 5 ? 5 : rating <= 1 ? 1 : rating;
  for (let i = 1; i <= 5; i++) {
    bars += `<div class="impact-segment ${i <= adjustedRating ? 'active' : ''}"></div>`;
  }
  return bars;
}

// Render weekly top story
function renderWeeklyStory(story) {
  weeklyCard.innerHTML = `
    <span class="category-tag category-${story.category}">${story.category}</span>
    <h3 class="headline"><a href="${story.url}" target="_blank">${story.headline}</a></h3>
    <p class="summary">${story.summary}</p>
    <div class="card-footer">
      <span class="source">${story.source}</span>
      <div class="ratings">
        <div class="importance">
          <div class="stars">
            ${generateStars(story.importance)}
          </div>
          <span class="rating-label">Importance</span>
        </div>
        <div class="impact">
          <div class="impact-bar">
            ${generateImpactBar(story.impact_to_me)}
          </div>
          <span class="rating-label">Impact</span>
        </div>
      </div>
    </div>
  `;
}

// Render news cards (top 3 daily stories)
function renderNewsCards(stories) {
  // Clear existing content but keep skeleton loaders for a moment
  setTimeout(() => {
    newsGrid.innerHTML = '';
    
    stories.forEach((story, index) => {
      // Add delay to create staggered animation effect
      setTimeout(() => {
        const card = document.createElement('article');
        card.className = 'news-card';
        card.innerHTML = `
          <span class="category-tag category-${story.category}">${story.category}</span>
          <h3 class="headline"><a href="${story.url}" target="_blank">${story.headline}</a></h3>
          <p class="summary">${story.summary}</p>
          <div class="card-footer">
            <span class="source">${story.source}</span>
            <div class="ratings">
              <div class="importance">
                <div class="stars">
                  ${generateStars(story.importance)}
                </div>
                <span class="rating-label">Importance</span>
              </div>
              <div class="impact">
                <div class="impact-bar">
                  ${generateImpactBar(story.impact_to_me)}
                </div>
                <span class="rating-label">Impact</span>
              </div>
            </div>
          </div>
        `;
        newsGrid.appendChild(card);
      }, 100 * index); // Stagger the animations
    });
  }, 500); // Brief delay to show loading state
}



// Fetch data from API
async function fetchData(category) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/${category}`);
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching ${category} news:`, error);
    // Fallback to sample data
    return category === 'healthcare' ? sampleHealthcareData : sampleGeneralData;
  }
}

// Load data function
async function loadData(category) {
  // Show loading state for all sections
  weeklyCard.innerHTML = `
    <div class="skeleton-weekly">
      <div class="skeleton-category"></div>
      <div class="skeleton-headline"></div>
      <div class="skeleton-summary"></div>
      <div class="skeleton-footer"></div>
    </div>
  `;
  
  newsGrid.innerHTML = `
    <div class="news-card skeleton">
      <div class="skeleton-category"></div>
      <div class="skeleton-headline"></div>
      <div class="skeleton-summary"></div>
      <div class="skeleton-footer"></div>
    </div>
    <div class="news-card skeleton">
      <div class="skeleton-category"></div>
      <div class="skeleton-headline"></div>
      <div class="skeleton-summary"></div>
      <div class="skeleton-footer"></div>
    </div>
    <div class="news-card skeleton">
      <div class="skeleton-category"></div>
      <div class="skeleton-headline"></div>
      <div class="skeleton-summary"></div>
      <div class="skeleton-footer"></div>
    </div>
  `;
  
  try {
    // Fetch data from API
    const data = await fetchData(category);
    
    // Render weekly top story
    renderWeeklyStory(data.weekly_top_story);
    
    // Sort stories by importance and render top 3 daily news cards
    const sortedStories = [...data.stories].sort((a, b) => b.importance - a.importance);
    renderNewsCards(sortedStories.slice(0, 3));
  } catch (error) {
    console.error('Error loading data:', error);
    
    // Fallback to sample data after a delay
    setTimeout(() => {
      const sampleData = category === 'healthcare' ? sampleHealthcareData : sampleGeneralData;
      
      // Render weekly top story
      renderWeeklyStory(sampleData.weekly_top_story);
      
      // Sort stories by importance and render top 3 daily news cards
      const sortedStories = [...sampleData.stories].sort((a, b) => b.importance - a.importance);
      renderNewsCards(sortedStories.slice(0, 3));
    }, 1500);
  }
}

// Initialize with healthcare data
document.addEventListener('DOMContentLoaded', () => {
  loadData('healthcare');
});
