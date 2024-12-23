#--------------基本數據獲取和篩選--------------
import yfinance as yf
import pandas as pd
from datetime import datetime

# 取得今天日期
date = datetime.now().strftime('%Y%m%d')

def get_stock_data(ticker_list, start_date, end_date):
    """
    獲取股票基本數據
    """
    stock_data = pd.DataFrame()
    for ticker in ticker_list:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        hist['Symbol'] = ticker
        stock_data = pd.concat([stock_data, hist])
    return stock_data


#--------------加入基本面數據--------------

def get_fundamental_data(ticker):
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        if info.get('trailingPE') is not None and info.get('marketCap') is not None and info.get('priceToBook') is not None and info.get('returnOnEquity') is not None:
            return {
                'Symbol': ticker,
                'MarketCap': info.get('marketCap'),
                'P/E': info.get('trailingPE'),
                'P/B': info.get('priceToBook'),
                'ROE': info.get('returnOnEquity')
            }
        else:
            return None
    except Exception as e:
        print(f"Error getting fundamental data for {ticker}: {e}")
        return None
    
#--------------使用範例--------------
def main():
    # 台股前50大市值股票（示例）
    ticker_list = ['2330.TW']  # 您可以擴充這個清單
    
    # 1. 獲取數據
    start_date = '2020-01-01'
    end_date = '2024-12-03'
    stock_data = get_stock_data(ticker_list, start_date, end_date)

    # 2. 加入基本面數據
    fundamental_data = pd.DataFrame([get_fundamental_data(ticker) for ticker in ticker_list])
    stock_data = stock_data.reset_index()
    stock_data = pd.merge(stock_data, fundamental_data, on='Symbol', how='left')
    stock_data = stock_data.reindex(columns=['Symbol', 'Date', 'MarketCap', 'Open', 'High', 'Low', 'Close', 'Volume', 'P/E', 'P/B', 'ROE', 'Dividends', 'Stock Splits'])
    stock_data['Date'] = pd.to_datetime(stock_data['Date']).dt.strftime('%Y%m%d')
    stock_data = stock_data.set_index('Symbol')

    stock_data.to_csv(f"stock_data_{date}.csv")
    print(f"\nData saved to {date}_stock_data.csv")
    return stock_data

if __name__ == "__main__":
    results = main()
    print(results)

