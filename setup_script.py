"""
Setup script for Trend Extraction System
Run this to create necessary directories and check dependencies
"""

import os
import sys
import subprocess

def create_directories():
    """Create necessary directories for the project"""
    directories = [
        'reports',
        'charts',
        'data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def check_dependencies():
    """Check if all required packages are installed"""
    print("\nChecking dependencies...")
    
    try:
        import google.generativeai
        print("✓ google-generativeai installed")
    except ImportError:
        print("✗ google-generativeai not installed")
    
    try:
        import pytrends
        print("✓ pytrends installed")
    except ImportError:
        print("✗ pytrends not installed")
    
    try:
        import praw
        print("✓ praw installed")
    except ImportError:
        print("✗ praw not installed")
    
    try:
        import matplotlib
        print("✓ matplotlib installed")
    except ImportError:
        print("✗ matplotlib not installed")
    
    try:
        import seaborn
        print("✓ seaborn installed")
    except ImportError:
        print("✗ seaborn not installed")
    
    try:
        import reportlab
        print("✓ reportlab installed")
    except ImportError:
        print("✗ reportlab not installed")

def install_dependencies():
    """Install all dependencies from requirements.txt"""
    print("\nInstalling dependencies from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✓ All dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("\n✗ Error installing dependencies. Please install manually.")

def check_env_file():
    """Check if .env file exists"""
    if os.path.exists('.env'):
        print("\n✓ .env file found")
    else:
        print("\n✗ .env file not found")
        print("  Please copy .env.example to .env and add your API keys")

def main():
    print("="*60)
    print("TREND EXTRACTION SYSTEM SETUP")
    print("="*60)
    
    # Create directories
    print("\nCreating directories...")
    create_directories()
    
    # Check for .env file
    check_env_file()
    
    # Check dependencies
    check_dependencies()
    
    # Ask if user wants to install dependencies
    print("\n" + "="*60)
    response = input("\nDo you want to install missing dependencies? (y/n): ")
    if response.lower() == 'y':
        install_dependencies()
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Copy .env.example to .env")
    print("2. Add your API keys to .env file")
    print("3. Run: python main.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()