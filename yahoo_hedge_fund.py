#!/usr/bin/env python3
"""
Run Complete AI Hedge Fund using Yahoo Finance Data
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import create_workflow
from llm.models import AVAILABLE_MODELS, get_model
from graph.state import AgentState, show_agent_reasoning
from langchain_core.messages import HumanMessage
from tools.api import get_yahoo_financial_info, get_yahoo_prices
from datetime import datetime, timedelta

def run_yahoo_hedge_fund(tickers=["VZ", "CMCSA"]):
    """Run the complete AI hedge fund using Yahoo Finance data"""
    
    # Load environment variables
    load_dotenv()
    
    print("🚀 AI HEDGE FUND - YAHOO FINANCE EDITION")
    print("=" * 70)
    print(f"🎯 Analyzing: {', '.join(tickers)}")
    print("🤖 Using: Groq AI Models + Yahoo Finance Data")
    print("=" * 70)
    
    # Get Groq model
    groq_models = [model for model in AVAILABLE_MODELS if model.provider.value == "Groq"]
    if not groq_models:
        print("❌ No Groq models available.")
        return
    
    model = groq_models[0]
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
    
    # Run the AI hedge fund workflow
    print(f"\n🚀 Starting AI Hedge Fund Analysis...")
    print("=" * 70)
    print("📋 AI Agents in the workflow:")
    print("   • Ben Graham (Value Investing)")
    print("   • Warren Buffett (Long-term Value)")
    print("   • Charlie Munger (Quality & Value)")
    print("   • Bill Ackman (Activist Investing)")
    print("   • Cathie Wood (Growth & Innovation)")
    print("   • Stanley Druckenmiller (Macro & Momentum)")
    print("   • Technical Analyst (Chart Analysis)")
    print("   • Fundamentals Analyst (Financial Metrics)")
    print("   • Sentiment Analyst (Market Sentiment)")
    print("   • Valuation Analyst (Intrinsic Value)")
    print("   • Risk Manager (Portfolio Risk)")
    print("   • Portfolio Manager (Final Decisions)")
    print("=" * 70)
    
    try:
        # Create the workflow with all agents
        workflow = create_workflow([])  # Empty list means use all agents
        agent = workflow.compile()
        
        print(f"✅ Workflow created successfully!")
        
        # Prepare the analysis state
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        initial_state = {
            "messages": [
                HumanMessage(
                    content=f"Analyze {', '.join(tickers)} using all available AI agents and provide comprehensive investment recommendations based on Yahoo Finance data."
                )
            ],
            "data": {
                "tickers": tickers,
                "portfolio": {"cash": 100000, "positions": {}},
                "start_date": start_date,
                "end_date": end_date,
                "analyst_signals": {},
                "yahoo_data": ticker_data,  # Include Yahoo Finance data
            },
            "metadata": {
                "show_reasoning": True,
                "model_name": model.model_name,
                "model_provider": model.provider.value,
            }
        }
        
        print(f"\n🎯 Running AI Hedge Fund Analysis...")
        print("=" * 70)
        
        # Run the complete workflow
        final_state = agent.invoke(initial_state)
        
        print(f"\n✅ AI Hedge Fund Analysis Complete!")
        print("=" * 70)
        
        # Display comprehensive results
        display_hedge_fund_results(final_state, tickers, ticker_data)
        
    except Exception as e:
        print(f"❌ Error during hedge fund analysis: {e}")
        import traceback
        traceback.print_exc()

def display_hedge_fund_results(final_state, tickers, ticker_data):
    """Display comprehensive hedge fund results"""
    
    print(f"\n📊 AI HEDGE FUND RESULTS")
    print("=" * 70)
    
    # Display final state structure
    print(f"📈 Final State Keys: {list(final_state.keys())}")
    
    # Display messages
    if "messages" in final_state:
        print(f"\n💬 Total Messages: {len(final_state['messages'])}")
        
        # Show the last few messages (agent outputs)
        for i, message in enumerate(final_state["messages"][-3:], 1):
            print(f"\n--- Message {i} ---")
            print(f"Type: {type(message).__name__}")
            if hasattr(message, 'content'):
                content = message.content
                print(f"Content Length: {len(str(content))}")
                
                # Try to parse as JSON
                try:
                    parsed = json.loads(content)
                    print(f"✅ JSON Content:")
                    print(json.dumps(parsed, indent=2))
                except json.JSONDecodeError:
                    print(f"📝 Text Content: {content[:200]}...")
    
    # Display data
    if "data" in final_state:
        data = final_state["data"]
        print(f"\n📊 Data Analysis:")
        print(f"   Tickers: {data.get('tickers', [])}")
        print(f"   Portfolio: {data.get('portfolio', {})}")
        
        # Display analyst signals
        if "analyst_signals" in data:
            signals = data["analyst_signals"]
            print(f"\n🎯 ANALYST SIGNALS ({len(signals)} agents):")
            
            for agent_name, agent_analysis in signals.items():
                print(f"\n--- {agent_name.upper().replace('_', ' ')} ---")
                if isinstance(agent_analysis, dict):
                    for ticker in tickers:
                        if ticker in agent_analysis:
                            analysis = agent_analysis[ticker]
                            print(f"   {ticker}:")
                            print(f"     Action: {analysis.get('action', 'N/A')}")
                            print(f"     Confidence: {analysis.get('confidence', 'N/A')}%")
                            print(f"     Price Target: ${analysis.get('price_target', 'N/A')}")
                            print(f"     Reasoning: {analysis.get('reasoning', 'N/A')[:100]}...")
                else:
                    print(f"   Analysis: {agent_analysis}")
    
    # Display metadata
    if "metadata" in final_state:
        print(f"\n🔧 Metadata: {final_state['metadata']}")
    
    # Generate final recommendations
    generate_final_recommendations(final_state, tickers, ticker_data)

def generate_final_recommendations(final_state, tickers, ticker_data):
    """Generate final investment recommendations"""
    
    print(f"\n🎯 FINAL INVESTMENT RECOMMENDATIONS")
    print("=" * 70)
    
    if "data" not in final_state or "analyst_signals" not in final_state["data"]:
        print("❌ No analyst signals available for final recommendation.")
        return
    
    signals = final_state["data"]["analyst_signals"]
    
    for ticker in tickers:
        print(f"\n📊 {ticker} ANALYSIS:")
        print("-" * 50)
        
        # Show financial metrics
        if ticker in ticker_data:
            data = ticker_data[ticker]
            print(f"📈 Financial Metrics:")
            print(f"   Current Price: ${data['current_price']}")
            print(f"   Market Cap: ${data['market_cap']:,}" if data['market_cap'] else "   Market Cap: N/A")
            print(f"   P/E Ratio: {data['pe_ratio']:.2f}")
            print(f"   P/B Ratio: {data['pb_ratio']:.2f}")
            print(f"   Dividend Yield: {data['dividend_yield']*100:.2f}%")
            print(f"   ROE: {data['roe']*100:.2f}%")
            print(f"   Debt to Equity: {data['debt_to_equity']:.2f}")
            print(f"   Revenue Growth: {data['revenue_growth']*100:.2f}%")
            print(f"   Beta: {data['beta']:.3f}")
        
        # Aggregate recommendations for this ticker
        buy_count = 0
        hold_count = 0
        sell_count = 0
        total_confidence = 0
        valid_analyses = 0
        
        agent_recommendations = []
        
        for agent_name, agent_analysis in signals.items():
            if isinstance(agent_analysis, dict) and ticker in agent_analysis:
                analysis = agent_analysis[ticker]
                action = analysis.get('action', 'HOLD')
                confidence = analysis.get('confidence', 0)
                
                agent_recommendations.append({
                    'agent': agent_name,
                    'action': action,
                    'confidence': confidence,
                    'reasoning': analysis.get('reasoning', 'No reasoning provided')
                })
                
                if action == 'BUY':
                    buy_count += 1
                elif action == 'SELL':
                    sell_count += 1
                else:
                    hold_count += 1
                
                total_confidence += confidence
                valid_analyses += 1
        
        # Calculate consensus
        if valid_analyses > 0:
            avg_confidence = total_confidence / valid_analyses
            
            print(f"\n🎯 AI AGENT CONSENSUS:")
            print(f"   Total Agents: {valid_analyses}")
            print(f"   BUY: {buy_count} agents")
            print(f"   HOLD: {hold_count} agents") 
            print(f"   SELL: {sell_count} agents")
            print(f"   Average Confidence: {avg_confidence:.1f}%")
            
            # Determine consensus action
            if buy_count > hold_count and buy_count > sell_count:
                consensus_action = "BUY"
                consensus_strength = buy_count / valid_analyses
            elif sell_count > hold_count and sell_count > buy_count:
                consensus_action = "SELL"
                consensus_strength = sell_count / valid_analyses
            else:
                consensus_action = "HOLD"
                consensus_strength = hold_count / valid_analyses
            
            print(f"\n🎯 CONSENSUS RECOMMENDATION:")
            print(f"   Action: {consensus_action}")
            print(f"   Strength: {consensus_strength:.1%} of agents agree")
            print(f"   Confidence: {avg_confidence:.1f}%")
            
            # Display individual agent recommendations
            print(f"\n📋 INDIVIDUAL AGENT RECOMMENDATIONS:")
            for rec in agent_recommendations:
                print(f"   {rec['agent'].replace('_', ' ').title()}: {rec['action']} (Confidence: {rec['confidence']}%)")
                print(f"      Reasoning: {rec['reasoning'][:80]}...")
                print()
            
            # Final summary
            print(f"💡 FINAL SUMMARY FOR {ticker}:")
            if consensus_action == "BUY":
                print(f"   🟢 RECOMMENDATION: BUY {ticker}")
                print(f"   📈 The majority of AI agents recommend buying this stock")
                print(f"   💰 Consider this as a value opportunity")
            elif consensus_action == "SELL":
                print(f"   🔴 RECOMMENDATION: SELL {ticker}")
                print(f"   📉 The majority of AI agents recommend selling this stock")
                print(f"   ⚠️  Consider reducing or exiting your position")
            else:
                print(f"   🟡 RECOMMENDATION: HOLD {ticker}")
                print(f"   ⚖️  Mixed signals from AI agents")
                print(f"   🔍 Monitor closely for better entry/exit points")
            
            print(f"\n🎯 Risk Level: {'HIGH' if avg_confidence < 50 else 'MEDIUM' if avg_confidence < 75 else 'LOW'}")
            print(f"📊 Confidence: {avg_confidence:.1f}%")
        
        else:
            print(f"❌ No valid analyses available for {ticker}.")

def main():
    """Main function"""
    # You can modify the tickers here
    tickers = ["VZ", "CMCSA"]  # Verizon and Comcast
    
    print("🚀 AI HEDGE FUND - YAHOO FINANCE EDITION")
    print("=" * 70)
    print(f"🎯 Target Stocks: {', '.join(tickers)}")
    print("=" * 70)
    
    run_yahoo_hedge_fund(tickers)

if __name__ == "__main__":
    main()
