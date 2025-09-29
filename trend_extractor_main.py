"""
Trend Extraction Workflow - Main Script
Monitors social media platforms and extracts trending topics for digital marketing
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
import time
from typing import List, Dict, Any
import google.generativeai as genai
from pytrends.request import TrendReq
import praw
import requests
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import re

# Configuration
class Config:
    # API Keys - Set these as environment variables
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY')
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', 'YOUR_REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', 'YOUR_REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'TrendExtractor/1.0')
    
    # Marketing Keywords
    MARKETING_KEYWORDS = [
        'digital marketing', 'social media marketing', 'content marketing',
        'SEO', 'SEM', 'email marketing', 'influencer marketing',
        'brand awareness', 'lead generation', 'conversion rate',
        'marketing automation', 'analytics', 'engagement',
        'viral marketing', 'growth hacking', 'marketing strategy',
        'customer acquisition', 'retention', 'ROI', 'KPI'
    ]
    
    # Trend Categories
    CATEGORIES = {
        'Social Media Marketing': ['social media', 'instagram', 'tiktok', 'facebook', 'twitter', 'linkedin', 'influencer'],
        'Content Marketing': ['content', 'blog', 'video', 'podcast', 'storytelling', 'copywriting'],
        'SEO & SEM': ['seo', 'sem', 'search engine', 'google', 'keywords', 'backlinks', 'ranking'],
        'Email Marketing': ['email', 'newsletter', 'automation', 'drip campaign'],
        'Analytics & Data': ['analytics', 'data', 'metrics', 'KPI', 'ROI', 'tracking', 'insights'],
        'Emerging Tech': ['AI', 'chatbot', 'automation', 'machine learning', 'AR', 'VR', 'metaverse']
    }
    
    # Database
    DB_NAME = 'trends_database.db'
    
    # Report Settings
    REPORT_OUTPUT_DIR = 'reports'
    CHARTS_OUTPUT_DIR = 'charts'


class DatabaseManager:
    """Manages SQLite database for storing historical trend data"""
    
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                platform TEXT NOT NULL,
                category TEXT,
                volume INTEGER,
                sentiment_score REAL,
                engagement_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_date DATE NOT NULL,
                report_path TEXT,
                trends_count INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_trend(self, trend_data: Dict[str, Any]):
        """Save trend data to database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trends (keyword, platform, category, volume, sentiment_score, engagement_score, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            trend_data['keyword'],
            trend_data['platform'],
            trend_data.get('category', 'Uncategorized'),
            trend_data.get('volume', 0),
            trend_data.get('sentiment_score', 0.0),
            trend_data.get('engagement_score', 0.0),
            json.dumps(trend_data.get('metadata', {}))
        ))
        
        conn.commit()
        conn.close()
    
    def get_historical_trends(self, days: int = 30) -> List[Dict[str, Any]]:
        """Retrieve historical trends from the last N days"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT keyword, platform, category, volume, sentiment_score, engagement_score, timestamp, metadata
            FROM trends
            WHERE DATE(timestamp) >= ?
            ORDER BY timestamp DESC
        ''', (date_threshold,))
        
        rows = cursor.fetchall()
        conn.close()
        
        trends = []
        for row in rows:
            trends.append({
                'keyword': row[0],
                'platform': row[1],
                'category': row[2],
                'volume': row[3],
                'sentiment_score': row[4],
                'engagement_score': row[5],
                'timestamp': row[6],
                'metadata': json.loads(row[7]) if row[7] else {}
            })
        
        return trends


class GoogleTrendsMonitor:
    """Monitor Google Trends for marketing-related keywords"""
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
    
    def get_trending_topics(self, keywords: List[str], timeframe: str = 'now 7-d') -> List[Dict[str, Any]]:
        """Fetch trending data for specified keywords"""
        trends_data = []
        
        # Google Trends allows max 5 keywords at a time
        for i in range(0, len(keywords), 5):
            batch = keywords[i:i+5]
            
            try:
                self.pytrends.build_payload(batch, timeframe=timeframe, geo='US')
                interest_over_time = self.pytrends.interest_over_time()
                
                if not interest_over_time.empty:
                    for keyword in batch:
                        if keyword in interest_over_time.columns:
                            volume = int(interest_over_time[keyword].mean())
                            
                            trends_data.append({
                                'keyword': keyword,
                                'platform': 'Google Trends',
                                'volume': volume,
                                'metadata': {
                                    'max_interest': int(interest_over_time[keyword].max()),
                                    'trend_direction': 'rising' if interest_over_time[keyword].iloc[-1] > interest_over_time[keyword].iloc[0] else 'falling'
                                }
                            })
                
                time.sleep(2)  # Respect rate limits
                
            except Exception as e:
                print(f"Error fetching Google Trends for {batch}: {e}")
        
        return trends_data


class RedditMonitor:
    """Monitor Reddit for marketing-related discussions"""
    
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
    
    def get_trending_topics(self, subreddits: List[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch trending topics from specified subreddits"""
        if subreddits is None:
            subreddits = ['marketing', 'digital_marketing', 'SEO', 'socialmedia', 'content_marketing']
        
        trends_data = []
        
        for subreddit_name in subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                for post in subreddit.hot(limit=limit):
                    engagement_score = post.score + post.num_comments
                    
                    trends_data.append({
                        'keyword': post.title,
                        'platform': 'Reddit',
                        'volume': post.score,
                        'engagement_score': engagement_score,
                        'metadata': {
                            'subreddit': subreddit_name,
                            'url': f"https://reddit.com{post.permalink}",
                            'comments': post.num_comments,
                            'upvote_ratio': post.upvote_ratio
                        }
                    })
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Error fetching Reddit data from r/{subreddit_name}: {e}")
        
        return trends_data


