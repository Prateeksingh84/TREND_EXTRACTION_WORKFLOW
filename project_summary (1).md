# 📊 Digital Marketing Trend Extraction System
## Complete Project Summary & Documentation

---

## 🎯 Project Overview

A fully automated Python-based system that monitors social media platforms, extracts trending topics relevant to digital marketing, analyzes sentiment using AI, and generates comprehensive reports with visualizations.

### Key Features
- ✅ Multi-platform monitoring (Google Trends, Reddit)
- ✅ AI-powered sentiment analysis (Google Gemini)
- ✅ Automatic trend categorization
- ✅ Beautiful PDF & HTML reports
- ✅ Data visualization with charts
- ✅ Historical data storage (SQLite)
- ✅ Customizable keywords and categories

---

## 📁 Complete File Structure

```
trend-extraction-system/
│
├── 📄 main.py                          # Main application (core logic)
├── 📄 setup.py                         # Installation & setup script
├── 📄 db_utils.py                      # Database management utilities
├── 📄 requirements.txt                 # Python dependencies
│
├── 📄 .env.example                     # Environment variables template
├── 📄 .env                             # Your API keys (create this)
│
├── 📄 README.md                        # Full documentation
├── 📄 QUICKSTART.md                    # 5-minute setup guide
├── 📄 PROJECT_SUMMARY.md               # This file
├── 📄 SAMPLE_TRENDS.md                 # Example trends analysis
│
├── 📄 trend-extraction.code-workspace  # VS Code workspace config
├── 📄 run.bat                          # Windows quick-run script
├── 📄 run.sh                           # Unix/Mac quick-run script
│
├── 📁 reports/                         # Generated reports (auto-created)
│   ├── trend_report_YYYYMMDD.pdf
│   └── trend_report_YYYYMMDD.html
│
├── 📁 charts/                          # Generated charts (auto-created)
│   ├── category_distribution.png
│   ├── platform_comparison.png
│   ├── sentiment_distribution.png
│   └── top_trends.png
│
└── 📄 trends_database.db               # SQLite database (auto-created)
```

---

## 🔧 Technical Architecture

### Core Components

#### 1. **Data Collection Layer**
- `GoogleTrendsMonitor`: Fetches trending data from Google Trends API
- `RedditMonitor`: Monitors subreddits for marketing discussions
- Implements rate limiting and error handling

#### 2. **Processing Layer**
- `SentimentAnalyzer`: AI-powered sentiment analysis using Gemini
- `TrendCategorizer`: Categorizes trends into marketing segments
- `DatabaseManager`: Stores and retrieves historical data

#### 3. **Visualization Layer**
- `VisualizationGenerator`: Creates charts using Matplotlib & Seaborn
  - Pie charts for category distribution
  - Bar charts for platform comparison
  - Histograms for sentiment analysis
  - Horizontal bar charts for top trends

#### 4. **Reporting Layer**
- `ReportGenerator`: Creates professional reports
  - PDF reports with ReportLab
  - HTML reports with inline CSS
  - Includes charts, tables, and insights

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Programming Language | Python 3.8+ | Core application logic |
| AI/ML | Google Gemini API | Sentiment analysis |
| Data Collection | pytrends, PRAW | API interactions |
| Data Storage | SQLite | Historical data |
| Visualization | Matplotlib, Seaborn | Chart generation |
| PDF Generation | ReportLab | PDF reports |
| Data Processing | Pandas, NumPy | Data manipulation |

---

## 📊 Data Flow Diagram

```
┌─────────────────┐
│  Data Sources   │
│  - Google       │
│  - Reddit       │
│  - Twitter (opt)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Collect   │
│  - Fetch trends │
│  - Rate limit   │
│  - Error handle │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Processing    │
│  - Categorize   │
│  - AI Sentiment │
│  - Score calc   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Storage       │
│  - SQLite DB    │
│  - Historical   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Visualization  │
│  - Generate     │
│  - Charts/Graphs│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Reports      │
│  - PDF/HTML     │
│  - Email (opt)  │
└─────────────────┘
```

---

## 🚀 Installation & Setup Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection
- Google Gemini API key

### Quick Setup (3 Steps)

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Configure API keys
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Step 3: Run the system
python main.py
```

### Detailed Setup

1. **Install Python Dependencies**
   ```bash
   python setup.py
   # OR manually:
   pip install google-generativeai pytrends praw matplotlib seaborn reportlab pandas numpy
   ```

2. **Get API Keys**
   
   **Google Gemini API (Required):**
   - Visit: https://makersuite.google.com/app/apikey
   - Create/Get API key
   - Add to `.env` file
   
   **Reddit API (Optional):**
   - Visit: https://www.reddit.com/prefs/apps
   - Create app (script type)
   - Get client ID and secret
   - Add to `.env` file

3. **Configure Environment**
   ```bash
   # Create .env file
   GEMINI_API_KEY=your_key_here
   REDDIT_CLIENT_ID=your_id_here
   REDDIT_CLIENT_SECRET=your_secret_here
   ```

---

## 💻 Usage Guide

### Basic Usage

```bash
# Run trend extraction
python main.py

