import yfinance as yf
from langchain.tools import StructuredTool

def get_ticker_info(ticker_symbol: str) -> str:
    """Gets the detailed information about a stock market ticker symbol"""
    ticker = yf.Ticker(ticker_symbol)
    return ticker.info

def get_business_summary(ticker_symbol: str) -> str:
    """Gets the business summary a stock market ticker symbol"""
    ticker = yf.Ticker(ticker_symbol)
    return ticker.info['longBusinessSummary']

def get_ticker_history(ticker_symbol: str, period: str) -> str:
    """Gets the information about a stock market ticker symbol history for a period"""
    ticker = yf.Ticker(ticker_symbol)
    history = str(ticker.history(period=period))
    return history


def get_ticker_info_tool():
    description = (
        "Useful for when you need detailed ticker information about a company or a stock symbol. "
        "Useful if somebody asks 'I need detailed information for companyXXX' "
        "Useful if somebody asks 'Give me a detailed overview for companyXXX' "
    )

    return StructuredTool.from_function(
        func=get_ticker_info, name="yf_get_ticker_info", description=description
    )


def get_business_summary_tool():
    description = (
        "Useful for when you need summary information about a company or a stock symbol. "
        "Useful if somebody asks 'I need a summary for companyXXX' "
        "Useful if somebody asks 'Give me a summary for companyXXX' "
    )

    return StructuredTool.from_function(
        func=get_business_summary, name="yf_get_business_summary", description=description
    )
    
    
def get_ticker_history_tool():
    description = (
        "Useful for when you need ticker history information about a company or a stock symbol for a period. "
        "Useful if somebody asks 'How did companyXXX perform for the last ....' "
        "Useful if somebody asks 'I need the ticker history information for companyXXX for the last ....' "        
    )

    return StructuredTool.from_function(
        func=get_ticker_history, name="yf_get_ticker_history", description=description
    )    