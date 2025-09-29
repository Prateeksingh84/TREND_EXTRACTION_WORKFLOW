# Digital Marketing Trend Extraction System

A comprehensive Python-based system that monitors social media platforms, extracts trending topics relevant to digital marketing, and generates detailed reports with visualizations.

## 🚀 Features

- **Multi-Platform Monitoring**: Extracts trends from Google Trends, Reddit, and more
- **Smart Categorization**: Automatically categorizes trends into marketing segments
- **Sentiment Analysis**: Uses Gemini AI to analyze sentiment of trending topics
- **Visual Reports**: Generates PDF and HTML reports with charts
- **Historical Tracking**: Stores trend data in SQLite database for comparison
- **Engagement Metrics**: Analyzes and ranks trends by engagement scores

## 📋 Requirements

- Python 3.8+
- Google Gemini API Key
- Reddit API Credentials (optional)

## 🛠️ Installation

### Step 1: Clone or Download the Project

Download all files to a directory on your computer.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or run the setup script:

```bash
python setup.py
```

### Step 3: Configure API Keys

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   ```

### Getting API Keys

#### Google Gemini API Key (Required)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API Key"
3. Create a new API key
4. Copy and paste it into your `.env` file

#### Reddit API Credentials (Optional but Recommended)
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Scroll down and click "Create App" or "Create Another App"
3. Fill in the form:
   - **name**: TrendExtractor (or any name)
   - **App type**: script
   - **description**: Trend extraction tool
   - **redirect uri**: http://localhost:8080
4. Click "Create app"
5. Copy the client ID (under the app name) and secret
6. Add them to your `.env` file

## 🎯 Usage

### Basic Usage

Run the trend extraction workflow:

```bash
python main.py
```

This will:
1. Extract trends from Google Trends and Reddit
2. Categorize and analyze each trend
3. Generate sentiment scores using Gemini AI
4. Create visualizations (charts/graphs)
5. Generate PDF and HTML reports
6. Save data to SQLite database

### Output Files

After running, you'll find:

- **reports/**: PDF and HTML trend reports
- **charts/**: PNG files of all visualizations
- **trends_database.db**: SQLite database with historical data

### Customization

Edit the `Config` class in `main.py` to customize:

- Marketing keywords to monitor
- Trend categories
- Report output directories
- Subreddits to monitor

## 📊 Report Contents

Generated reports include:

1. **Executive Summary**: Overview of trends analyzed
2. **Key Metrics**: Total trends, sentiment averages, platform distribution
3. **Visual Analysis**:
   - Category distribution (pie chart)
   - Platform comparison (bar chart)
   - Sentiment distribution (histogram)
   - Top trends (horizontal bar chart)
4. **Top 20 Trends Table**: Detailed breakdown with rankings

## 🗂️ Project Structure

```
trend-extraction-system/
├── main.py                 # Main script with all functionality
├── setup.py               # Setup and installation script
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .env                  # Your API keys (create this)
├── README.md             # This file
├── reports/              # Generated reports (created automatically)
├── charts/               # Generated visualizations (created automatically)
└── trends_database.db    # SQLite database (created automatically)
```

## 🔧 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "API key not found" errors
Make sure you've created a `.env` file with your API keys.

### Rate limiting issues
The script includes delays between API calls. If you still hit rate limits:
- Reduce the number of keywords in `Config.MARKETING_KEYWORDS`
- Increase sleep delays in monitor classes

### Reddit connection issues
Reddit API is optional. The script will continue if Reddit fails to connect.

## 📈 Scheduling Regular Extractions

### On Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., weekly on Monday)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\main.py`

### On macOS/Linux (Cron)
```bash
# Edit crontab
crontab -e

# Add line to run every Monday at 9 AM
0 9 * * 1 cd /path/to/project && /usr/bin/python3 main.py
```

## 🤝 Contributing

Feel free to fork and enhance this project! Some ideas:
- Add Twitter/X API support
- Add more visualization types
- Implement email notifications
- Add web dashboard
- Export to Excel format

## 📝 License

This project is open source and available for educational and commercial use.

## ⚠️ Important Notes

- **API Rate Limits**: Be mindful of API rate limits for Google Trends and Reddit
- **Gemini API**: Free tier has limitations; monitor your usage
- **Data Privacy**: Don't share your `.env` file or commit it to version control
- **Storage**: Database will grow over time; implement cleanup if needed

## 🎓 Example Use Cases

1. **Marketing Teams**: Weekly trend reports for strategy planning
2. **Content Creators**: Identify trending topics for content creation
3. **SEO Specialists**: Track search trends and keyword opportunities
4. **Social Media Managers**: Monitor platform-specific trends
5. **Market Researchers**: Analyze sentiment and engagement patterns

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments in `main.py`
3. Verify your API keys are correct

---

**Happy Trend Hunting! 📊🚀**