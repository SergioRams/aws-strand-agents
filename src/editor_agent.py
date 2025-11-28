import os

from dotenv import load_dotenv
from strands import Agent, tool
from strands_tools import file_read, file_write

from custom_tools import audio_video_manipulation, s3_file_operations

load_dotenv()
S3_BUCKET = os.getenv("S3_BUCKET")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


EDITOR_SYSTEM_PROMPT = f"""
You are a news station editor, working with audio (.mp3) and video (.mp4), your capabilities include:

HELPFUL TOOLS:
    - AWS S3 Uploads: Uploads files to S3 Bucket, preferred for uploading audio files.
    - Use AWS: Good to download files from S3 Bucket.

INSTRUCTIONS:
    1. You will be given paths to 2 files:
        - a script file script-<topic>.txt
        - an audio file <language>-raw-audio-<topic>.mp3
    2. Identify the tone of the script file: positive, neutral or negative.
    3. Get the corresponding audio file from S3 Bucket corresponding to the tone:
        - s3://{S3_BUCKET}/audio/<tone>-background-audio.mp3
    4. Add background music to the input raw-audio .mp3 file.
    5. Create a video clip from the resulting new .mp3 audio file.
        - the video you need is in s3://{S3_BUCKET}/video/reporter_video.mp4

DELIVERABLE:
    Create audio file locally and also upload them to S3 as follows:

    Local output = /temp/<language>-<tone>-video-<topic>.mp4
    Upload the file to S3 as: {S3_BUCKET}/output/<language>-<tone>-video-<topic>.mp4

    Example:
       input script name = 'script-avocados-from-mexico.txt'
       local output = '/temp/en-positive-video-avocados-from-mexico.mp4'
       S3 upload = '{S3_BUCKET}/output/en-positive-video-avocados-from-mexico.mp4'

OUTPUT:
    Return the path to the audio file.
    Example:
        The video file has been generated successfully to /temp/en-positive-video-avocados-from-mexico.mp4 and uploaded
         to S3 '{S3_BUCKET}/output/en-positive-video-avocados-from-mexico.mp4'.
"""


@tool
def editor_assistant(script_filepath: str, raw_audio_filepath) -> str:
    """
    Generates video from audio files by using a specialized video editing capability.

    Args:
        script_filepath: a file path to the .txt script to review tone for: positive, negative, neutral.
        raw_audio_filepath: a file path to the .mp3 raw audio file to generate .mp4 video for.

    Returns:
        Filepath to a generated video file.
    """
    # Format the query for the news-agent with clear instructions
    formatted_query = (
        f"Help me create an video file for the following script file: {script_filepath} and"
        f" raw audio clip {raw_audio_filepath}"
    )

    try:
        print("Routed to audio generation assistant")
        audio_agent = Agent(
            system_prompt=EDITOR_SYSTEM_PROMPT,
            tools=[
                file_read,
                file_write,
                s3_file_operations,
                audio_video_manipulation,
            ],
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