# Manage database
python db_utils.py

# Quick run (Windows)
run.bat

# Quick run (Unix/Mac)
./run.sh
```

### Advanced Usage

**Custom Keywords:**
```python
# Edit main.py - Config class
MARKETING_KEYWORDS = [
    'your', 'custom', 'keywords'
]
```

**Custom Subreddits:**
```python
# In RedditMonitor.get_trending_topics()
subreddits = ['marketing', 'entrepreneur', 'startup']
```

**Custom Time Ranges:**
```python
# In GoogleTrendsMonitor.get_trending_topics()
timeframe = 'now 7-d'  # Last 7 days
timeframe = 'now 1-m'  # Last month
timeframe = 'today 3-m'  # Last 3 months
```

---

## 📈 Database Management

### Using db_utils.py

```bash
python db_utils.py
```

**Available Operations:**
1. View Recent Trends
2. View Statistics
3. Search by Keyword
4. Get Trending Keywords
5. Export to CSV
6. Clear Old Data
7. Backup Database

### Direct SQL Queries

```bash
sqlite3 trends_database.db

# View all trends
SELECT * FROM trends LIMIT 10;

# Count by platform
SELECT platform, COUNT(*) FROM trends GROUP BY platform;

# Get top trends
SELECT keyword, SUM(volume) as total 
FROM trends 
GROUP BY keyword 
ORDER BY total DESC 
LIMIT 20;
```

---

## 📊 Report Contents Breakdown

### PDF Report Sections

1. **Title Page**
   - Report title
   - Generation date
   - System branding

2. **Executive Summary**
   - Total trends analyzed
   - Time period covered
   - Key insights summary

3. **Key Metrics Table**
   - Total trends count
   - Most common category
   - Average sentiment score
   - Platforms monitored

4. **Visual Analysis** (Full Page Charts)
   - Category Distribution (Pie Chart)
   - Platform Comparison (Bar Chart)
   - Sentiment Distribution (Histogram)
   - Top Trends (Horizontal Bar)

5. **Top 20 Trends Table**
   - Rank, Keyword, Category
   - Platform, Score
   - Sortable data

### HTML Report Features

- Responsive design
- Interactive elements
- Embedded charts
- Clean, professional styling
- Printable format
- Browser-compatible

---

## 🎨 Customization Options

### Visual Customization

**Change Color Schemes:**
```python
# In VisualizationGenerator
sns.set_palette("husl")  # Default
sns.set_palette("Set2")  # Alternative
sns.set_palette("pastel")  # Soft colors
```

**Chart Styles:**
```python
sns.set_style("whitegrid")  # Default
sns.set_style("darkgrid")
sns.set_style("white")
sns.set_style("dark")
```

### Report Customization

**PDF Report:**
```python
# Edit ReportGenerator.generate_pdf_report()
# Modify title_style, heading_style for fonts
# Change colors: colors.HexColor('#1a1a1a')
```

**HTML Report:**
```python
# Edit ReportGenerator.generate_html_report()
# Modify CSS in html_content string
# Change layout, colors, fonts
```

---

## 🔄 Automation & Scheduling

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Trend Extraction Weekly"
4. Trigger: Weekly, Monday 9:00 AM
5. Action: Start a Program
   - Program: `C:\Python\python.exe`
   - Arguments: `C:\path\to\main.py`
   - Start in: `C:\path\to\project\`

### macOS/Linux Cron

```bash
# Edit crontab
crontab -e

# Run every Monday at 9 AM
0 9 * * 1 cd /path/to/project && python3 main.py

# Run daily at 6 AM
0 6 * * * cd /path/to/project && python3 main.py

# Run every 6 hours
0 */6 * * * cd /path/to/project && python3 main.py
```

### Python Script Scheduler

```python
# schedule_runner.py
import schedule
import time
from main import TrendExtractor

def run_extraction():
    extractor = TrendExtractor()
    extractor.run_weekly_extraction()

# Schedule weekly on Monday at 9 AM
schedule.every().monday.at("09:00").do(run_extraction)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

---

## 🐛 Troubleshooting Guide

### Common Issues & Solutions

#### 1. ModuleNotFoundError
```
Error: No module named 'google.generativeai'
```
**Solution:**
```bash
pip install -r requirements.txt
```

#### 2. API Key Errors
```
Error: API key not found or invalid
```
**Solution:**
- Check `.env` file exists
- Verify GEMINI_API_KEY is set correctly
- No spaces around `=` sign
- Key starts with "AIza"

#### 3. Rate Limiting
```
Error: 429 Too Many Requests
```
**Solution:**
- Wait 5-10 minutes
- Reduce number of keywords
- Increase sleep delays in code

#### 4. Database Lock
```
Error: database is locked
```
**Solution:**
- Close other programs accessing DB
- Check for running instances
- Restart if needed

#### 5. Chart Generation Fails
```
Error: Failed to save chart
```
**Solution:**
- Check `charts/` directory exists
- Verify write permissions
- Run: `python setup.py`

