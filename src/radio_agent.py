import os

from dotenv import load_dotenv
from strands import Agent, tool
from strands_tools import file_read, file_write, speak, use_aws

from custom_tools import s3_file_upload

load_dotenv()
S3_BUCKET = os.getenv("S3_BUCKET")


RADIO_SYSTEM_PROMPT = f"""
You are a radio station host, bringing news from the 'Serverless Radio Station', your capabilities include:

HELPFUL TOOLS:
    - File Read: Capability to read files.
    - File Write: Capability to write files.
    - Create audio file(s) .mp3 from Amazon Polly.
    - AWS S3 Uploads: Uploads files to S3 Bucket, preferred for uploading audio files.
    - Use AWS: for general AWS operations.

INSTRUCTIONS:
    - You will be given a path to a script file(s) to generate audio for.
    - You will generate audio files with a radio station informative style and theme.
    - Read the scrip as it is given to you, but add the introduction from the 'Serverless Radio Station'.
    - Default language is english if no other language is specified.
    - Use the most natural sounding voices for the language.
    - Use 2 letter acronym as prefix for the generated file to indicate the language used.
        Example: English = en, Spanish = es, Portuguese = pt.

DELIVERABLE:
    Create a file and upload it to S3 as follows:

    Upload the file to S3 as: {S3_BUCKET}/output/<language>-audio-<topic>.mp3

    Example:
       input script name = 'report-avocados-from-peru.txt'
       S3 upload = '{S3_BUCKET}/output/en-audio-avocados-from-peru.mp3'

OUTPUT:
    Return the path to the audio file.
    Example:
        The report has been generated successfully at '{S3_BUCKET}/output/en-audio-avocados-from-peru.mp3'
"""


@tool
def audio_assistant(filepath: str) -> str:
    """
    Generates audio only to queries using a specialized text-to-speech capability.

    Args:
        filepath: a file path to the report to generate audio for.

    Returns:
        Filepath to a generated audio file.
    """
    # Format the query for the news-agent with clear instructions
    formatted_query = (
        f"Help me create an audio file for the following report file: {filepath}"
    )

    try:
        print("Routed to audio generation assistant")
        audio_agent = Agent(
            system_prompt=RADIO_SYSTEM_PROMPT,
            tools=[speak, file_read, file_write, s3_file_upload, use_aws],
        )
        agent_response = audio_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response

        return (
            "I apologize, but I couldn't find the specified file. "
            "Please check if your query is clearly stated or try rephrasing it."
        )
    except Exception as e:
        # Return the specific error message for news processing
        return f"Error processing your audio generation request: {str(e)}"
