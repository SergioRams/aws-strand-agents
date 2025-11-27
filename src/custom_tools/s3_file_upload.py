import boto3
from strands import tool


@tool()
def upload_file_to_s3(file_path: str, bucket_name: str, object_name: str) -> bool:
    """
    Uploads a local audio file to an Amazon S3 bucket.

    This function is recommended for most use cases as it automatically
    handles robust multipart uploads for large files.

    Args:
        file_path (str): The local path to the file to upload (e.g., '/temp/combined_audio.mp3').
        bucket_name (str): The name of the target S3 bucket (e.g., 'my-bucket').
        object_name (str, optional): The desired S3 object key/path (e.g., 'output/audio-track.mp3').

    Returns:
        bool: A boolean indicating the outcome of the upload (success or failure details).
    """
    s3_client = boto3.client("s3")

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(
            f"File '{file_path}' uploaded to '{bucket_name}/{object_name}' successfully."
        )
        return True
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
