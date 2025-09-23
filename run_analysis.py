#!/usr/bin/env python3
"""
Simple script to run hedge fund analysis
Usage: python3.10 run_analysis.py [TICKER]
Example: python3.10 run_analysis.py AAPL
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import run_hedge_fund
from src.llm.models import ModelProvider
from datetime import datetime, timedelta

def main():
    """Run hedge fund analysis"""
    # Get ticker from command line or default to AAPL
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    
    print(f"🚀 Running Hedge Fund Analysis")
    print(f"📊 Ticker: {ticker}")
    print(f"🤖 Model: Mistral via Ollama")
    print("=" * 50)
    
    # Set up dates (1 year of data)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    
    # Initialize portfolio
    portfolio = {
        "cash": 100000.0,
        "margin_requirement": 0.0,
        "margin_used": 0.0,
        "positions": {
            ticker: {
                "long": 0,
                "short": 0,
                "long_cost_basis": 0.0,
                "short_cost_basis": 0.0,
                "short_margin_used": 0.0,
            }
        },
        "realized_gains": {
            ticker: {
                "long": 0.0,
                "short": 0.0,
            }
        },
    }
    
    # Start timing
    start_time = time.time()
    
    try:
        # Run the analysis
        result = run_hedge_fund(
            tickers=[ticker],
            start_date=start_date,
            end_date=end_date,
            portfolio=portfolio,
            show_reasoning=True,  # Enable verbose reasoning to see detailed results
            model_name="mistral:7b-instruct",
            model_provider=ModelProvider.OLLAMA
        )
        
        # End timing
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n⏱️  Analysis completed in {execution_time:.2f} seconds ({execution_time/60:.2f} minutes)")
        print("🎉 Done!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
