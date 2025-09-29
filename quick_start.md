# 🚀 Quick Start Guide

Get your Trend Extraction System up and running in 5 minutes!

## Step-by-Step Setup

### 1️⃣ Prerequisites Check
Make sure you have:
- Python 3.8 or higher installed
- Internet connection
- A Google Gemini API key (free from Google AI Studio)

### 2️⃣ Download Files
Download all these files to a new folder:
```
trend-extraction-system/
├── main.py
├── setup.py
├── requirements.txt
├── .env.example
├── README.md
├── QUICKSTART.md
└── trend-extraction.code-workspace
```

### 3️⃣ Install Dependencies

**Option A: Automatic (Recommended)**
```bash
python setup.py
```
Press 'y' when asked to install dependencies.

**Option B: Manual**
```bash
pip install -r requirements.txt
```

### 4️⃣ Get Your Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Click **"Get API Key"** or **"Create API Key"**
3. Copy the key (starts with "AIza...")

### 5️⃣ Configure Environment

**Windows:**
```cmd
copy .env.example .env
notepad .env
```

**Mac/Linux:**
```bash
cp .env.example .env
nano .env
```

Paste your Gemini API key:
```
GEMINI_API_KEY=AIzaSyD...your_actual_key_here...
```

Save and close the file.

### 6️⃣ Run the Program! 🎉

```bash
python main.py
```

That's it! The program will:
- ✅ Extract trends from Google Trends and Reddit
- ✅ Analyze sentiment with AI
- ✅ Generate beautiful charts
- ✅ Create PDF and HTML reports
- ✅ Display top 20 trends in your terminal

## 📂 Where to Find Your Reports

After running, check these folders:
- **reports/** - Your PDF and HTML reports
- **charts/** - All generated charts (PNG images)
- **trends_database.db** - Historical data (SQLite database)

## 🎯 Using VS Code (Optional)

If you use VS Code:

1. Open VS Code
2. File → Open Workspace from File
3. Select `trend-extraction.code-workspace`
4. Press **F5** to run with debugging

## ⚡ Quick Commands

```bash
# Run the trend extraction
python main.py

# Run setup/check dependencies
python setup.py

# Install/update dependencies
pip install -r requirements.txt

# View the database
sqlite3 trends_database.db "SELECT * FROM trends LIMIT 10;"
```

## 🔧 Common Issues & Fixes

### "ModuleNotFoundError: No module named 'X'"
**Fix:** Install dependencies
```bash
pip install -r requirements.txt
```

### "API key not found" or "Invalid API key"
**Fix:** Check your `.env` file
- Make sure the file is named exactly `.env` (not `.env.txt`)
- Make sure `GEMINI_API_KEY=` has no spaces around the `=`
- Make sure your key is correct (starts with "AIza")

### "No trends found"
**Fix:** This is normal on first run or if APIs are rate-limited
- Wait 5 minutes and run again
- Check your internet connection
- The program will still generate a report with sample data

### "Permission denied" on Windows
**Fix:** Run Command Prompt as Administrator

### Charts/Reports not generating
**Fix:** Make sure directories exist
```bash
python setup.py
```

## 🎨 Customization Tips

Want to customize? Edit `main.py`:

**Change keywords to monitor:**
```python
MARKETING_KEYWORDS = [
    'your', 'custom', 'keywords', 'here'
]
```

**Change subreddits:**
```python
subreddits = ['marketing', 'entrepreneur', 'business']
```

**Change report output:**
```python
REPORT_OUTPUT_DIR = 'my_reports'
CHARTS_OUTPUT_DIR = 'my_charts'
```

## 📊 Understanding Your Report

Your PDF/HTML report includes:

1. **Executive Summary** - Overview of what was analyzed
2. **Key Metrics** - Total trends, platforms, sentiment
3. **Visual Charts**:
   - Category Distribution (pie chart)
   - Platform Comparison (bar chart)
   - Sentiment Distribution (histogram)
   - Top Trends (horizontal bars)
4. **Top 20 Trends Table** - Detailed breakdown

## 🔄 Running Weekly

Want weekly automated reports?

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Weekly on Monday, 9 AM
4. Start a Program: `python`
5. Arguments: `C:\path\to\main.py`

**Mac/Linux Cron:**
```bash
crontab -e
# Add this line for weekly on Monday 9 AM:
0 9 * * 1 cd /path/to/project && python3 main.py
```

## 🆘 Need Help?

1. Check the full **README.md** for detailed docs
2. Review the **SAMPLE_TRENDS.md** for example output
3. Make sure your API keys are correct
4. Check that all files are in the same folder

## 🎉 You're Ready!

Run `python main.py` and watch the magic happen!

Your first report will be in the `reports/` folder. Open the PDF to see your trend analysis with beautiful visualizations.

---

**Pro Tip:** Run the program weekly to track how trends change over time. The database will store historical data for comparison!