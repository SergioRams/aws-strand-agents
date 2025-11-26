import os

from dotenv import load_dotenv
from strands import Agent
from strands_tools import current_time, editor, file_read, file_write, use_aws

from custom_tools import s3_file_upload
from news_agent import news_assistant
from radio_agent import audio_assistant

# Load a TAVILY_API_KEY to get this agent up and running: https://app.tavily.com/home
load_dotenv()
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
BYPASS_TOOL_CONSENT = os.getenv("BYPASS_TOOL_CONSENT", "True")


DIRECTOR_SYSTEM_PROMPT = f"""
You are Director for a news publishing agency, orchestrating the process of the 'breaking news' generation project.

HELPFUL ASSISTANTS & TOOLS:
    - News Agent: Collects up to date news about a given topic.
    - Audio Agent: Generates audio clips from news articles.
    - Current Time: Provides the current time.
    - AWS S3 Uploads: Uploads files to S3 Bucket, preferred for uploading audio files.
    - Use AWS: for general AWS operations.

GENERAL PROCESS:
    - Topic identification: Identify the topic given by the client's input.
    - News Collection: Collect up to date news about the topic
    - Report Generation: Generate a script to summarize and synthesizes teh content from the news collections process.
        - Act as en editor for a radio station.
        - Include highlights from the news articles.
        - Important! script must cite sources naturally, such as 'according to...', 'as reported by...', and so on.
        - Keep and engaging tome.
        - if not specified, audio time should be around 20 seconds to 90 seconds worth of reading.
    - Audio Generation: Generate audio clips from the script.
    - Files can be stored locally to /temp folder.

KEY RESPONSIBILITIES:
    - Orchestrate the process of collecting, synthesizing news articles and generating audio clips.
    - Ensure that the process is accurate and efficient.
    - You are working from AWS Lambda, so common location is /temp directory.

DELIVERABLES:
Make sure you the following files are store in S3 Bucket {S3_BUCKET} under the 'output/' prefix:
    1. news-<topic>.txt (raw news collection)
    2. report-<topic>.txt (script with news synthesis for audio generation)
"""

# Orchestrator agent
director_agent = Agent(
    system_prompt=DIRECTOR_SYSTEM_PROMPT,
    callback_handler=None,
    tools=[
        news_assistant,
        audio_assistant,
        editor,
        file_read,
        file_write,
        s3_file_upload,
        use_aws,
        current_time,
    ],
)
