"""
This module provides tools for retrieving detailed information, business summaries, and historical data
for stock market ticker symbols using the Yahoo Finance API. It utilizes the yfinance library for data retrieval
and the Langchain tools for structured data handling.

Functions:
    get_ticker_info(ticker_symbol: str) -> str:
        Retrieves detailed information about a specified stock market ticker symbol.
        
    get_business_summary(ticker_symbol: str) -> str:
        Retrieves the business summary for a specified stock market ticker symbol.
        
    get_ticker_history(ticker_symbol: str, period: str) -> str:
        Retrieves historical data for a specified stock market ticker symbol over a given period.
        
    get_ticker_info_tool() -> StructuredTool:
        Creates a StructuredTool for retrieving detailed ticker information.
        
    get_business_summary_tool() -> StructuredTool:
        Creates a StructuredTool for retrieving business summaries.
        
    get_ticker_history_tool() -> StructuredTool:
        Creates a StructuredTool for retrieving historical data.
"""

import yfinance as yf
from langchain.tools import StructuredTool

def get_ticker_info(ticker_symbol: str) -> str:
    """
    Retrieves detailed information about a specified stock market ticker symbol.
    
    Args:
        ticker_symbol (str): The ticker symbol of the stock to retrieve information for.
        
    Returns:
        str: A string containing the detailed information of the stock.
    """
    ticker = yf.Ticker(ticker_symbol)
    return ticker.info

def get_business_summary(ticker_symbol: str) -> str:
    """
    Retrieves the business summary for a specified stock market ticker symbol.
    
    Args:
        ticker_symbol (str): The ticker symbol of the stock to retrieve the business summary for.
        
    Returns:
        str: A string containing the business summary of the stock.
    """
    ticker = yf.Ticker(ticker_symbol)
    return ticker.info['longBusinessSummary']

def get_ticker_history(ticker_symbol: str, period: str) -> str:
    """
    Retrieves historical data for a specified stock market ticker symbol over a given period.
    
    Args:
        ticker_symbol (str): The ticker symbol of the stock to retrieve historical data for.
        period (str): The period over which to retrieve historical data (e.g., '1d', '5d', '1mo', '1y', '5y', 'max').
        
    Returns:
        str: A string containing the historical data of the stock.
    """
    ticker = yf.Ticker(ticker_symbol)
    history = str(ticker.history(period=period))
    return history

def get_ticker_info_tool():
    """
    Creates a StructuredTool for retrieving detailed ticker information.
    
    Returns:
        StructuredTool: A tool for retrieving detailed ticker information.
    """
    description = (
        "Useful for when you need detailed ticker information about a company or a stock symbol. "
        "Useful if somebody asks 'I need detailed information for companyXXX' "
        "Useful if somebody asks 'Give me a detailed overview for companyXXX' "
    )

    return StructuredTool.from_function(
        func=get_ticker_info, name="yf_get_ticker_info", description=description
    )

def get_business_summary_tool():
    """
    Creates a StructuredTool for retrieving business summaries.
    
    Returns:
        StructuredTool: A tool for retrieving business summaries.
    """
    description = (
        "Useful for when you need summary information about a company or a stock symbol. "
        "Useful if somebody asks 'I need a summary for companyXXX' "
        "Useful if somebody asks 'Give me a summary for companyXXX' "
    )

    return StructuredTool.from_function(
        func=get_business_summary, name="yf_get_business_summary", description=description
    )
    
def get_ticker_history_tool():
    """
    Creates a StructuredTool for retrieving historical data.
    
    Returns:
        StructuredTool: A tool for retrieving historical data.
    """
    description = (
        "Useful for when you need ticker history information about a company or a stock symbol for a period. "
        "Useful if somebody asks 'How did companyXXX perform for the last ....' "
        "Useful if somebody asks 'I need the ticker history information for companyXXX for the last ....' "        
    )

    return StructuredTool.from_function(
        func=get_ticker_history, name="yf_get_ticker_history", description=description
    )
