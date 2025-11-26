from strands import Agent, tool
from strands_tools import file_read, file_write, use_aws
from strands_tools.tavily import tavily_search

NEWS_AGENT_SYSTEM_PROMPT = """
You are a news collecting assistant, your capabilities include:

HELPFUL TOOLS:
    - Search: Collecting up to date news about a given topic by searching the web.
    - File Read: Capability to read files.
    - File Write: Capability to write files.

INSTRUCTIONS:
    - You will be provided with a topic name.
    - Unless specified otherwise, news should be no more than 3 months old.
    - You will collect at least 1 news and maximum 5 if possible (default to basic mode search).
    - if no news are found, write a file about nothing being available for the given topic and search date.

DELIVERABLE:
    Create a file and write it to /temp/news-<topic> replace <topic> with the given topic name.
    Example:
       topic = 'avocados from Mexico', then /temp/news-avocados-from-mexico.txt

    The file should contain the following structure per news found:
    - News title.
    - Source name.
    - Link.
    - News date.
    - News content.
    - Highlight summary of a couple of sentences.

    If there is nothing available, write an summary file about nothing being available for the topic at the moment.

OUTPUT:
    Return the path to the news research file.
    Example:
        The news research file has been generated successfully at /temp/news-avocados-from-mexico.txt
"""


@tool
def news_assistant(query: str) -> str:
    """
    Process and respond to news-related queries using a specialized news searching agent.

    Args:
        query: A topic to be searched using the web for up-to-date news articles.

    Returns:
        A detailed report of the news found, content and sources.
    """
    # Format the query for the news-agent with clear instructions
    formatted_query = f"Help gather news about this topic: {query}"

    try:
        print("Routed to News collecting assistant")
        news_agent = Agent(
            system_prompt=NEWS_AGENT_SYSTEM_PROMPT,
            tools=[tavily_search, file_read, file_write, use_aws],
        )
        agent_response = news_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response

        return (
            "I apologize, but I couldn't find news articles for new. "
            "Please check if your query is clearly stated or try rephrasing it."
        )
    except Exception as e:
        # Return the specific error message for news processing
        return f"Error processing your news collection request: {str(e)}"
