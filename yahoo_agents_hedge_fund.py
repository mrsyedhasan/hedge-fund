#!/usr/bin/env python3
"""
AI Hedge Fund with Custom Yahoo Finance Agents
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from llm.models import AVAILABLE_MODELS, get_model
from tools.api import get_yahoo_financial_info, get_yahoo_prices
from datetime import datetime, timedelta

def run_yahoo_agents_hedge_fund(tickers=["VZ", "CMCSA"]):
    """Run AI hedge fund with custom Yahoo Finance agents"""
    
    # Load environment variables
    load_dotenv()
    
    print("🚀 AI HEDGE FUND - YAHOO FINANCE AGENTS")
    print("=" * 70)
    print(f"🎯 Analyzing: {', '.join(tickers)}")
    print("🤖 Using: Groq AI Models + Custom Yahoo Finance Agents")
    print("=" * 70)
    
    # Get Groq model
    groq_models = [model for model in AVAILABLE_MODELS if model.provider.value == "Groq"]
    if not groq_models:
        print("❌ No Groq models available.")
        return
    
    model = groq_models[0]
    llm = get_model(model.model_name, model.provider)
    
    print(f"🤖 Using: {model.display_name}")
    
    # Prepare data for each ticker
    ticker_data = {}
    
    for ticker in tickers:
        print(f"\n📊 Fetching Yahoo Finance data for {ticker}...")
        
        try:
            # Get Yahoo Finance data
            financial_info = get_yahoo_financial_info(ticker)
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            prices = get_yahoo_prices(ticker, start_date, end_date)
            
            print(f"✅ {ticker} data retrieved: {len(financial_info)} financial metrics, {len(prices)} price points")
            
            # Extract key metrics using correct Yahoo Finance key names
            current_price = financial_info.get('currentPrice', 0)
            market_cap = financial_info.get('market_cap', 0)
            pe_ratio = financial_info.get('price_to_earnings_ratio', 0)
            pb_ratio = financial_info.get('price_to_book_ratio', 0)
            dividend_yield = financial_info.get('dividend_yield', 0) / 100 if financial_info.get('dividend_yield') else 0
            roe = financial_info.get('return_on_equity', 0)
            debt_to_equity = financial_info.get('debt_to_equity', 0)
            revenue_growth = financial_info.get('revenue_growth', 0)
            beta = financial_info.get('beta', 0)
            
            print(f"📈 {ticker} Key Metrics:")
            print(f"   Current Price: ${current_price}")
            print(f"   Market Cap: ${market_cap:,}" if market_cap else "   Market Cap: N/A")
            print(f"   P/E Ratio: {pe_ratio:.2f}")
            print(f"   P/B Ratio: {pb_ratio:.2f}")
            print(f"   Dividend Yield: {dividend_yield*100:.2f}%")
            print(f"   ROE: {roe*100:.2f}%")
            print(f"   Debt to Equity: {debt_to_equity:.2f}")
            print(f"   Revenue Growth: {revenue_growth*100:.2f}%")
            print(f"   Beta: {beta:.3f}")
            
            # Store data for the hedge fund
            ticker_data[ticker] = {
                'financial_info': financial_info,
                'prices': prices,
                'current_price': current_price,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio,
                'pb_ratio': pb_ratio,
                'dividend_yield': dividend_yield,
                'roe': roe,
                'debt_to_equity': debt_to_equity,
                'revenue_growth': revenue_growth,
                'beta': beta
            }
            
        except Exception as e:
            print(f"❌ Error fetching data for {ticker}: {e}")
            continue
    
    if not ticker_data:
        print("❌ No data available for analysis.")
        return
    
    # Run all AI agents
    print(f"\n🚀 Running AI Hedge Fund Agents...")
    print("=" * 70)
    print("📋 AI Agents:")
    print("   • Ben Graham (Value Investing)")
    print("   • Warren Buffett (Long-term Value)")
    print("   • Charlie Munger (Quality & Value)")
    print("   • Technical Analyst (Chart Analysis)")
    print("   • Risk Manager (Portfolio Risk)")
    print("   • Portfolio Manager (Final Decisions)")
    print("=" * 70)
    
    all_agent_results = {}
    
    for ticker in tickers:
        if ticker not in ticker_data:
            continue
            
        print(f"\n🎯 ANALYZING {ticker}")
        print("-" * 50)
        
        data = ticker_data[ticker]
        agent_results = {}
        
        # 1. Ben Graham Analysis
        print(f"\n🔍 1. BEN GRAHAM (Value Investing)...")
        ben_graham_result = run_ben_graham_agent(llm, ticker, data)
        agent_results['ben_graham'] = ben_graham_result
        
        # 2. Warren Buffett Analysis
        print(f"\n🔍 2. WARREN BUFFETT (Long-term Value)...")
        warren_buffett_result = run_warren_buffett_agent(llm, ticker, data)
        agent_results['warren_buffett'] = warren_buffett_result
        
        # 3. Charlie Munger Analysis
        print(f"\n🔍 3. CHARLIE MUNGER (Quality & Value)...")
        charlie_munger_result = run_charlie_munger_agent(llm, ticker, data)
        agent_results['charlie_munger'] = charlie_munger_result
        
        # 4. Technical Analyst
        print(f"\n🔍 4. TECHNICAL ANALYST (Chart Analysis)...")
        technical_result = run_technical_agent(llm, ticker, data)
        agent_results['technical_analyst'] = technical_result
        
        # 5. Risk Manager
        print(f"\n🔍 5. RISK MANAGER (Portfolio Risk)...")
        risk_result = run_risk_agent(llm, ticker, data)
        agent_results['risk_manager'] = risk_result
        
        # 6. Portfolio Manager (Final Decision)
        print(f"\n🔍 6. PORTFOLIO MANAGER (Final Decision)...")
        portfolio_result = run_portfolio_agent(llm, ticker, agent_results, data)
        agent_results['portfolio_manager'] = portfolio_result
        
        all_agent_results[ticker] = agent_results
        
        # Display results for this ticker
        display_ticker_results(ticker, agent_results)
    
    # Display final comparison
    display_final_comparison(all_agent_results, ticker_data)

def run_ben_graham_agent(llm, ticker, data):
    """Run Ben Graham value investing agent"""
    
    prompt = f"""
    You are Ben Graham, the father of value investing. Analyze {ticker} based on these metrics:
    
    Current Price: ${data['current_price']}
    P/E Ratio: {data['pe_ratio']:.2f}
    P/B Ratio: {data['pb_ratio']:.2f}
    Dividend Yield: {data['dividend_yield']*100:.2f}%
    ROE: {data['roe']*100:.2f}%
    Debt to Equity: {data['debt_to_equity']:.2f}
    Revenue Growth: {data['revenue_growth']*100:.2f}%
    
    Apply Ben Graham's value investing principles:
    1. P/E ratio should be below 15
    2. P/B ratio should be below 1.5
    3. Positive dividend yield
    4. Positive ROE
    5. Low debt levels
    
    Provide your analysis in JSON format:
    {{
        "action": "BUY" or "HOLD" or "SELL",
        "confidence": 0-100,
        "reasoning": "Your detailed analysis as Ben Graham",
        "key_insights": ["insight1", "insight2", "insight3"],
        "risk_factors": ["risk1", "risk2"],
        "price_target": estimated_fair_value
    }}
    """
    
    try:
        response = llm.invoke(prompt)
        result = json.loads(response.content)
        print(f"   ✅ Action: {result.get('action', 'N/A')} (Confidence: {result.get('confidence', 'N/A')}%)")
        return result
    except:
        return {"action": "HOLD", "confidence": 50, "reasoning": "Analysis error", "key_insights": [], "risk_factors": [], "price_target": data['current_price']}

def run_warren_buffett_agent(llm, ticker, data):
    """Run Warren Buffett long-term value agent"""
    
    prompt = f"""
    You are Warren Buffett, the Oracle of Omaha. Analyze {ticker} for long-term value:
    
    Current Price: ${data['current_price']}
    Market Cap: ${data['market_cap']:,}
    ROE: {data['roe']*100:.2f}%
    Revenue Growth: {data['revenue_growth']*100:.2f}%
    Debt to Equity: {data['debt_to_equity']:.2f}
    Dividend Yield: {data['dividend_yield']*100:.2f}%
    Beta: {data['beta']:.3f}
    
    Apply Warren Buffett's principles:
    1. Is this a business you understand?
    2. Does it have a durable competitive advantage?
    3. Is management competent and honest?
    4. Is the price attractive relative to intrinsic value?
    5. Long-term growth potential
    
    Provide your analysis in JSON format:
    {{
        "action": "BUY" or "HOLD" or "SELL",
        "confidence": 0-100,
        "reasoning": "Your detailed analysis as Warren Buffett",
        "key_insights": ["insight1", "insight2", "insight3"],
        "risk_factors": ["risk1", "risk2"],
        "price_target": estimated_intrinsic_value
    }}
    """
    
    try:
        response = llm.invoke(prompt)
        result = json.loads(response.content)
        print(f"   ✅ Action: {result.get('action', 'N/A')} (Confidence: {result.get('confidence', 'N/A')}%)")
        return result
    except:
        return {"action": "HOLD", "confidence": 50, "reasoning": "Analysis error", "key_insights": [], "risk_factors": [], "price_target": data['current_price']}

def run_charlie_munger_agent(llm, ticker, data):
    """Run Charlie Munger quality and value agent"""
    
    prompt = f"""
    You are Charlie Munger, Warren Buffett's partner. Analyze {ticker} for quality and value:
    
    Current Price: ${data['current_price']}
    P/E Ratio: {data['pe_ratio']:.2f}
    ROE: {data['roe']*100:.2f}%
    Revenue Growth: {data['revenue_growth']*100:.2f}%
    Beta: {data['beta']:.3f}
    Dividend Yield: {data['dividend_yield']*100:.2f}%
    Debt to Equity: {data['debt_to_equity']:.2f}
    
    Apply Charlie Munger's principles:
    1. Quality over quantity
    2. Mental models and multidisciplinary thinking
    3. Long-term compound growth
    4. Margin of safety
    5. Circle of competence
    
    Provide your analysis in JSON format:
    {{
        "action": "BUY" or "HOLD" or "SELL",
        "confidence": 0-100,
        "reasoning": "Your detailed analysis as Charlie Munger",
        "key_insights": ["insight1", "insight2", "insight3"],
        "risk_factors": ["risk1", "risk2"],
        "price_target": estimated_fair_value
    }}
    """
    
    try:
        response = llm.invoke(prompt)
        result = json.loads(response.content)
        print(f"   ✅ Action: {result.get('action', 'N/A')} (Confidence: {result.get('confidence', 'N/A')}%)")
        return result
    except:
        return {"action": "HOLD", "confidence": 50, "reasoning": "Analysis error", "key_insights": [], "risk_factors": [], "price_target": data['current_price']}

def run_technical_agent(llm, ticker, data):
    """Run technical analysis agent"""
    
    price_data = [p.close for p in data['prices'][-20:]] if data['prices'] else [data['current_price']]
    
    prompt = f"""
    You are a Technical Analyst. Analyze {ticker} based on price action and technical indicators:
    
    Current Price: ${data['current_price']}
    Beta: {data['beta']:.3f}
    Recent Price Trend: {price_data[-5:] if len(price_data) >= 5 else price_data}
    Market Cap: ${data['market_cap']:,}
    
    Analyze:
    1. Price trends and patterns
    2. Support and resistance levels
    3. Momentum indicators
    4. Volume analysis
    5. Technical signals
    
    Provide your analysis in JSON format:
    {{
        "action": "BUY" or "HOLD" or "SELL",
        "confidence": 0-100,
        "reasoning": "Your detailed technical analysis",
        "key_insights": ["insight1", "insight2", "insight3"],
        "risk_factors": ["risk1", "risk2"],
        "price_target": technical_price_target
    }}
    """
    
    try:
        response = llm.invoke(prompt)
        result = json.loads(response.content)
        print(f"   ✅ Action: {result.get('action', 'N/A')} (Confidence: {result.get('confidence', 'N/A')}%)")
        return result
    except:
        return {"action": "HOLD", "confidence": 50, "reasoning": "Analysis error", "key_insights": [], "risk_factors": [], "price_target": data['current_price']}

def run_risk_agent(llm, ticker, data):
    """Run risk management agent"""
    
    prompt = f"""
    You are a Risk Manager. Analyze {ticker} for portfolio risk:
    
    Current Price: ${data['current_price']}
    Beta: {data['beta']:.3f}
    Debt to Equity: {data['debt_to_equity']:.2f}
    Market Cap: ${data['market_cap']:,}
    ROE: {data['roe']*100:.2f}%
    Revenue Growth: {data['revenue_growth']*100:.2f}%
    
    Assess:
    1. Market risk (beta)
    2. Credit risk (debt levels)
    3. Liquidity risk
    4. Concentration risk
    5. Overall portfolio impact
    
    Provide your analysis in JSON format:
    {{
        "action": "BUY" or "HOLD" or "SELL",
        "confidence": 0-100,
        "reasoning": "Your detailed risk analysis",
        "key_insights": ["insight1", "insight2", "insight3"],
        "risk_factors": ["risk1", "risk2"],
        "risk_level": "LOW" or "MEDIUM" or "HIGH"
    }}
    """
    
    try:
        response = llm.invoke(prompt)
        result = json.loads(response.content)
        print(f"   ✅ Action: {result.get('action', 'N/A')} (Confidence: {result.get('confidence', 'N/A')}%)")
        return result
    except:
        return {"action": "HOLD", "confidence": 50, "reasoning": "Analysis error", "key_insights": [], "risk_factors": [], "risk_level": "MEDIUM"}

def run_portfolio_agent(llm, ticker, agent_results, data):
    """Run portfolio manager final decision agent"""
    
    # Aggregate previous analyses
    buy_count = sum(1 for result in agent_results.values() if result.get('action') == 'BUY')
    hold_count = sum(1 for result in agent_results.values() if result.get('action') == 'HOLD')
    sell_count = sum(1 for result in agent_results.values() if result.get('action') == 'SELL')
    
    prompt = f"""
    You are a Portfolio Manager making the final investment decision for {ticker}.
    
    Current Price: ${data['current_price']}
    Market Cap: ${data['market_cap']:,}
    
    Agent Consensus:
    - BUY: {buy_count} agents
    - HOLD: {hold_count} agents
    - SELL: {sell_count} agents
    
    Individual Agent Results:
    {json.dumps(agent_results, indent=2)}
    
    Make the final portfolio decision considering:
    1. Agent consensus
    2. Risk-return profile
    3. Portfolio diversification
    4. Market conditions
    5. Position sizing
    
    Provide your final decision in JSON format:
    {{
        "action": "BUY" or "HOLD" or "SELL",
        "confidence": 0-100,
        "reasoning": "Your final portfolio decision reasoning",
        "position_size": "percentage of portfolio",
        "key_insights": ["insight1", "insight2", "insight3"],
        "risk_factors": ["risk1", "risk2"],
        "price_target": final_price_target
    }}
    """
    
    try:
        response = llm.invoke(prompt)
        result = json.loads(response.content)
        print(f"   ✅ Final Decision: {result.get('action', 'N/A')} (Confidence: {result.get('confidence', 'N/A')}%)")
        return result
    except:
        return {"action": "HOLD", "confidence": 50, "reasoning": "Analysis error", "key_insights": [], "risk_factors": [], "position_size": "0%", "price_target": data['current_price']}

def display_ticker_results(ticker, agent_results):
    """Display results for a specific ticker"""
    
    print(f"\n🎯 ANALYSIS RESULTS FOR {ticker}")
    print("=" * 50)
    
    # Calculate consensus
    buy_count = sum(1 for result in agent_results.values() if result.get('action') == 'BUY')
    hold_count = sum(1 for result in agent_results.values() if result.get('action') == 'HOLD')
    sell_count = sum(1 for result in agent_results.values() if result.get('action') == 'SELL')
    total_agents = len(agent_results)
    
    avg_confidence = sum(result.get('confidence', 0) for result in agent_results.values()) / total_agents if total_agents > 0 else 0
    
    print(f"📊 CONSENSUS:")
    print(f"   BUY: {buy_count} agents ({buy_count/total_agents:.1%})")
    print(f"   HOLD: {hold_count} agents ({hold_count/total_agents:.1%})")
    print(f"   SELL: {sell_count} agents ({sell_count/total_agents:.1%})")
    print(f"   Average Confidence: {avg_confidence:.1f}%")
    
    # Determine consensus
    if buy_count > hold_count and buy_count > sell_count:
        consensus_action = "BUY"
    elif sell_count > hold_count and sell_count > buy_count:
        consensus_action = "SELL"
    else:
        consensus_action = "HOLD"
    
    print(f"\n🎯 CONSENSUS: {consensus_action}")
    
    # Display individual results
    print(f"\n📋 AGENT RESULTS:")
    for agent_name, result in agent_results.items():
        print(f"   {agent_name.replace('_', ' ').title()}: {result.get('action', 'N/A')} ({result.get('confidence', 'N/A')}%)")

def display_final_comparison(all_agent_results, ticker_data):
    """Display final comparison between all tickers"""
    
    print(f"\n{'='*70}")
    print(f"🎯 FINAL COMPARISON & RECOMMENDATIONS")
    print(f"{'='*70}")
    
    for ticker, agent_results in all_agent_results.items():
        buy_count = sum(1 for result in agent_results.values() if result.get('action') == 'BUY')
        hold_count = sum(1 for result in agent_results.values() if result.get('action') == 'HOLD')
        sell_count = sum(1 for result in agent_results.values() if result.get('action') == 'SELL')
        total_agents = len(agent_results)
        avg_confidence = sum(result.get('confidence', 0) for result in agent_results.values()) / total_agents if total_agents > 0 else 0
        
        print(f"\n📊 {ticker} SUMMARY:")
        print(f"   Consensus: {'BUY' if buy_count > hold_count and buy_count > sell_count else 'SELL' if sell_count > hold_count and sell_count > buy_count else 'HOLD'}")
        print(f"   BUY: {buy_count}/{total_agents} agents")
        print(f"   Confidence: {avg_confidence:.1f}%")
        
        # Show portfolio manager's final decision
        if 'portfolio_manager' in agent_results:
            pm_result = agent_results['portfolio_manager']
            print(f"   Final Decision: {pm_result.get('action', 'N/A')}")
            print(f"   Position Size: {pm_result.get('position_size', 'N/A')}")
            print(f"   Price Target: ${pm_result.get('price_target', 'N/A')}")
        
        # Show key financial metrics
        if ticker in ticker_data:
            data = ticker_data[ticker]
            print(f"   Key Metrics: P/E {data['pe_ratio']:.1f}, Div {data['dividend_yield']*100:.1f}%, ROE {data['roe']*100:.1f}%")
    
    print(f"\n💡 FINAL RECOMMENDATION:")
    print(f"   Based on comprehensive AI analysis using Groq's Llama 3.3 70B model")
    print(f"   All stocks analyzed by 6 legendary investor agents")
    print(f"   Consider the consensus and individual agent insights for your investment decision")

def main():
    """Main function"""
    # You can modify the tickers here
    tickers = ["VZ", "CMCSA"]  # Verizon and Comcast
    
    print("🚀 AI HEDGE FUND - YAHOO FINANCE AGENTS")
    print("=" * 70)
    print(f"🎯 Target Stocks: {', '.join(tickers)}")
    print("=" * 70)
    
    run_yahoo_agents_hedge_fund(tickers)

if __name__ == "__main__":
    main()
