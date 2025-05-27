from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from research_tools import fetch_wikipedia_summary
import os
from dotenv import load_dotenv


load_dotenv()


def create_search_agent():
    # LLM model
    llm = ChatGroq(
        temperature=0.7,
        model_name="llama3-70b-8192",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    # DuckDuckGo + Wikipedia tools
    tools = [
        Tool(
            name="Wikipedia",
            func=fetch_wikipedia_summary,
            description="Fetches summary of a topic from Wikipedia"
        ),
        Tool(
            name="DuckDuckGo",
            func=DuckDuckGoSearchRun().run,
            description="Performs real-time web search"
        )
    ]

    # Specifying langchain agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        handle_parsing_errors=True,
        verbose=True
    )
    return agent