#### 6. Empty Reports
```
Warning: No trends found
```
**Solution:**
- Normal on first run
- Check internet connection
- Verify API keys are correct
- Try different keywords

---

## 📊 Performance Optimization

### Speed Improvements

1. **Reduce Keywords**
   ```python
   # Limit to 10-15 most important keywords
   MARKETING_KEYWORDS = ['seo', 'content marketing', ...]
   ```

2. **Parallel Processing**
   ```python
   from concurrent.futures import ThreadPoolExecutor
   
   with ThreadPoolExecutor(max_workers=3) as executor:
       futures = [executor.submit(fetch_platform) for platform in platforms]
   ```

3. **Cache Results**
   ```python
   import pickle
   from datetime import datetime, timedelta
   
   # Cache for 1 hour
   cache_file = 'trends_cache.pkl'
   cache_duration = timedelta(hours=1)
   ```

### Memory Optimization

1. **Limit Result Size**
   ```python
   # Reduce limit parameter
   reddit_trends = reddit_monitor.get_trending_topics(limit=25)
   ```

2. **Stream Processing**
   ```python
   # Process in batches instead of loading all at once
   batch_size = 100
   ```

---

## 🔒 Security Best Practices

### API Key Protection

1. **Never commit .env file**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use Environment Variables**
   ```bash
   # Linux/Mac
   export GEMINI_API_KEY="your_key"
   
   # Windows
   set GEMINI_API_KEY=your_key
   ```

3. **Rotate Keys Regularly**
   - Change API keys every 90 days
   - Revoke unused keys

### Data Privacy

1. **Don't log sensitive data**
2. **Encrypt database** (optional)
3. **Secure report storage**

---

## 📚 API Reference

### Main Classes

#### TrendExtractor
```python
extractor = TrendExtractor()
extractor.extract_trends()  # Fetch from all platforms
extractor.process_trends(trends)  # Categorize & analyze
extractor.generate_report(trends)  # Create reports
extractor.run_weekly_extraction()  # Full workflow
```

#### DatabaseManager
```python
db = DatabaseManager('trends_database.db')
db.save_trend(trend_data)  # Save single trend
db.get_historical_trends(days=30)  # Retrieve trends
```

#### SentimentAnalyzer
```python
analyzer = SentimentAnalyzer(api_key)
score = analyzer.analyze_sentiment(text)  # Returns -1 to 1
scores = analyzer.batch_analyze(texts)  # Multiple texts
```

---

## 🎓 Example Use Cases

### 1. Marketing Agency
**Goal:** Weekly client reports
```python
# Customize keywords per client
client_keywords = ['real estate', 'property', 'housing']
extractor.config.MARKETING_KEYWORDS = client_keywords
extractor.run_weekly_extraction()
```

### 2. Content Creator
**Goal:** Find trending topics
```python
# Focus on specific platforms
trends = extractor.extract_trends()
top_trends = sorted(trends, key=lambda x: x['volume'], reverse=True)[:10]
```

### 3. SEO Specialist
**Goal:** Track search trends
```python
# Focus on Google Trends only
google_trends = extractor.google_trends.get_trending_topics(keywords)
```

### 4. Social Media Manager
**Goal:** Monitor platform-specific trends
```python
# Reddit only
reddit_trends = extractor.reddit_monitor.get_trending_topics(
    subreddits=['socialmedia', 'marketing']
)
```

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Twitter/X API integration
- [ ] Email report delivery
- [ ] Web dashboard interface
- [ ] Real-time monitoring
- [ ] Slack/Discord notifications
- [ ] Excel export format
- [ ] Trend prediction using ML
- [ ] Competitor analysis
- [ ] Custom alert system

### How to Contribute
1. Fork the repository
2. Create feature branch
3. Add your enhancement
4. Test thoroughly
5. Submit pull request

---

## 📞 Support & Resources

### Documentation
- **README.md** - Complete documentation
- **QUICKSTART.md** - 5-minute setup
- **SAMPLE_TRENDS.md** - Example output
- Code comments in main.py

### External Resources
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [pytrends Documentation](https://pypi.org/project/pytrends/)
- [PRAW Documentation](https://praw.readthedocs.io/)
- [ReportLab Guide](https://www.reportlab.com/docs/)

---

## 📝 License & Credits

### License
This project is open-source and available for educational and commercial use.

### Credits
- Google Gemini AI for sentiment analysis
- pytrends library for Google Trends data
- PRAW library for Reddit API
- Matplotlib & Seaborn for visualizations
- ReportLab for PDF generation

---

## ✅ Checklist for Success

Before running the first time:
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with API keys
- [ ] Gemini API key is valid
- [ ] Internet connection active
- [ ] Write permissions in project folder

After first run:
- [ ] Check `reports/` folder for PDF/HTML
- [ ] Check `charts/` folder for images
- [ ] Verify `trends_database.db` was created
- [ ] Review trends in terminal output

---

**🎉 You're all set! Run `python main.py` to start extracting trends!**

---

*Last Updated: September 2025*
*Version: 1.0.0*