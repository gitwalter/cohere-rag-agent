from langchain.agents import load_tools
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults

def get_openweathermap_tool():
    return load_tools(["openweathermap-api"])[0]


def get_internet_search_tool():
    internet_search = TavilySearchResults(max_results=4)
    internet_search.name = "internet_search"
    internet_search.description = "Route a user query to the internet, Useful when you need actual information"
    return internet_search


def get_wikipedia_tool():
    api_wrapper = WikipediaAPIWrapper(top_k_results=1)

    class WikiInputs(BaseModel):
        """Inputs to the wikipedia tool."""

        query: str = Field(
            description="query to look up in Wikipedia"
        )
        
    return WikipediaQueryRun(
        name="wikipedia-tool",
        description="look up things in wikipedia",
        args_schema=WikiInputs,
        api_wrapper=api_wrapper,
        return_direct=True,
    )



