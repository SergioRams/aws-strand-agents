import ffmpeg
from pydub import AudioSegment
from strands import tool


@tool()
def combine_voice_with_background_music(
    main_track_path, bg_music_path, output_path, bg_volume_reduction: int = 20
) -> str:
    """
    Combines a main voice track with background music, ideal for adding background music to an audio clip.

    Args:
        main_track_path (str): Path to the main audio voice file.
        bg_music_path (str): Path to the background music file.
        output_path (str): Path to save the combined audio file.
        bg_volume_reduction (int): Decibels to reduce the background music volume. (20 seems like the sweet spot)

    Returns:
        str: A message indicating the outcome of the upload (success or failure details).
    """
    try:
        main_audio = AudioSegment.from_file(main_track_path)
        background_music = AudioSegment.from_file(bg_music_path)

        # Ensure background music matches main audio length
        if len(background_music) < len(main_audio):
            repeats = int(len(main_audio) / len(background_music)) + 1
            background_music = background_music * repeats
            background_music = background_music[: len(main_audio)]
        else:
            background_music = background_music[: len(main_audio)]

        # Adjust background music volume
        background_music = background_music - bg_volume_reduction

        # Overlay the background music
        combined_audio = main_audio.overlay(background_music)

        combined_audio.export(output_path, format="mp3")
        return f"Successfully combined audio and saved to {output_path}"

    except Exception as e:
        return f"An error occurred: {e}"


@tool()
def combine_video_audio(video_file: str, audio_file: str, output_file: str) -> str:
    """
    Merges a video file and a longer audio file, looping the video to match the audio duration.

    Args:
        video_file (str): Path to the video file to be looped.
        audio_file (str): Path to the audio file to be used as the track.
        output_file (str): Path to save the resulting merged video file.

    Returns:
        str: A message indicating the outcome of the operation (success or failure details).
    """
    try:
        # Input for the video, specifying infinite loop (-1) before the input file
        input_video = ffmpeg.input(video_file, stream_loop=-1)
        input_audio = ffmpeg.input(audio_file)

        # Combine streams
        ffmpeg.output(
            input_video["v:0"],
            input_audio["a:0"],
            output_file,
            c="copy",
            shortest=None,  # Use the flag to signify the shortest stream should govern duration
        ).run(overwrite_output=True, quiet=True)

        return f"Successfully merged video and audio to {output_file}"

    except Exception as e:
        return f"An error occurred during video/audio combination: {e}"