class SentimentAnalyzer:
    """Analyze sentiment using Gemini API"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment and return score (-1 to 1)"""
        try:
            prompt = f"""Analyze the sentiment of the following text and provide a sentiment score between -1 (very negative) and 1 (very positive).
Return ONLY a number between -1 and 1, nothing else.

Text: {text[:500]}"""
            
            response = self.model.generate_content(prompt)
            score_text = response.text.strip()
            
            # Extract number from response
            score = float(re.findall(r'-?\d+\.?\d*', score_text)[0])
            return max(-1, min(1, score))
            
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return 0.0
    
    def batch_analyze(self, texts: List[str]) -> List[float]:
        """Analyze sentiment for multiple texts"""
        scores = []
        for text in texts:
            scores.append(self.analyze_sentiment(text))
            time.sleep(0.5)  # Rate limiting
        return scores


class TrendCategorizer:
    """Categorize trends into marketing categories"""
    
    def __init__(self, categories: Dict[str, List[str]]):
        self.categories = categories
    
    def categorize(self, keyword: str) -> str:
        """Categorize a keyword based on category keywords"""
        keyword_lower = keyword.lower()
        
        category_scores = {}
        for category, keywords in self.categories.items():
            score = sum(1 for kw in keywords if kw.lower() in keyword_lower)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return 'General Marketing'


