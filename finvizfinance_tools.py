from finvizfinance.quote import finvizfinance
from langchain.tools import StructuredTool

def get_fundamental_data(ticker_symbol):
 """
    Retrieves fundamental data about a specified stock market ticker symbol.
    
    Args:
        ticker_symbol (str): The ticker symbol of the stock to retrieve information for.
        
    Returns:
        dict: A dictionary containing the fundamental data of the stock.
"""
 stock = finvizfinance(ticker_symbol)
 return stock.ticker_fundament()


def get_fundamental_data_tool():
    """
    Creates a StructuredTool for retrieving fundamental data for a stock.
    
    Returns:
        StructuredTool: A tool for fundamental stock information.
    """
    description = (
        "Useful for when you need fundamental data information about a ticker XXX. "
        "Useful if somebody asks 'I need fundamental information for ticker XXX' "
        "Useful if somebody asks 'Give me an overview of the financial situation for companyXXX' "
    )

    return StructuredTool.from_function(
        func=get_fundamental_data, name="fv_get_fundamental_data", description=description
    )




# fundamental_data = get_fundamental_data('MSFT')

# print(fundamental_data)