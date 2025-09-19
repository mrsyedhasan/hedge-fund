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
    """Fetch price data from cache or API."""
    # Check cache first
    if cached_data := _cache.get_prices(ticker):
        # Filter cached data by date range and convert to Price objects
        filtered_data = [Price(**price) for price in cached_data if start_date <= price["time"] <= end_date]
        if filtered_data:
            return filtered_data

    # If not in cache or no data in range, fetch from API
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    url = f"https://api.financialdatasets.ai/prices/?ticker={ticker}&interval=day&interval_multiplier=1&start_date={start_date}&end_date={end_date}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {ticker} - {response.status_code} - {response.text}")

    # Parse response with Pydantic model
    price_response = PriceResponse(**response.json())
    prices = price_response.prices

    if not prices:
        return []

    # Cache the results as dicts
    _cache.set_prices(ticker, [p.model_dump() for p in prices])
    return prices


def get_financial_metrics(
    ticker: str,
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
) -> List[FinancialMetrics]:
    """Fetch financial metrics from cache or API."""
    # Check cache first
    if cached_data := _cache.get_financial_metrics(ticker):
        # Filter cached data by date and limit
        filtered_data = [FinancialMetrics(**metric) for metric in cached_data if metric["report_period"] <= end_date]
        filtered_data.sort(key=lambda x: x.report_period, reverse=True)
        if filtered_data:
            return filtered_data[:limit]

    # If not in cache or insufficient data, fetch from API
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    url = f"https://api.financialdatasets.ai/financial-metrics/?ticker={ticker}&report_period_lte={end_date}&limit={limit}&period={period}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {ticker} - {response.status_code} - {response.text}")

    # Parse response with Pydantic model
    metrics_response = FinancialMetricsResponse(**response.json())
    # Return the FinancialMetrics objects directly instead of converting to dict
    financial_metrics = metrics_response.financial_metrics

    if not financial_metrics:
        return []

    # Cache the results as dicts
    _cache.set_financial_metrics(ticker, [m.model_dump() for m in financial_metrics])
    return financial_metrics


def search_line_items(
    ticker: str,
    line_items: List[str],
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
) -> List[LineItem]:
    """Fetch line items from API."""
    # If not in cache or insufficient data, fetch from API
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    url = "https://api.financialdatasets.ai/financials/search/line-items"

    body = {
        "tickers": [ticker],
        "line_items": line_items,
        "end_date": end_date,
        "period": period,
        "limit": limit,
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {ticker} - {response.status_code} - {response.text}")
    data = response.json()
    response_model = LineItemResponse(**data)
    search_results = response_model.search_results
    if not search_results:
        return []

    # Cache the results
    return search_results[:limit]


def get_insider_trades(
    ticker: str,
    end_date: str,
    start_date: Optional[str] = None,
    limit: int = 1000,
) -> List[InsiderTrade]:
    """Fetch insider trades from cache or API."""
    # Check cache first
    if cached_data := _cache.get_insider_trades(ticker):
        # Filter cached data by date range
        filtered_data = [InsiderTrade(**trade) for trade in cached_data 
                        if (start_date is None or (trade.get("transaction_date") or trade["filing_date"]) >= start_date)
                        and (trade.get("transaction_date") or trade["filing_date"]) <= end_date]
        filtered_data.sort(key=lambda x: x.transaction_date or x.filing_date, reverse=True)
        if filtered_data:
            return filtered_data

    # If not in cache or insufficient data, fetch from API
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    all_trades = []
    current_end_date = end_date
    
    while True:
        url = f"https://api.financialdatasets.ai/insider-trades/?ticker={ticker}&filing_date_lte={current_end_date}"
        if start_date:
            url += f"&filing_date_gte={start_date}"
        url += f"&limit={limit}"
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {ticker} - {response.status_code} - {response.text}")
        
        data = response.json()
        response_model = InsiderTradeResponse(**data)
        insider_trades = response_model.insider_trades
        
        if not insider_trades:
            break
            
        all_trades.extend(insider_trades)
        
        # Only continue pagination if we have a start_date and got a full page
        if not start_date or len(insider_trades) < limit:
            break
            
        # Update end_date to the oldest filing date from current batch for next iteration
        current_end_date = min(trade.filing_date for trade in insider_trades).split('T')[0]
        
        # If we've reached or passed the start_date, we can stop
        if current_end_date <= start_date:
            break

    if not all_trades:
        return []

    # Cache the results
    _cache.set_insider_trades(ticker, [trade.model_dump() for trade in all_trades])
    return all_trades


def get_company_news(
    ticker: str,
    end_date: str,
    start_date: Optional[str] = None,
    limit: int = 1000,
) -> List[CompanyNews]:
    """Fetch company news from cache or API."""
    # Check cache first
    if cached_data := _cache.get_company_news(ticker):
        # Filter cached data by date range
        filtered_data = [CompanyNews(**news) for news in cached_data 
                        if (start_date is None or news["date"] >= start_date)
                        and news["date"] <= end_date]
        filtered_data.sort(key=lambda x: x.date, reverse=True)
        if filtered_data:
            return filtered_data

    # If not in cache or insufficient data, fetch from API
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    all_news = []
    current_end_date = end_date
    
    while True:
        url = f"https://api.financialdatasets.ai/news/?ticker={ticker}&end_date={current_end_date}"
        if start_date:
            url += f"&start_date={start_date}"
        url += f"&limit={limit}"
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {ticker} - {response.status_code} - {response.text}")
        
        data = response.json()
        response_model = CompanyNewsResponse(**data)
        company_news = response_model.news
        
        if not company_news:
            break
            
        all_news.extend(company_news)
        
        # Only continue pagination if we have a start_date and got a full page
        if not start_date or len(company_news) < limit:
            break
            
        # Update end_date to the oldest date from current batch for next iteration
        current_end_date = min(news.date for news in company_news).split('T')[0]
        
        # If we've reached or passed the start_date, we can stop
        if current_end_date <= start_date:
            break

    if not all_news:
        return []

    # Cache the results
    _cache.set_company_news(ticker, [news.model_dump() for news in all_news])
    return all_news



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
