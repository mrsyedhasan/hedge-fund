#!/usr/bin/env python3
"""
Interactive AI Hedge Fund Analysis
Asks user to choose between GROQ or YAHOO before running analysis
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_user_choice():
    """Get user's choice between GROQ or YAHOO"""
    print("🚀 AI HEDGE FUND ANALYSIS")
    print("=" * 50)
    print("Please choose your preferred option:")
    print("1. GROQ - Advanced AI analysis with Groq's Llama models")
    print("2. YAHOO - Yahoo Finance data with AI analysis")
    print("=" * 50)
    
    # Check if we're in an interactive environment
    try:
        while True:
            choice = input("Enter your choice (1 for GROQ, 2 for YAHOO): ").strip()
            
            if choice == "1":
                return "GROQ"
            elif choice == "2":
                return "YAHOO"
            else:
                print("❌ Invalid choice. Please enter 1 for GROQ or 2 for YAHOO.")
    except EOFError:
        # Non-interactive environment, use default
        print("❌ Non-interactive environment detected. Using GROQ as default.")
        return "GROQ"

def get_tickers():
    """Get tickers from user"""
    print("\n📊 Enter the stock tickers you want to analyze:")
    print("Example: VZ,CMCSA or GOOGL,NVDA,AAPL")
    
    try:
        tickers_input = input("Tickers (comma-separated): ").strip()
        
        if not tickers_input:
            print("❌ No tickers provided. Using default: VZ,CMCSA")
            return ["VZ", "CMCSA"]
        
        tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]
        return tickers
    except EOFError:
        # Non-interactive environment, use default
        print("❌ Non-interactive environment detected. Using default: VZ,CMCSA")
        return ["VZ", "CMCSA"]

def run_groq_analysis(tickers):
    """Run analysis using Groq"""
    print(f"\n🤖 Running GROQ analysis for: {', '.join(tickers)}")
    print("=" * 50)
    
    # Import and run the Groq analysis
    try:
        from yahoo_agents_hedge_fund import run_comprehensive_analysis
        run_comprehensive_analysis(tickers)
    except ImportError:
        print("❌ Error: Could not import Groq analysis module")
        print("Make sure yahoo_agents_hedge_fund.py exists")
    except Exception as e:
        print(f"❌ Error running Groq analysis: {e}")

def run_yahoo_analysis(tickers):
    """Run analysis using Yahoo Finance"""
    print(f"\n📈 Running YAHOO analysis for: {', '.join(tickers)}")
    print("=" * 50)
    
    # Import and run the Yahoo analysis
    try:
        from yahoo_hedge_fund import run_yahoo_hedge_fund
        run_yahoo_hedge_fund(tickers)
    except ImportError:
        print("❌ Error: Could not import Yahoo analysis module")
        print("Make sure yahoo_hedge_fund.py exists")
    except Exception as e:
        print(f"❌ Error running Yahoo analysis: {e}")

def main():
    """Main function"""
    print("Welcome to the AI Hedge Fund Analysis Tool!")
    print("This tool will analyze stocks using legendary investor AI agents.")
    print()
    
    # Get user choices
    choice = get_user_choice()
    tickers = get_tickers()
    
    print(f"\n✅ You selected: {choice}")
    print(f"✅ Analyzing: {', '.join(tickers)}")
    print()
    
    # Run the appropriate analysis
    if choice == "GROQ":
        run_groq_analysis(tickers)
    elif choice == "YAHOO":
        run_yahoo_analysis(tickers)
    
    print("\n🎯 Analysis complete!")
    print("Thank you for using the AI Hedge Fund Analysis Tool!")

if __name__ == "__main__":
    main()
