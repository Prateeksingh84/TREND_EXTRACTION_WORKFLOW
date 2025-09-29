"""
Database Utility Script
Tools for managing and querying the trends database
"""

import sqlite3
import sys
from datetime import datetime, timedelta
from collections import Counter
import json


class DatabaseUtils:
    """Utility class for database operations"""
    
    def __init__(self, db_name='trends_database.db'):
        self.db_name = db_name
    
    def view_recent_trends(self, days=7, limit=50):
        """View recent trends from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT keyword, platform, category, volume, sentiment_score, 
                   engagement_score, timestamp
            FROM trends
            WHERE DATE(timestamp) >= ?
            ORDER BY (volume + engagement_score) DESC
            LIMIT ?
        ''', (date_threshold, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        print(f"\n{'='*100}")
        print(f"RECENT TRENDS (Last {days} days)")
        print(f"{'='*100}\n")
        
        print(f"{'Keyword':<40} {'Platform':<15} {'Category':<20} {'Score':<10} {'Sentiment':<10}")
        print("-" * 100)
        
        for row in rows:
            keyword = row[0][:37] + "..." if len(row[0]) > 40 else row[0]
            score = int(row[3] + row[5])
            sentiment = 'Positive' if row[4] > 0.3 else 'Negative' if row[4] < -0.3 else 'Neutral'
            
            print(f"{keyword:<40} {row[1]:<15} {row[2]:<20} {score:<10} {sentiment:<10}")
        
        print(f"\nTotal trends found: {len(rows)}")
    
    def get_statistics(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Total trends
        cursor.execute('SELECT COUNT(*) FROM trends')
        total_trends = cursor.fetchone()[0]
        
        # Trends by platform
        cursor.execute('SELECT platform, COUNT(*) FROM trends GROUP BY platform')
        platform_stats = cursor.fetchall()
        
        # Trends by category
        cursor.execute('SELECT category, COUNT(*) FROM trends GROUP BY category ORDER BY COUNT(*) DESC')
        category_stats = cursor.fetchall()
        
        # Average sentiment
        cursor.execute('SELECT AVG(sentiment_score) FROM trends')
        avg_sentiment = cursor.fetchone()[0] or 0
        
        # Date range
        cursor.execute('SELECT MIN(timestamp), MAX(timestamp) FROM trends')
        date_range = cursor.fetchone()
        
        conn.close()
        
        print(f"\n{'='*60}")
        print("DATABASE STATISTICS")
        print(f"{'='*60}\n")
        
        print(f"Total Trends Stored: {total_trends}")
        print(f"Average Sentiment: {avg_sentiment:.2f}")
        
        if date_range[0] and date_range[1]:
            print(f"Date Range: {date_range[0][:10]} to {date_range[1][:10]}")
        
        print(f"\n{'Platform':<20} {'Count':<10}")
        print("-" * 30)
        for platform, count in platform_stats:
            print(f"{platform:<20} {count:<10}")
        
        print(f"\n{'Category':<30} {'Count':<10}")
        print("-" * 40)
        for category, count in category_stats:
            print(f"{category:<30} {count:<10}")
    
    def search_trends(self, keyword):
        """Search for trends containing a keyword"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT keyword, platform, category, volume, sentiment_score, 
                   engagement_score, timestamp
            FROM trends
            WHERE keyword LIKE ?
            ORDER BY timestamp DESC
        ''', (f'%{keyword}%',))
        
        rows = cursor.fetchall()
        conn.close()
        
        print(f"\n{'='*100}")
        print(f"SEARCH RESULTS FOR: '{keyword}'")
        print(f"{'='*100}\n")
        
        if not rows:
            print("No trends found matching your search.")
            return
        
        print(f"{'Keyword':<40} {'Platform':<15} {'Category':<20} {'Date':<12}")
        print("-" * 100)
        
        for row in rows:
            keyword_text = row[0][:37] + "..." if len(row[0]) > 40 else row[0]
            date = row[6][:10] if row[6] else 'N/A'
            
            print(f"{keyword_text:<40} {row[1]:<15} {row[2]:<20} {date:<12}")
        
        print(f"\nTotal results found: {len(rows)}")
    
    def export_to_csv(self, output_file='trends_export.csv', days=30):
        """Export trends to CSV file"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT keyword, platform, category, volume, sentiment_score, 
                   engagement_score, timestamp
            FROM trends
            WHERE DATE(timestamp) >= ?
            ORDER BY timestamp DESC
        ''', (date_threshold,))
        
        rows = cursor.fetchall()
        conn.close()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('Keyword,Platform,Category,Volume,Sentiment Score,Engagement Score,Timestamp\n')
            
            for row in rows:
                # Escape commas in keyword
                keyword = row[0].replace(',', ';')
                f.write(f'"{keyword}",{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}\n')
        
        print(f"\n✓ Exported {len(rows)} trends to {output_file}")
    
    def clear_old_data(self, days=90):
        """Delete trends older than specified days"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute('SELECT COUNT(*) FROM trends WHERE DATE(timestamp) < ?', (date_threshold,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            print(f"\nNo trends older than {days} days found.")
            conn.close()
            return
        
        print(f"\nFound {count} trends older than {days} days.")
        confirm = input("Are you sure you want to delete them? (yes/no): ")
        
        if confirm.lower() == 'yes':
            cursor.execute('DELETE FROM trends WHERE DATE(timestamp) < ?', (date_threshold,))
            conn.commit()
            print(f"✓ Deleted {count} old trends.")
        else:
            print("Operation cancelled.")
        
        conn.close()
    
    def get_trending_keywords(self, days=7, top_n=20):
        """Get most frequently appearing keywords"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT keyword, COUNT(*) as frequency, 
                   AVG(volume) as avg_volume,
                   AVG(sentiment_score) as avg_sentiment
            FROM trends
            WHERE DATE(timestamp) >= ?
            GROUP BY keyword
            ORDER BY frequency DESC, avg_volume DESC
            LIMIT ?
        ''', (date_threshold, top_n))
        
        rows = cursor.fetchall()
        conn.close()
        
        print(f"\n{'='*100}")
        print(f"TOP {top_n} TRENDING KEYWORDS (Last {days} days)")
        print(f"{'='*100}\n")
        
        print(f"{'#':<4} {'Keyword':<45} {'Frequency':<12} {'Avg Volume':<12} {'Sentiment':<10}")
        print("-" * 100)
        
        for idx, row in enumerate(rows, 1):
            keyword = row[0][:42] + "..." if len(row[0]) > 45 else row[0]
            sentiment = 'Positive' if row[3] > 0.3 else 'Negative' if row[3] < -0.3 else 'Neutral'
            
            print(f"{idx:<4} {keyword:<45} {row[1]:<12} {int(row[2]):<12} {sentiment:<10}")
    
    def backup_database(self, backup_file=None):
        """Create a backup of the database"""
        if backup_file is None:
            backup_file = f"trends_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        import shutil
        try:
            shutil.copy2(self.db_name, backup_file)
            print(f"\n✓ Database backed up to: {backup_file}")
        except Exception as e:
            print(f"\n✗ Error creating backup: {e}")


def print_menu():
    """Print the main menu"""
    print("\n" + "="*60)
    print("TREND DATABASE UTILITY MENU")
    print("="*60)
    print("1. View Recent Trends")
    print("2. View Database Statistics")
    print("3. Search Trends by Keyword")
    print("4. Get Trending Keywords")
    print("5. Export to CSV")
    print("6. Clear Old Data")
    print("7. Backup Database")
    print("8. Exit")
    print("="*60)


def main():
    """Main function for interactive database management"""
    db_utils = DatabaseUtils()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            days = input("Enter number of days (default 7): ").strip()
            days = int(days) if days.isdigit() else 7
            limit = input("Enter limit (default 50): ").strip()
            limit = int(limit) if limit.isdigit() else 50
            db_utils.view_recent_trends(days=days, limit=limit)
        
        elif choice == '2':
            db_utils.get_statistics()
        
        elif choice == '3':
            keyword = input("Enter keyword to search: ").strip()
            if keyword:
                db_utils.search_trends(keyword)
        
        elif choice == '4':
            days = input("Enter number of days (default 7): ").strip()
            days = int(days) if days.isdigit() else 7
            top_n = input("Enter top N (default 20): ").strip()
            top_n = int(top_n) if top_n.isdigit() else 20
            db_utils.get_trending_keywords(days=days, top_n=top_n)
        
        elif choice == '5':
            output_file = input("Enter output filename (default: trends_export.csv): ").strip()
            output_file = output_file if output_file else 'trends_export.csv'
            days = input("Enter number of days to export (default 30): ").strip()
            days = int(days) if days.isdigit() else 30
            db_utils.export_to_csv(output_file=output_file, days=days)
        
        elif choice == '6':
            days = input("Delete trends older than how many days? (default 90): ").strip()
            days = int(days) if days.isdigit() else 90
            db_utils.clear_old_data(days=days)
        
        elif choice == '7':
            backup_file = input("Enter backup filename (press Enter for auto-generated): ").strip()
            backup_file = backup_file if backup_file else None
            db_utils.backup_database(backup_file=backup_file)
        
        elif choice == '8':
            print("\nExiting... Goodbye!")
            break
        
        else:
            print("\n✗ Invalid choice. Please enter a number between 1 and 8.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()