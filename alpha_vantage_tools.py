from langchain.agents import Tool
from langchain.tools.base import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

def search_symbols(company_name: str) -> str:
    """Searches a stock market symbol or a company."""
    alpha_vantage = AlphaVantageAPIWrapper()
    return alpha_vantage.search_symbols(company_name)

def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Gets the exchange rate for twu currencies."""
    alpha_vantage = AlphaVantageAPIWrapper()
    return alpha_vantage._get_exchange_rate(from_currency, to_currency)


def get_time_series_daily(ticker_symbol: str) -> str:
    """"Gets the daily time series for a stock market ticker symbol"""
    alpha_vantage = AlphaVantageAPIWrapper()
    return alpha_vantage._get_time_series_daily(ticker_symbol)


def get_time_series_weekly(ticker_symbol: str) -> str:
    """"Gets the weekly time series for a stock market ticker symbol"""
    alpha_vantage = AlphaVantageAPIWrapper()
    return alpha_vantage._get_time_series_weekly(ticker_symbol)


def get_market_news_sentiment(ticker_symbol: str) -> str:
    """"Gets the market news sentiment for a ticker"""
    alpha_vantage = AlphaVantageAPIWrapper()
    return alpha_vantage._get_market_news_sentiment(ticker_symbol)

def get_top_gainers_losers() -> str:
    """"Gets the top gainers and losers of the stock market"""
    alpha_vantage = AlphaVantageAPIWrapper()
    return alpha_vantage._get_top_gainers_losers()

def get_search_symbol_tool():
    description = (
        "Useful for when you need to search for a company or a stock symbol. "
        "Useful if somebody asks 'How is the stock market symbol for...' "    
        "Useful if somebody asks 'For which company stands this stock symbol...' "
    )

    return Tool(
        name="av_search_symbols",
        func=search_symbols,
        description=description,
    )


def get_time_series_daily_tool():
    description = (
        "Useful for when you need to get the daily time series for a company or a stock symbol. "
        "Useful if somebody asks 'How did the stock...perform the last time.' "    
        "Useful if somebody asks 'How did the stock...perform last year.' "
    )

    return Tool(
        name="av_get_time_series_daily",
        func=get_time_series_daily,
        description=description,
    )


def get_time_series_weekly_tool():
    description = (
        "Useful for when you need to get the daily time series for a company or a stock symbol. "
        "Useful if somebody asks 'How did the stock...perform the last years.' "    
        "Useful if somebody asks 'How does the stock perform...historically.' "
    )

    return Tool(
        name="av_get_time_series_weekly",
        func=get_time_series_weekly,
        description=description,
    )
    
    
    
def get_market_news_sentimen_tool():
    description = (
        "Useful for when you need to get the market news sentiment for a company or a stock symbol. "
        "Useful if somebody asks 'What is in the news about a company.' "    
        "Useful if somebody asks 'What is in the news about Microsoft, Google etc....' "
    )

    return Tool(
        name="av_get_market_news_sentiment",
        func=get_market_news_sentiment,
        description=description,
    )    


def get_top_gainers_losers_tool():
    description = (
        "Useful for when you need to get the top gainers and losers of the stock market. "
        "Useful if somebody asks 'What are the gainers and losers.' "    
        "Useful if somebody asks 'Which companies did perform well wich not?' "
    )

    return Tool(
        name="av_get_market_news_sentiment",
        func=get_market_news_sentiment,
        description=description,
    )    

def get_exchange_rate_tool():
    class ExchangeRateInputs(BaseModel):
        """Inputs to the get_exchange_rate tool."""
        from_currency: str = Field(
            description="currency to convert from"
        )
        to_currency: str = Field(
            description="currency to convert to"
        )
    
    
    
    description = (
        "Useful when the user asks for currency conversion."
        "Useful if somebody asks 'How much is one dollar in euro?' "    
        "Useful if somebody asks 'How many brazilian real is one euro?' "
    )

    return StructuredTool(
        name="av_get_exchange_rate",
        func=get_exchange_rate,
        description=description,
        args_schema=ExchangeRateInputs,
        return_direct=True,
    )
