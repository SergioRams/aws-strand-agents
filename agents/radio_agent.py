from strands import Agent, tool
from strands_tools import editor, file_read, file_write, speak

RADIO_SYSTEM_PROMPT = """
You are a radio station host, your capabilities include:

NEWS REPORT FILE READING:
    - Read news files, usually under the folder: output/ as report_<topic>.txt.

AUDIO GENERATION:
    - Create audio file(s).
    - Multiple languages supported.

INSTRUCTIONS:
    - You will be given a path to a news report file(s) to read.
    - You will generate audio files with a radio station style and theme.
    - Read the scrip as it is given to you, do not alter it unless told to do so..
    - Default language is english, if no other language is specified.
        - if more languages are specified use a 2 letter acronym as prefix.
    - Use the most natural sounding voices.

DELIVERABLE:
    Create a file(s) and output it to output/audio-{topic} replace {topic} with the given filename.
    Example:
       filepath = 'report-avocados-from-peru.txt', then output/en-audio-avocados-from-peru.txt

OUTPUT:
    Return the path to the audio file.
    Example:
        The report has been generated successfully at output/en-audio-avocados-from-peru.mp3
"""


@tool
def audio_assistant(filepath: str) -> str:
    """
    Generates audio only to queries using a specialized text-tos-speech capability.

    Args:
        filepath: a file path to a news article summary.

    Returns:
        Filepath to a generated audio file.
    """
    # Format the query for the news-agent with clear instructions
    formatted_query = (
        f"Help me create an audio file for the following news file: {filepath}"
    )

    try:
        print("Routed to audio generation assistant")
        audio_agent = Agent(
            system_prompt=RADIO_SYSTEM_PROMPT,
            tools=[speak, file_read, file_write, editor],
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
