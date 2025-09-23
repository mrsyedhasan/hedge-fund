# AI Hedge Fund - Data Requirements

This document provides an exact list of data required to run and analyze each agent in the AI Hedge Fund system.

## 📊 Data Sources

All data comes from **Financial Datasets API** (`https://api.financialdatasets.ai/`):

### Free Data (No API Key Required)
- **AAPL** (Apple)
- **GOOGL** (Google/Alphabet) 
- **MSFT** (Microsoft)
- **NVDA** (NVIDIA)
- **TSLA** (Tesla)

### Paid Data (API Key Required)
- All other tickers require `FINANCIAL_DATASETS_API_KEY`

---

## 🔍 Data Types & Endpoints

### 1. **Price Data** (`get_prices`)
- **Endpoint**: `/prices/`
- **Parameters**: `ticker`, `start_date`, `end_date`, `interval=day`
- **Returns**: Daily OHLCV data
- **Fields**:
  - `open`, `close`, `high`, `low` (float)
  - `volume` (int)
  - `time` (string)

### 2. **Financial Metrics** (`get_financial_metrics`)
- **Endpoint**: `/financial-metrics/`
- **Parameters**: `ticker`, `end_date`, `period=ttm`, `limit=10`
- **Returns**: Key financial ratios and metrics
- **Fields** (60+ metrics including):
  - **Valuation**: `price_to_earnings_ratio`, `price_to_book_ratio`, `price_to_sales_ratio`
  - **Profitability**: `gross_margin`, `operating_margin`, `net_margin`, `return_on_equity`
  - **Liquidity**: `current_ratio`, `quick_ratio`, `cash_ratio`
  - **Leverage**: `debt_to_equity`, `debt_to_assets`, `interest_coverage`
  - **Growth**: `revenue_growth`, `earnings_growth`, `book_value_growth`
  - **Efficiency**: `asset_turnover`, `inventory_turnover`, `receivables_turnover`

### 3. **Line Items** (`search_line_items`)
- **Endpoint**: `/financials/search/line-items`
- **Parameters**: `ticker`, `line_items[]`, `end_date`, `period=ttm`, `limit=10`
- **Returns**: Detailed financial statement items
- **Common Fields**:
  - `capital_expenditure`, `depreciation_and_amortization`
  - `net_income`, `outstanding_shares`
  - `total_assets`, `total_liabilities`, `shareholders_equity`
  - `dividends_and_other_cash_distributions`
  - `issuance_or_purchase_of_equity_shares`
  - `gross_profit`, `revenue`, `free_cash_flow`
  - `working_capital`, `total_debt`, `cash_and_equivalents`
  - `interest_expense`, `operating_income`, `ebit`, `ebitda`

### 4. **Insider Trades** (`get_insider_trades`)
- **Endpoint**: `/insider-trades/`
- **Parameters**: `ticker`, `end_date`, `limit=1000`
- **Returns**: Insider buying/selling activity
- **Fields**:
  - `transaction_shares`, `transaction_price_per_share`, `transaction_value`
  - `shares_owned_before_transaction`, `shares_owned_after_transaction`
  - `transaction_date`, `filing_date`
  - `name`, `title`, `is_board_director`

### 5. **Company News** (`get_company_news`)
- **Endpoint**: `/news/`
- **Parameters**: `ticker`, `end_date`, `limit=100`
- **Returns**: Recent news articles
- **Fields**:
  - `title`, `author`, `source`, `date`, `url`
  - `sentiment` (positive/negative/neutral)

### 6. **Market Cap** (`get_market_cap`)
- **Endpoint**: `/company/facts/` or from financial metrics
- **Parameters**: `ticker`, `end_date`
- **Returns**: Current market capitalization

---

## 🤖 Agent Data Requirements

### **Warren Buffett Agent**
**Data Sources**: Financial Metrics + Line Items + Market Cap
- **Financial Metrics**: 10 periods (TTM)
- **Line Items**: 10 periods, 12 specific items
- **Market Cap**: Current value
- **Analysis**: ROE, debt levels, margins, consistency, moat, pricing power, book value growth, management quality, intrinsic value

### **Charlie Munger Agent**
**Data Sources**: Financial Metrics + Line Items + Market Cap
- **Financial Metrics**: 10 periods (TTM)
- **Line Items**: 10 periods, 12 specific items
- **Market Cap**: Current value
- **Analysis**: Similar to Buffett but with Munger's focus on quality businesses

### **Ben Graham Agent**
**Data Sources**: Financial Metrics + Line Items + Market Cap
- **Financial Metrics**: 10 periods (TTM)
- **Line Items**: 10 periods, 12 specific items
- **Market Cap**: Current value
- **Analysis**: Value investing principles, margin of safety

### **Technical Analysis Agent**
**Data Sources**: Price Data
- **Price Data**: Daily OHLCV for specified date range
- **Analysis**: Moving averages, RSI, MACD, Bollinger Bands, momentum, volatility

