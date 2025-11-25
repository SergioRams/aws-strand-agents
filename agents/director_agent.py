from news_agent import news_assistant
from radio_agent import audio_assistant
from strands import Agent
from strands_tools import editor, file_read, file_write

DIRECTOR_SYSTEM_PROMPT = """
You are Director for a news publishing agency, orchestrating the process of the 'breaking news' generation project.

HELPFUL ASSISTANTS:
    - News Agent: Collects up to date news about a given topic.
    - Audio Agent: Generates audio clips from news articles.

GENERAL PROCESS:
    - Topic(s) identification: Identify the topic(s) given by the client's input.
    - News Collection: Collect up to date news about the topic(s)
    - Report Generation: Generate a script to summarize and synthesizes teh content from the news collections process.
        - Act as en editor for a radio station.
        - Include highlights from the news articles.
        - Important! script must cite sources naturally, such as 'according to...', 'as reported by...', and so on.
        - Keep and engaging tome.
        - if not specified, audio time should be around 20 seconds to 90 seconds worth of reading.
    - Audio Generation: Generate audio clips from the report.

KEY RESPONSIBILITIES:
    - Orchestrate the process of collecting, synthesizing news articles and generating audio clips.
    - Ensure that the process is accurate and efficient.

DELIVERABLES:
under the output/ folder:
    - news-{topic}.txt (raw news collection)
    - report-{topic}.txt (news synthesis for audio generation)
    - {language}-audio-{topic}.mp3
"""

# Create a file-focused agent with selected tools
director_agent = Agent(
    system_prompt=DIRECTOR_SYSTEM_PROMPT,
    callback_handler=None,
    tools=[news_assistant, audio_assistant, editor, file_read, file_write],
)

response = director_agent(
    """
    There is already a report output/report-mexican-blueberry.txt, generate an audio file for it in spanish only.
    """
)

print(response)
