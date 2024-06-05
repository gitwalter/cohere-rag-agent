import streamlit as st
import os
import markdown
import warnings
from langchain_cohere.llms import Cohere
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_cohere import ChatCohere, create_cohere_react_agent
from langchain_community.agent_toolkits.polygon.toolkit import PolygonToolkit
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain.agents import AgentExecutor
from cohere_tools import get_internet_search_tool
from yfinance_tools import get_business_summary_tool, get_ticker_history_tool, get_ticker_info_tool

# Function to get API keys from Streamlit secrets
def get_keys():
    warnings.filterwarnings("ignore")
    os.environ["ALPHAVANTAGE_API_KEY"] = st.secrets["ALPHAVANTAGE_API_KEY"]
    os.environ["COHERE_API_KEY"] = st.secrets["COHERE_API_KEY"]
    os.environ["OPENWEATHERMAP_API_KEY"] = st.secrets["OPEN_WEATHER_API_KEY"]
    os.environ["POLYGON_API_KEY"] = st.secrets["POLYGON_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

# Function to get tools from Polygon API
def get_polygon_tools():
    polygon = PolygonAPIWrapper()
    toolkit = PolygonToolkit.from_polygon_api_wrapper(polygon)
    return toolkit.get_tools()

# Function to get tools from Yahoo Finance API
def get_yfinance_tools():
    return [get_business_summary_tool(), get_ticker_history_tool(), get_ticker_info_tool()]

def invoke_cohere_with_tools(input, tools, prompt_template="{input}"):
    llm = ChatCohere()
    prompt = ChatPromptTemplate.from_template(prompt_template)
    agent = create_cohere_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    response = agent_executor.invoke(input)    
    return response

# Initialize the Streamlit app
def main():
    st.title("Investment Advisor Analysis")
    
    # Get API keys
    get_keys()
    
    # User inputs
    ticker = st.text_input("Enter the ticker symbol:", "NVDA")
    period = st.text_input("Enter the period (e.g., '1y'):", "1y")
    topics = st.text_area("Enter the topics:", "all relevant key figures like margin, profit, earnings growth and so on, fundamental indicators, technical indicators and analyst recommendations")
    
    # Prompt templates
    prompt_start = """0. I want you to act as an investment advisor.
                         Your advise is always reflected and based on science and proven economic and investment theories.
                         Think step-by-step and use the right tools and check your results against this instruction.
                         Before analyzing make an internet search about 1. the current macroeconomic situation,
                         2. the detailed actual performance of the big indices, 3. the detailed actual performance of the different sectors,
                         4. the value of the fear and greed index for today and 5. the sentiment
                         at the stock market exchanges by doing a profound internet research.
                         Use therefore the tools of your choice.
                         Use always the right tools to answer each question.
                         After answering each question, make a final analysis as described in step 7.
                         Display the final investment rating first and then the detailed analysis from the steps 0 to 6 
                         with the following headers:
                         
                         - overall political, macroeconomic and market situation
                           - political
                           - macoreconomic
                           - markets
                           - fear and greed index
                           
                         - company summary
                           - description
                           - headquater
                           - board
                           - market cap
                           - sector
                           - industry
                           
                         - fundamental analysis
                           - P/E ratio
                           - earnings
                           - margins
                           - cashflow
                           - debts
                           - sales growth
                           - earnings growth
                           - revenue growth
                           - revenue
                           
                         - technical analysis 
                           - 52 week high/low
                           - 200 day MA
                           - 100 day MA
                           - 50 day MA
                           - overbought/oversold
                           - beta
                           - performance 1 week
                           - performance 1 month
                           - performance 3 month
                           - performance 6 month
                           - performance 1 year
                           
                         - sentiment analysis
                           - news
                           - analysts
                           - web research

                    Write everything in HTML markup for a good display in a chatbot.
                   """
    
    prompt_template_summary = """ 1. Get a summary for {ticker}. If summary could not be loaded by  the summary tool,
                                     search in the internet for a summary about {ticker}."""
    
    prompt_template_ticker_info = """ 2. I need detailed information about {ticker}. Produce a bullet point key value list for all for your analysis important {topics} using CRLF before each point.
                                     After that analyze the fundamental and technical data and rate the company. Is it a good buy? Is it oversold or overbought? Is it a stable investment
                                     with a good sharpe ratio? Is it risky or safe to hold stocks of {ticker}? Display your detailed analysis at the end."""
    
    prompt_template_av_financials = """ 3. How are the financials for {ticker}? What is its market value?
                                        Produce an overview in form of a bullet point list and use CRLF for new lines
                                        and rate the financial situation of the company and display it. """
    
    prompt_template_av_sentiment = " 4. What is the news sentiment for {ticker}? Rate the sentiment based on the news and explain your rating and display it. "
    
    prompt_template_history = " 5. How did {ticker} perform the last {period}? Get the timeseries in a dataframe and calculate and rate the performance and display it. "
    
    prompt_template_search = """ 6. Search news and articles in the internet what you find about {ticker} and judge the sentiment. """
    
    prompt_template_rating = """ 7. Based on all relevant information about fundamental, technical and sentiment data 
                                determined in the steps before for {ticker}
                                and the overall macroeconomic situation and sentiment at the stock market exchange
                                produce now a profound and detailed investment and trading advice based on a factor analysis and your own ratings in your report.
                                The rating should have an explicit header and explain why the stock is a buy or not.
                                Make an educated advice for a trader about a reasonable profit-target above the stock price, a reasonable stop-loss under the stock price
                                and a reasonable position size all in currency USD if the stock is a buy.                            
                             """
    
    # Prompt template checkboxes
    prompt_templates = {
        "prompt_start": prompt_start,
        "prompt_template_summary": prompt_template_summary,
        "prompt_template_ticker_info": prompt_template_ticker_info,
        "prompt_template_av_financials": prompt_template_av_financials,
        "prompt_template_av_sentiment": prompt_template_av_sentiment,
        "prompt_template_history": prompt_template_history,
        "prompt_template_search": prompt_template_search,
        "prompt_template_rating": prompt_template_rating
    }
    
    selected_templates = []
    for key, value in prompt_templates.items():
        if st.checkbox(f"Include {key}", value=True):
            selected_templates.append(value)
    
    # Combine selected templates into a single prompt
    prompt_template_combined = "".join(selected_templates)
    
    # Get tools
    combined_tools = []
    filtered_polygon_tools = [tool for tool in get_polygon_tools() if tool.name in ("polygon_financials", "polygon_ticker_news")]
    combined_tools.extend(filtered_polygon_tools)
    combined_tools.extend(get_yfinance_tools())
    combined_tools.append(get_internet_search_tool())
    
    # Prepare input
    input = {"ticker": ticker, "topics": topics, "period": period}
    
    # Execute analysis
    if st.button("Run Analysis"):
        response = invoke_cohere_with_tools(input=input, tools=combined_tools, prompt_template=prompt_template_combined)
        st.write(response)

if __name__ == "__main__":
    main()
