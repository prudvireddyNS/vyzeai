from vyze.tools.raw_functions import *
from pydantic import BaseModel, Field, EmailStr, AnyUrl, FilePath, constr, conint, StringConstraints
from enum import Enum
from vyze.tools.base_tool import Tool, add_function
from typing import List, Optional, Annotated

@add_function(extract_relevant_sections_from_website)
class ExtractRelevantSectionsFromWebsite(BaseModel):
    """This tool helps to extract specific sections from a website based on the given keywords."""
    url : AnyUrl = Field(description="URL of a website")
    keywords : List[str] = Field(description="A list of keywords(single word) used to find relevant content about a topic from a website. More keywords gives best result. ")

@add_function(post_on_twitter)
class PostOnTwitter(BaseModel):
    """This tool helps to post a tweet on a specifit twitter account given their credentials."""
    tweet : str = Field(description="Twitter tweet content")
    consumer_key : str = Field(description="consumer_key - one of the four credentials")
    consumer_secret : str = Field(description="consumer_secret - one of the four credentials")
    access_token : str = Field(description="access_token - one of the four credentials")
    access_token_secret : str = Field(description="access_token_secret - one of the four credentials")

@add_function(post_on_linkedin)
class PostOnLinkedIn(BaseModel):
    """This tool helps to post on specific LinkedIn account given his/her LinkedIn access token"""
    token : str = Field(description="LinkedIn access token")
    text_content : str = Field(description="Linekin post content")
    image_path : Optional[FilePath] = Field(default=None, description="Image path for the post")

@add_function(send_email)
class SendEmail(BaseModel):
    """This tool helps to send an email."""
    to_email : EmailStr = Field(description="receiver email address")
    subject : str = Field(description="email subject")
    body : str = Field(description="email content")
    credentials_json_file_path: Optional[FilePath] = Field(
        default='credentials.json', description="The file path to the JSON file containing the sender's email credentials."
    )
    token_json_file_path: Optional[FilePath] = Field(
        default='token.json', description="The file path to the JSON file containing the OAuth token for authentication."
    )

@add_function(upload_to_drive)
class UploadToDrive(BaseModel):
    """This tool helps upload a file to Google Drive."""
    filepath: FilePath = Field(description="The path to the file to be uploaded.")
    filename: str = Field(description="The desired name for the file in Google Drive.")
    parent_folder_id: str = Field(description="The ID of the parent folder in Google Drive where the file will be uploaded.")
    service_account_file_path: Optional[FilePath] = Field(default='service_account.json', description="The path to the service account JSON file for authentication.")

@add_function(convert_md_to_docx)
class ConvertMDToDocx(BaseModel):
    """Model for converting a Markdown file to a DOCX file."""
    md_file_path: FilePath = Field(description="The path to the Markdown file to be converted.")
    docx_file_path: FilePath = Field(description="The path where the converted DOCX file will be saved.")

class ModelName(Enum):
    """Enum for the available OpenAI models."""
    DALL_E_2 = "dall-e-2"
    DALL_E_3 = "dall-e-3"

class Quality(Enum):
    """Enum for the available image qualities."""
    STANDARD = "standard"
    HD = "hd"

@add_function(generate_image_openai)
class GenerateImageOpenAI(BaseModel):
    """Model for generating an image using OpenAI's image generation API."""
    text: str = Field(description="The text prompt for generating the image.")
    openai_api_key : Optional[str] = Field(description="The OpenAI API key for authentication.")
    model_name: Optional[ModelName] = Field(default=ModelName.DALL_E_2, description="The name of the OpenAI image generation model.")
    resolution: Optional[Annotated[str, StringConstraints(pattern=r'^\d+x\d+$')]] = Field(default="512x512", description="The resolution of the generated image, e.g., '512x512'.")
    quality: Optional[Quality] = Field(default=Quality.STANDARD, description="The quality of the generated image.")
    same_temp: Optional[bool] = Field(default=False, description="Whether to use a temporary file for the output image. Usually do not prefer saving temporary.")

# class GenerateImageOpenAIModel(BaseModel):
#     """Model for generating an image using OpenAI's image generation API."""
#     text: str = Field(description="The text prompt for generating the image.")
#     same_temp: Optional[bool] = Field(default=False, description="Whether to use a temporary file for the output image.")
#     model_name: Optional[str] = Field(default="dall-e-2", description="The name of the OpenAI image generation model.")
#     resolution: Optional[constr(regex=r'^\d+x\d+$')] = Field(default="512x512", description="The resolution of the generated image, e.g., '512x512'.")
#     quality: Optional[str] = Field(default='standard', description="The quality of the generated image.")
#     n: Optional[conint(ge=1)] = Field(default=1, description="The number of images to generate.")

@add_function(generate_images_and_add_to_blog)
class AddImagesToBlog(BaseModel):
    """This tool helps to add images to a blog. Blog should contain image generation prompts enclosed XML tag (<image>).
    Returns blog content and a doc file containing blog. """
    blog_content : str = Field(description="content of a blog")
    save_temp : Optional[bool] = Field(False, description="if True, files and images are stored temporarily. (not recommended). ")

@add_function(generate_video)
class GenerateVideo(BaseModel):
    """Given image promt pairs and narration pairs, this tool helps to generate a video.
    Images are generated using image prompts and speech is generated using narration prompts."""
    pairs: str = Field(description="A string of narration and image prompt pairs enclosed in <narration> and <image> tags.")
    final_video_filename : Optional[str] = Field('video.mp4', description="final video file name used to save the video.")

@add_function(extract_audio_from_video)
class ExtractAudioFromVideo(BaseModel):
    """This tool is used for extracting audio from a video."""
    video_path: FilePath = FilePath(description="The path to the video file from which to extract audio.")

@add_function(transcribe_audio)
class TranscribeAudio(BaseModel):
    """This tool is used for transcribing audio using openai whisper."""
    audio_file_path: FilePath = FilePath(description="The path to the audio file for transcription.")

@add_function(youtube_transcript_loader)
class YouTubeTranscriptLoader(BaseModel):
    """This tool helps to load transcript of a YouTube video."""
    url : AnyUrl = Field(description="YouTube video url.")

@add_function(search_multiple_wikipedia_pages)
class WikipediaSearch(BaseModel):
    """Search multiple Wikipedia pages based on a query and return summaries or full content."""
    query: str = Field(..., description="Search term for querying Wikipedia.")
    lang: str = Field("en", description="Language of Wikipedia to query, default is 'en' for English.")
    result_count: int = Field(3, description="Number of search results to return, default is 3.")
    full_content: bool = Field(False, description="Whether to return full page content or just summary, default is summary.")

@add_function(calculate)
class Calculate(BaseModel):
    """This tool is used to evaluate a mathematical expression."""
    operation: str = Field(..., description="Mathematical expression to evaluate (no symbols or text allowed).")