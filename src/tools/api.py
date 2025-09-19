import os
import pandas as pd
import requests
import yfinance as yf
from datetime import datetime
from typing import List, Optional

from data.cache import get_cache
from data.models import (
    CompanyNews,
    CompanyNewsResponse,
    FinancialMetrics,
    FinancialMetricsResponse,
    Price,
    PriceResponse,
    LineItem,
    LineItemResponse,
    InsiderTrade,
    InsiderTradeResponse,
)

# Global cache instance
_cache = get_cache()


def get_prices(ticker: str, start_date: str, end_date: str) -> List[Price]:
    """Fetch price data using Yahoo Finance."""
    return get_yahoo_prices(ticker, start_date, end_date)


def get_financial_metrics(
    ticker: str,
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
) -> List[FinancialMetrics]:
    """Fetch financial metrics using Yahoo Finance."""
    # Convert Yahoo Finance data to FinancialMetrics format
    financial_info = get_yahoo_financial_info(ticker)
    
    # Create a FinancialMetrics object from Yahoo Finance data
    metrics = FinancialMetrics(
        ticker=ticker,
        report_period=end_date,
        market_cap=financial_info.get('market_cap', 0),
        enterprise_value=financial_info.get('enterprise_value', 0),
        pe_ratio=financial_info.get('price_to_earnings_ratio', 0),
        pb_ratio=financial_info.get('price_to_book_ratio', 0),
        ps_ratio=financial_info.get('price_to_sales_ratio', 0),
        ev_to_ebitda=financial_info.get('enterprise_value_to_ebitda_ratio', 0),
        ev_to_revenue=financial_info.get('enterprise_value_to_revenue_ratio', 0),
        gross_margin=financial_info.get('gross_margin', 0),
        operating_margin=financial_info.get('operating_margin', 0),
        net_margin=financial_info.get('net_margin', 0),
        roe=financial_info.get('return_on_equity', 0),
        roa=financial_info.get('return_on_assets', 0),
        debt_to_equity=financial_info.get('debt_to_equity', 0),
        current_ratio=financial_info.get('current_ratio', 0),
        quick_ratio=financial_info.get('quick_ratio', 0),
        revenue_growth=financial_info.get('revenue_growth', 0),
        earnings_growth=financial_info.get('earnings_growth', 0),
        book_value_per_share=financial_info.get('book_value_per_share', 0),
        earnings_per_share=financial_info.get('earnings_per_share', 0),
        free_cash_flow=financial_info.get('free_cash_flow', 0),
        operating_cash_flow=financial_info.get('operating_cash_flow', 0),
        total_debt=financial_info.get('total_debt', 0),
        total_cash=financial_info.get('total_cash', 0),
        shares_outstanding=financial_info.get('shares_outstanding', 0),
        dividend_yield=financial_info.get('dividend_yield', 0) / 100 if financial_info.get('dividend_yield') else 0,
        payout_ratio=financial_info.get('payout_ratio', 0),
        beta=financial_info.get('beta', 0)
    )
    
    return [metrics]


def search_line_items(
    ticker: str,
    line_items: List[str],
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
) -> List[LineItem]:
    """Fetch line items using Yahoo Finance data."""
    # Get Yahoo Finance financials data
    financials = get_yahoo_financials(ticker)
    
    # Map common line items to Yahoo Finance data
    line_item_mapping = {
        'earnings_per_share': 'eps',
        'revenue': 'totalRevenue',
        'net_income': 'netIncome',
        'book_value_per_share': 'bookValue',
        'total_assets': 'totalAssets',
        'total_liabilities': 'totalLiab',
        'current_assets': 'totalCurrentAssets',
        'current_liabilities': 'totalCurrentLiabilities',
        'dividends_and_other_cash_distributions': 'dividendsPaid',
        'outstanding_shares': 'sharesOutstanding'
    }
    
    results = []
    for line_item in line_items:
        if line_item in line_item_mapping:
            yahoo_key = line_item_mapping[line_item]
            value = financials.get(yahoo_key, 0)
            
            # Create LineItem object
            line_item_obj = LineItem(
                ticker=ticker,
                line_item=line_item,
                value=value,
                report_period=end_date,
                period=period
            )
            results.append(line_item_obj)
    
    return results[:limit]