### **Sentiment Agent**
**Data Sources**: Insider Trades + Company News
- **Insider Trades**: Up to 1000 recent transactions
- **Company News**: Up to 100 recent articles
- **Analysis**: Insider sentiment + news sentiment

### **Valuation Agent**
**Data Sources**: Financial Metrics + Line Items
- **Financial Metrics**: 8 periods (TTM)
- **Line Items**: 8 periods, 12 specific items
- **Analysis**: DCF, P/E, P/B, EV/EBITDA, intrinsic value

### **Fundamentals Agent**
**Data Sources**: Financial Metrics
- **Financial Metrics**: 10 periods (TTM)
- **Analysis**: Financial health, profitability, growth, efficiency

### **Risk Manager**
**Data Sources**: Price Data
- **Price Data**: Daily OHLCV for specified date range
- **Analysis**: Volatility, correlation, position sizing, risk limits

### **Portfolio Manager**
**Data Sources**: All previous agent outputs
- **Input**: Signals from all other agents
- **Analysis**: Final trading decisions, position management

---

## 📋 Complete Data Checklist

### For Each Ticker:
- [ ] **Price Data**: Daily OHLCV (start_date to end_date)
- [ ] **Financial Metrics**: 10 periods TTM
- [ ] **Line Items**: 10 periods TTM, 12+ specific items
- [ ] **Insider Trades**: Up to 1000 recent transactions
- [ ] **Company News**: Up to 100 recent articles
- [ ] **Market Cap**: Current value

### Required Line Items:
- [ ] `capital_expenditure`
- [ ] `depreciation_and_amortization`
- [ ] `net_income`
- [ ] `outstanding_shares`
- [ ] `total_assets`
- [ ] `total_liabilities`
- [ ] `shareholders_equity`
- [ ] `dividends_and_other_cash_distributions`
- [ ] `issuance_or_purchase_of_equity_shares`
- [ ] `gross_profit`
- [ ] `revenue`
- [ ] `free_cash_flow`
- [ ] `working_capital`
- [ ] `total_debt`
- [ ] `cash_and_equivalents`
- [ ] `interest_expense`
- [ ] `operating_income`
- [ ] `ebit`
- [ ] `ebitda`

### Required Financial Metrics:
- [ ] `return_on_equity`
- [ ] `debt_to_equity`
- [ ] `operating_margin`
- [ ] `current_ratio`
- [ ] `gross_margin`
- [ ] `price_to_earnings_ratio`
- [ ] `price_to_book_ratio`
- [ ] `price_to_sales_ratio`
- [ ] `enterprise_value_to_ebitda_ratio`
- [ ] `free_cash_flow_yield`
- [ ] `revenue_growth`
- [ ] `earnings_growth`
- [ ] `book_value_growth`
- [ ] `asset_turnover`
- [ ] `inventory_turnover`
- [ ] `receivables_turnover`
- [ ] `days_sales_outstanding`
- [ ] `operating_cycle`
- [ ] `working_capital_turnover`
- [ ] `quick_ratio`
- [ ] `cash_ratio`
- [ ] `operating_cash_flow_ratio`
- [ ] `debt_to_assets`
- [ ] `interest_coverage`
- [ ] `earnings_per_share_growth`
- [ ] `free_cash_flow_growth`
- [ ] `operating_income_growth`
- [ ] `ebitda_growth`
- [ ] `payout_ratio`
- [ ] `earnings_per_share`
- [ ] `book_value_per_share`
- [ ] `free_cash_flow_per_share`

---

## 🚀 Quick Start

### For Free Stocks (AAPL, GOOGL, MSFT, NVDA, TSLA):
```bash
# No API key needed
python src/main.py --ticker AAPL,GOOGL,MSFT,NVDA,TSLA
```

### For Other Stocks:
```bash
# Set API key in .env file
echo "FINANCIAL_DATASETS_API_KEY=your-api-key" >> .env

# Run analysis
python src/main.py --ticker BRK.A,AMZN,GOOGL
```

### With Ollama/Mistral:
```bash
python src/main.py --ticker AAPL,MSFT,NVDA --ollama
```

---

## ⚠️ Important Notes

1. **Rate Limiting**: API has rate limits (429 errors handled with backoff)
2. **Data Freshness**: Financial data is typically 1-2 days behind
3. **Missing Data**: Some metrics may be null for certain companies
4. **Historical Limits**: Most data goes back 10+ years
5. **Caching**: Responses are cached to avoid redundant API calls

---

## 🔧 Troubleshooting

### Common Issues:
- **No data found**: Check if ticker is valid and has sufficient history
- **Rate limited**: Wait and retry (automatic backoff implemented)
- **Missing metrics**: Some companies may not have all financial data
- **API key required**: Set `FINANCIAL_DATASETS_API_KEY` in `.env` file

### Data Validation:
- Check if `financial_metrics` list is not empty
- Verify `line_items` has sufficient historical data (2+ periods)
- Ensure `prices` data covers the required date range
- Validate `insider_trades` and `company_news` are not empty
