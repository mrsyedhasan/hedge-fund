#!/usr/bin/env python3
"""
Command Line AI Hedge Fund Analysis
Usage: python hedge_fund_cli.py --provider GROQ --tickers VZ,CMCSA
"""

import argparse
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_groq_analysis(tickers):
    """Run analysis using Groq"""
    print(f"\n🤖 Running GROQ analysis for: {', '.join(tickers)}")
    print("=" * 50)
    
    try:
        from yahoo_agents_hedge_fund import run_yahoo_agents_hedge_fund
        run_yahoo_agents_hedge_fund(tickers)
    except ImportError:
        print("❌ Error: Could not import Groq analysis module")
        print("Make sure yahoo_agents_hedge_fund.py exists")
        return False
    except Exception as e:
        print(f"❌ Error running Groq analysis: {e}")
        return False
    return True

def run_yahoo_analysis(tickers):
    """Run analysis using Yahoo Finance"""
    print(f"\n📈 Running YAHOO analysis for: {', '.join(tickers)}")
    print("=" * 50)
    
    try:
        from yahoo_hedge_fund import run_yahoo_hedge_fund
        run_yahoo_hedge_fund(tickers)
    except ImportError:
        print("❌ Error: Could not import Yahoo analysis module")
        print("Make sure yahoo_hedge_fund.py exists")
        return False
    except Exception as e:
        print(f"❌ Error running Yahoo analysis: {e}")
        return False
    return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="AI Hedge Fund Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hedge_fund_cli.py --provider GROQ --tickers VZ,CMCSA
  python hedge_fund_cli.py --provider YAHOO --tickers GOOGL,NVDA,AAPL
  python hedge_fund_cli.py --provider GROQ --tickers VZ
        """
    )
    
    parser.add_argument(
        "--provider", 
        choices=["GROQ", "YAHOO"], 
        required=True,
        help="Choose between GROQ (advanced AI) or YAHOO (Yahoo Finance data)"
    )
    
    parser.add_argument(
        "--tickers", 
        type=str, 
        default="VZ,CMCSA",
        help="Comma-separated list of stock tickers (default: VZ,CMCSA)"
    )
    
    args = parser.parse_args()
    
    # Parse tickers
    tickers = [ticker.strip().upper() for ticker in args.tickers.split(",")]
    
    print("🚀 AI HEDGE FUND ANALYSIS")
    print("=" * 50)
    print(f"Provider: {args.provider}")
    print(f"Tickers: {', '.join(tickers)}")
    print("=" * 50)
    
    # Run the appropriate analysis
    success = False
    if args.provider == "GROQ":
        success = run_groq_analysis(tickers)
    elif args.provider == "YAHOO":
        success = run_yahoo_analysis(tickers)
    
    if success:
        print("\n🎯 Analysis complete!")
        print("Thank you for using the AI Hedge Fund Analysis Tool!")
    else:
        print("\n❌ Analysis failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