def get_insider_trades(
    ticker: str,
    end_date: str,
    start_date: Optional[str] = None,
    limit: int = 1000,
) -> List[InsiderTrade]:
    """Fetch insider trades - Yahoo Finance doesn't provide this data, return empty list."""
    # Yahoo Finance doesn't provide insider trading data
    # Return empty list for now
    return []


def get_company_news(
    ticker: str,
    end_date: str,
    start_date: Optional[str] = None,
    limit: int = 1000,
) -> List[CompanyNews]:
    """Fetch company news using Yahoo Finance."""
    return get_yahoo_news(ticker, limit)



def get_market_cap(
    ticker: str,
    end_date: str,
) -> Optional[float]:
    """Fetch market cap from the API."""
    financial_metrics = get_financial_metrics(ticker, end_date)
    market_cap = financial_metrics[0].market_cap
    if not market_cap:
        return None

    return market_cap


def prices_to_df(prices: List[Price]) -> pd.DataFrame:
    """Convert prices to a DataFrame."""
    df = pd.DataFrame([p.model_dump() for p in prices])
    df["Date"] = pd.to_datetime(df["time"])
    df.set_index("Date", inplace=True)
    numeric_cols = ["open", "close", "high", "low", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.sort_index(inplace=True)
    return df


# Update the get_price_data function to use the new functions
def get_price_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    prices = get_prices(ticker, start_date, end_date)
    return prices_to_df(prices)


# ============================================================================
# YAHOO FINANCE API FUNCTIONS (FREE ALTERNATIVE)
# ============================================================================

def get_yahoo_prices(ticker: str, start_date: str, end_date: str) -> List[Price]:
    """Fetch price data from Yahoo Finance (FREE)."""
    try:
        # Create yfinance ticker object
        yf_ticker = yf.Ticker(ticker)
        
        # Download historical data
        hist = yf_ticker.history(start=start_date, end=end_date)
        
        if hist.empty:
            return []
        
        # Convert to our Price format
        prices = []
        for date, row in hist.iterrows():
            price = Price(
                open=float(row['Open']),
                close=float(row['Close']),
                high=float(row['High']),
                low=float(row['Low']),
                volume=int(row['Volume']),
                time=date.strftime('%Y-%m-%d')
            )
            prices.append(price)
        
        return prices
        
    except Exception as e:
        print(f"Error fetching Yahoo Finance data for {ticker}: {e}")
        return []


def get_yahoo_financial_info(ticker: str) -> dict:
    """Get basic financial information from Yahoo Finance (FREE)."""
    try:
        yf_ticker = yf.Ticker(ticker)
        info = yf_ticker.info
        
        # Extract key financial metrics
        financial_info = {
            'market_cap': info.get('marketCap'),
            'enterprise_value': info.get('enterpriseValue'),
            'price_to_earnings_ratio': info.get('trailingPE'),
            'price_to_book_ratio': info.get('priceToBook'),
            'price_to_sales_ratio': info.get('priceToSalesTrailing12Months'),
            'enterprise_value_to_ebitda_ratio': info.get('enterpriseToEbitda'),
            'enterprise_value_to_revenue_ratio': info.get('enterpriseToRevenue'),
            'gross_margin': info.get('grossMargins'),
            'operating_margin': info.get('operatingMargins'),
            'net_margin': info.get('profitMargins'),
            'return_on_equity': info.get('returnOnEquity'),
            'return_on_assets': info.get('returnOnAssets'),
            'debt_to_equity': info.get('debtToEquity'),
            'current_ratio': info.get('currentRatio'),
            'quick_ratio': info.get('quickRatio'),
            'revenue_growth': info.get('revenueGrowth'),
            'earnings_growth': info.get('earningsGrowth'),
            'book_value_per_share': info.get('bookValue'),
            'earnings_per_share': info.get('trailingEps'),
            'free_cash_flow': info.get('freeCashflow'),
            'operating_cash_flow': info.get('operatingCashflow'),
            'total_debt': info.get('totalDebt'),
            'total_cash': info.get('totalCash'),
            'shares_outstanding': info.get('sharesOutstanding'),
            'dividend_yield': info.get('dividendYield'),
            'payout_ratio': info.get('payoutRatio'),
            'beta': info.get('beta'),
            '52_week_high': info.get('fiftyTwoWeekHigh'),
            '52_week_low': info.get('fiftyTwoWeekLow'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'company_name': info.get('longName'),
            'currency': info.get('currency'),
        }
        
        return financial_info
        
    except Exception as e:
        print(f"Error fetching Yahoo Finance info for {ticker}: {e}")
        return {}


def get_yahoo_news(ticker: str, limit: int = 10) -> List[CompanyNews]:
    """Get company news from Yahoo Finance (FREE)."""
    try:
        yf_ticker = yf.Ticker(ticker)
        news = yf_ticker.news
        
        if not news:
            return []
        
        # Convert to our CompanyNews format
        company_news = []
        for article in news[:limit]:
            news_item = CompanyNews(
                ticker=ticker,
                title=article.get('title', ''),
                author=article.get('publisher', ''),
                source=article.get('publisher', ''),
                date=datetime.fromtimestamp(article.get('providerPublishTime', 0)).strftime('%Y-%m-%d'),
                url=article.get('link', ''),
                sentiment=None  # Yahoo Finance doesn't provide sentiment
            )
            company_news.append(news_item)
        
        return company_news
        
    except Exception as e:
        print(f"Error fetching Yahoo Finance news for {ticker}: {e}")
        return []


def get_yahoo_financials(ticker: str) -> dict:
    """Get financial statements from Yahoo Finance (FREE)."""
    try:
        yf_ticker = yf.Ticker(ticker)
        
        # Get financial statements
        financials = yf_ticker.financials
        balance_sheet = yf_ticker.balance_sheet
        cash_flow = yf_ticker.cashflow
        
        return {
            'income_statement': financials.to_dict() if not financials.empty else {},
            'balance_sheet': balance_sheet.to_dict() if not balance_sheet.empty else {},
            'cash_flow': cash_flow.to_dict() if not cash_flow.empty else {}
        }
        
    except Exception as e:
        print(f"Error fetching Yahoo Finance financials for {ticker}: {e}")
        return {}


# ============================================================================
# UNIFIED API FUNCTIONS (AUTO-SELECT BEST AVAILABLE)
# ============================================================================

def get_prices_unified(ticker: str, start_date: str, end_date: str, use_yahoo: bool = True) -> List[Price]:
    """Get prices from the best available source."""
    if use_yahoo:
        # Try Yahoo Finance first (free)
        prices = get_yahoo_prices(ticker, start_date, end_date)
        if prices:
            return prices
    
    # Fallback to Financial Datasets API
    return get_prices(ticker, start_date, end_date)


def get_financial_info_unified(ticker: str, use_yahoo: bool = True) -> dict:
    """Get financial info from the best available source."""
    if use_yahoo:
        # Try Yahoo Finance first (free)
        info = get_yahoo_financial_info(ticker)
        if info:
            return info
    
    # Fallback to Financial Datasets API
    try:
        financial_metrics = get_financial_metrics(ticker, datetime.now().strftime('%Y-%m-%d'))
        if financial_metrics:
            return financial_metrics[0].model_dump()
    except:
        pass
    
    return {}


def get_news_unified(ticker: str, limit: int = 10, use_yahoo: bool = True) -> List[CompanyNews]:
    """Get news from the best available source."""
    if use_yahoo:
        # Try Yahoo Finance first (free)
        news = get_yahoo_news(ticker, limit)
        if news:
            return news
    
    # Fallback to Financial Datasets API
    try:
        return get_company_news(ticker, datetime.now().strftime('%Y-%m-%d'), limit=limit)
    except:
        pass
    
    return []