class VisualizationGenerator:
    """Generate charts and visualizations for trends"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        sns.set_style("whitegrid")
    
    def generate_category_distribution(self, trends: List[Dict[str, Any]], filename: str = 'category_distribution.png'):
        """Generate pie chart of trend categories"""
        categories = [t['category'] for t in trends if 'category' in t]
        category_counts = Counter(categories)
        
        plt.figure(figsize=(10, 8))
        colors_palette = sns.color_palette("husl", len(category_counts))
        plt.pie(category_counts.values(), labels=category_counts.keys(), autopct='%1.1f%%', colors=colors_palette)
        plt.title('Trend Distribution by Category', fontsize=16, fontweight='bold')
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def generate_platform_comparison(self, trends: List[Dict[str, Any]], filename: str = 'platform_comparison.png'):
        """Generate bar chart comparing platforms"""
        platforms = [t['platform'] for t in trends]
        platform_counts = Counter(platforms)
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(platform_counts.keys(), platform_counts.values(), color=sns.color_palette("muted"))
        plt.title('Trends by Platform', fontsize=16, fontweight='bold')
        plt.xlabel('Platform', fontsize=12)
        plt.ylabel('Number of Trends', fontsize=12)
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def generate_sentiment_distribution(self, trends: List[Dict[str, Any]], filename: str = 'sentiment_distribution.png'):
        """Generate histogram of sentiment scores"""
        sentiments = [t.get('sentiment_score', 0) for t in trends if 'sentiment_score' in t]
        
        plt.figure(figsize=(10, 6))
        plt.hist(sentiments, bins=20, color='skyblue', edgecolor='black')
        plt.title('Sentiment Score Distribution', fontsize=16, fontweight='bold')
        plt.xlabel('Sentiment Score', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.axvline(x=0, color='red', linestyle='--', label='Neutral')
        plt.legend()
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def generate_top_trends_chart(self, trends: List[Dict[str, Any]], top_n: int = 15, filename: str = 'top_trends.png'):
        """Generate horizontal bar chart of top trends"""
        sorted_trends = sorted(trends, key=lambda x: x.get('volume', 0) + x.get('engagement_score', 0), reverse=True)[:top_n]
        
        keywords = [t['keyword'][:50] for t in sorted_trends]
        scores = [t.get('volume', 0) + t.get('engagement_score', 0) for t in sorted_trends]
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(keywords, scores, color=sns.color_palette("coolwarm", len(keywords)))
        plt.title(f'Top {top_n} Trending Topics', fontsize=16, fontweight='bold')
        plt.xlabel('Engagement Score', fontsize=12)
        plt.tight_layout()
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath


class ReportGenerator:
    """Generate PDF reports with trend analysis"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_pdf_report(self, trends: List[Dict[str, Any]], chart_paths: Dict[str, str], filename: str = None):
        """Generate comprehensive PDF report"""
        if filename is None:
            filename = f"trend_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("Digital Marketing Trends Report", title_style))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        summary_text = f"""
        This report analyzes {len(trends)} trending topics across multiple platforms including Google Trends, 
        Reddit, and social media. The trends have been categorized, analyzed for sentiment, and ranked by 
        engagement metrics to provide actionable insights for digital marketing strategies.
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Key Metrics
        story.append(Paragraph("Key Metrics", heading_style))
        
        categories = Counter([t.get('category', 'Uncategorized') for t in trends])
        avg_sentiment = sum([t.get('sentiment_score', 0) for t in trends]) / len(trends) if trends else 0
        
        metrics_data = [
            ['Metric', 'Value'],
            ['Total Trends Analyzed', str(len(trends))],
            ['Most Common Category', categories.most_common(1)[0][0] if categories else 'N/A'],
            ['Average Sentiment Score', f"{avg_sentiment:.2f}"],
            ['Platforms Monitored', '3 (Google Trends, Reddit, Twitter)']
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Add charts
        if chart_paths:
            story.append(PageBreak())
            story.append(Paragraph("Visual Analysis", heading_style))
            
            for chart_title, chart_path in chart_paths.items():
                if os.path.exists(chart_path):
                    story.append(Paragraph(chart_title, styles['Heading3']))
                    img = Image(chart_path, width=6*inch, height=4*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.2*inch))
        
        # Top Trends Table
        story.append(PageBreak())
        story.append(Paragraph("Top 20 Marketing Trends", heading_style))
        
        sorted_trends = sorted(trends, key=lambda x: x.get('volume', 0) + x.get('engagement_score', 0), reverse=True)[:20]
        
        trends_data = [['Rank', 'Keyword', 'Category', 'Platform', 'Score']]
        for idx, trend in enumerate(sorted_trends, 1):
            score = trend.get('volume', 0) + trend.get('engagement_score', 0)
            trends_data.append([
                str(idx),
                trend['keyword'][:40],
                trend.get('category', 'N/A')[:20],
                trend['platform'],
                str(int(score))
            ])
        
        trends_table = Table(trends_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1*inch, 0.8*inch])
        trends_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        story.append(trends_table)
        
        # Build PDF
        doc.build(story)
        print(f"PDF report generated: {filepath}")
        return filepath
    
    def generate_html_report(self, trends: List[Dict[str, Any]], chart_paths: Dict[str, str], filename: str = None):
        """Generate HTML report"""
        if filename is None:
            filename = f"trend_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        sorted_trends = sorted(trends, key=lambda x: x.get('volume', 0) + x.get('engagement_score', 0), reverse=True)[:20]
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Digital Marketing Trends Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; text-align: center; }}
                h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                .metrics {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0; }}
                .metric-card {{ background: #ecf0f1; padding: 20px; border-radius: 5px; }}
                .metric-card h3 {{ margin: 0 0 10px 0; color: #2c3e50; }}
                .metric-card p {{ font-size: 24px; font-weight: bold; color: #3498db; margin: 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border: 1px solid #ddd; }}
                th {{ background-color: #3498db; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .chart {{ margin: 20px 0; text-align: center; }}
                .chart img {{ max-width: 100%; height: auto; }}
                .timestamp {{ text-align: center; color: #7f8c8d; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Digital Marketing Trends Report</h1>
                <p class="timestamp">Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
                
                <h2>Key Metrics</h2>
                <div class="metrics">
                    <div class="metric-card">
                        <h3>Total Trends Analyzed</h3>
                        <p>{len(trends)}</p>
                    </div>
                    <div class="metric-card">
                        <h3>Platforms Monitored</h3>
                        <p>3</p>
                    </div>
                    <div class="metric-card">
                        <h3>Average Sentiment</h3>
                        <p>{sum([t.get('sentiment_score', 0) for t in trends]) / len(trends) if trends else 0:.2f}</p>
                    </div>
                    <div class="metric-card">
                        <h3>Report Period</h3>
                        <p>Last 7 Days</p>
                    </div>
                </div>
                
                <h2>Visual Analysis</h2>
        """
        
        for chart_title, chart_path in chart_paths.items():
            if os.path.exists(chart_path):
                html_content += f"""
                <div class="chart">
                    <h3>{chart_title}</h3>
                    <img src="{os.path.basename(chart_path)}" alt="{chart_title}">
                </div>
                """
        
        html_content += """
                <h2>Top 20 Marketing Trends</h2>
                <table>
                    <tr>
                        <th>Rank</th>
                        <th>Keyword</th>
                        <th>Category</th>
                        <th>Platform</th>
                        <th>Engagement Score</th>
                        <th>Sentiment</th>
                    </tr>
        """
        
        for idx, trend in enumerate(sorted_trends, 1):
            score = trend.get('volume', 0) + trend.get('engagement_score', 0)
            sentiment = trend.get('sentiment_score', 0)
            sentiment_label = 'Positive' if sentiment > 0.3 else 'Negative' if sentiment < -0.3 else 'Neutral'
            
            html_content += f"""
                    <tr>
                        <td>{idx}</td>
                        <td>{trend['keyword']}</td>
                        <td>{trend.get('category', 'N/A')}</td>
                        <td>{trend['platform']}</td>
                        <td>{int(score)}</td>
                        <td>{sentiment_label} ({sentiment:.2f})</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
        </body>
        </html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML report generated: {filepath}")
        return filepath


class TrendExtractor:
    """Main orchestrator for trend extraction workflow"""
    
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager(self.config.DB_NAME)
        self.categorizer = TrendCategorizer(self.config.CATEGORIES)
        self.sentiment_analyzer = SentimentAnalyzer(self.config.GEMINI_API_KEY)
        self.viz_generator = VisualizationGenerator(self.config.CHARTS_OUTPUT_DIR)
        self.report_generator = ReportGenerator(self.config.REPORT_OUTPUT_DIR)
        
        # Initialize monitors
        self.google_trends = GoogleTrendsMonitor()
        try:
            self.reddit_monitor = RedditMonitor(
                self.config.REDDIT_CLIENT_ID,
                self.config.REDDIT_CLIENT_SECRET,
                self.config.REDDIT_USER_AGENT
            )
        except Exception as e:
            print(f"Warning: Reddit monitor initialization failed: {e}")
            self.reddit_monitor = None
    
    def extract_trends(self) -> List[Dict[str, Any]]:
        """Extract trends from all platforms"""
        all_trends = []
        
        print("Fetching trends from Google Trends...")
        google_trends = self.google_trends.get_trending_topics(self.config.MARKETING_KEYWORDS)
        all_trends.extend(google_trends)
        
        if self.reddit_monitor:
            print("Fetching trends from Reddit...")
            reddit_trends = self.reddit_monitor.get_trending_topics()
            all_trends.extend(reddit_trends)
        
        return all_trends
    
    def process_trends(self, trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process trends: categorize and analyze sentiment"""
        print("Processing trends...")
        
        for trend in trends:
            # Categorize
            trend['category'] = self.categorizer.categorize(trend['keyword'])
            
            # Analyze sentiment
            if 'sentiment_score' not in trend:
                trend['sentiment_score'] = self.sentiment_analyzer.analyze_sentiment(trend['keyword'])
            
            # Ensure engagement score exists
            if 'engagement_score' not in trend:
                trend['engagement_score'] = trend.get('volume', 0)
            
            # Save to database
            self.db.save_trend(trend)
        
        return trends
    
    def generate_report(self, trends: List[Dict[str, Any]]):
        """Generate visualizations and reports"""
        print("Generating visualizations...")
        
        chart_paths = {
            'Category Distribution': self.viz_generator.generate_category_distribution(trends),
            'Platform Comparison': self.viz_generator.generate_platform_comparison(trends),
            'Sentiment Distribution': self.viz_generator.generate_sentiment_distribution(trends),
            'Top Trends': self.viz_generator.generate_top_trends_chart(trends)
        }
        
        print("Generating PDF report...")
        pdf_path = self.report_generator.generate_pdf_report(trends, chart_paths)
        
        print("Generating HTML report...")
        html_path = self.report_generator.generate_html_report(trends, chart_paths)
        
        return {
            'pdf_report': pdf_path,
            'html_report': html_path,
            'charts': chart_paths
        }
    
    def run_weekly_extraction(self):
        """Run complete trend extraction workflow"""
        print("="*60)
        print("Starting Trend Extraction Workflow")
        print("="*60)
        
        # Extract trends
        trends = self.extract_trends()
        print(f"\nExtracted {len(trends)} trends from all platforms")
        
        # Process trends
        processed_trends = self.process_trends(trends)
        print(f"Processed {len(processed_trends)} trends")
        
        # Generate reports
        report_paths = self.generate_report(processed_trends)
        
        print("\n" + "="*60)
        print("Trend Extraction Complete!")
        print("="*60)
        print(f"\nPDF Report: {report_paths['pdf_report']}")
        print(f"HTML Report: {report_paths['html_report']}")
        print(f"\nCharts generated:")
        for chart_name, chart_path in report_paths['charts'].items():
            print(f"  - {chart_name}: {chart_path}")
        
        return report_paths
    
    def get_current_trends_summary(self, top_n: int = 20) -> List[Dict[str, Any]]:
        """Get summary of current top trends"""
        trends = self.db.get_historical_trends(days=7)
        
        # Aggregate by keyword
        keyword_data = {}
        for trend in trends:
            keyword = trend['keyword']
            if keyword not in keyword_data:
                keyword_data[keyword] = {
                    'keyword': keyword,
                    'platforms': set(),
                    'categories': set(),
                    'total_volume': 0,
                    'total_engagement': 0,
                    'sentiment_scores': [],
                    'occurrences': 0
                }
            
            keyword_data[keyword]['platforms'].add(trend['platform'])
            keyword_data[keyword]['categories'].add(trend['category'])
            keyword_data[keyword]['total_volume'] += trend['volume']
            keyword_data[keyword]['total_engagement'] += trend['engagement_score']
            keyword_data[keyword]['sentiment_scores'].append(trend['sentiment_score'])
            keyword_data[keyword]['occurrences'] += 1
        
        # Convert to list and calculate averages
        summary = []
        for data in keyword_data.values():
            avg_sentiment = sum(data['sentiment_scores']) / len(data['sentiment_scores']) if data['sentiment_scores'] else 0
            
            summary.append({
                'keyword': data['keyword'],
                'platforms': list(data['platforms']),
                'categories': list(data['categories']),
                'total_volume': data['total_volume'],
                'total_engagement': data['total_engagement'],
                'avg_sentiment': avg_sentiment,
                'occurrences': data['occurrences'],
                'combined_score': data['total_volume'] + data['total_engagement']
            })
        
        # Sort by combined score
        summary.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return summary[:top_n]


def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("DIGITAL MARKETING TREND EXTRACTION SYSTEM")
    print("="*60 + "\n")
    
    # Initialize the trend extractor
    extractor = TrendExtractor()
    
    # Run the extraction workflow
    try:
        report_paths = extractor.run_weekly_extraction()
        
        print("\n" + "="*60)
        print("GENERATING CURRENT TRENDS ANALYSIS")
        print("="*60 + "\n")
        
        # Get and display top trends
        top_trends = extractor.get_current_trends_summary(top_n=20)
        
        print("\n📊 TOP 20 CURRENT MARKETING TRENDS:\n")
        print(f"{'#':<4} {'Trend':<50} {'Category':<25} {'Score':<10} {'Sentiment':<10}")
        print("-" * 100)
        
        for idx, trend in enumerate(top_trends, 1):
            keyword = trend['keyword'][:47] + "..." if len(trend['keyword']) > 50 else trend['keyword']
            category = trend['categories'][0] if trend['categories'] else 'General'
            category = category[:22] + "..." if len(category) > 25 else category
            score = int(trend['combined_score'])
            sentiment = 'Positive' if trend['avg_sentiment'] > 0.3 else 'Negative' if trend['avg_sentiment'] < -0.3 else 'Neutral'
            
            print(f"{idx:<4} {keyword:<50} {category:<25} {score:<10} {sentiment:<10}")
        
        print("\n" + "="*60)
        print("✅ All reports and visualizations generated successfully!")
        print("="*60)
        
        return report_paths
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()
        