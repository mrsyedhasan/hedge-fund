#!/usr/bin/env python3
"""
Fast version of hedge fund analysis - optimized for speed
"""

import sys
import os
from datetime import datetime, timedelta

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import run_hedge_fund
from src.llm.models import ModelProvider

def main():
    if len(sys.argv) < 2:
        print("Usage: python3.10 run_analysis_fast.py <TICKER>")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    
    # Set up analysis period (6 months for faster execution)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")

    print(f"🚀 Running FAST Hedge Fund Analysis")
    print(f"📊 Ticker: {ticker}")
    print(f"🤖 Model: Mistral via Ollama")
    print(f"⏱️  Period: 6 months (optimized for speed)")
    print("=" * 50)

    # Run the hedge fund analysis with optimized settings
    run_hedge_fund(
        tickers=[ticker],
        start_date=start_date,
        end_date=end_date,
        portfolio={"cash": 100000.0, "positions": {}, "equity": 100000.0, "margin_used": 0.0},
        model_name="mistral:7b-instruct",
        model_provider=ModelProvider.OLLAMA.value,
        selected_analysts=[], # Use all analysts
        show_reasoning=False,  # Disable verbose reasoning for speed
    )
    print(f"🎉 Done!")

if __name__ == "__main__":
    main()
