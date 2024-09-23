from vyze.models.openai import ChatOpenAI
from vyze.tools.prebuilt_tools import ExtractRelevantSectionsFromWebsite, AddImagesToBlog, GenerateVideo, YouTubeTranscriptLoader, ExtractAudioFromVideo, TranscribeAudio
from vyze.tools.base_tool import Tool



class BlogAgent:
    def __init__(self) -> None:
        self.llm1 = ChatOpenAI()
        self.tools = Tool([ExtractRelevantSectionsFromWebsite, AddImagesToBlog])()
        self.llm = ChatOpenAI(tools=self.tools)

    def research(self, topic, url):
        
        prompt1 = (
            f"Gather relavent information about topic from the website. "
            f"\nTopic: {topic} "
            f"\nWebsite: {url} "
        )
        context = self.llm.run(prompt1, system_message="You are a senior research agent.")
        return context

    def write_blog_text(self, topic, url, context):
        prompt2 = (
            f"Write a comprehensive blog post based on the following details:\n\n"
            f"Topic: {topic}\n"
            f"Company's website: {url}\n"
            f"Summarized content from company's website: {context}\n\n"
            f"The blog should include an engaging introduction to topic, then detailed stections about how the company addresses the topic, "
            f"and a conclusion summarizing the key points. Structure the blog with clear headings, and write it in a conversational style."
            f"Use '<-IMAGE->' placeholders: one after the introduction and another at a point where it would enhance the narrative.(total 2 images)"
            f"Output the blog in markdown format, including a title, introduction, body sections, and conclusion. Write in a conversational style to engage readers. "
        )
        blog_text = self.llm1.run(prompt2, system_message="You are an effective Blog writer.")
        return blog_text

    def add_image_prompts(self,blog_content):
        prompt3 = (
            "Please replace all instances of '<-IMAGE->' with specific image prompts. "
            "Each image prompt should be enclosed within XML tag ('<image>'). "
            "Ensure that the image prompts avoid including any text, names of individuals, company names, logos, or other identifiable information. "
            "Think of the image prompt as 'what you want to see in the final image.' "
            "Provide a descriptive prompt that clearly defines the elements, colors, and subjects. "
            "For instance: 'The sky was a crisp (blue:0.3) and (green:0.8)' indicates a sky that is predominantly green with a hint of blue. "
            "The weights (e.g., 0.3 and 0.8) apply to all words in the prompt, guiding the emphasis of the colors and elements. "
            "While you may reduce the number of images, ensure that no two image prompts are identical."
            f"Blog: \n{blog_content}\n\n"
            "Expected Output: A complete blog with image prompts enclosed in <image> tags."
        )
        blog = self.llm1.run(prompt3)
        return blog
    
    def add_images(self, blog_content):
        prompt4 = f"Use tool to generate images and add them to below blog. \n\n Blog: {blog_content}"
        final_blog = self.llm.run(prompt4)
        return final_blog
    
    def generate_blog(self, topic, url):
        research_content = self.research(topic, url)
        blog_text = self.write_blog_text(topic, url, research_content)
        blog_content = self.add_image_prompts(blog_text)
        # print(blog_content)
        output = self.add_images(blog_content)

        return output
    
class VideoAgent:
    def __init__(self) -> None:
        self.llm1 = ChatOpenAI()
        self.tools = Tool([ExtractRelevantSectionsFromWebsite, GenerateVideo])()
        self.llm = ChatOpenAI(tools=self.tools)

    def research(self, topic, url):
        
        prompt1 = (
            f"Gather relavent information about topic from the website. "
            f"\nTopic: {topic} "
            f"\nWebsite: {url} "
        )
        context = self.llm.run(prompt1, system_message="You are a senior research agent.")
        return context
    
    def generate_script(self, topic, context):
        prompt2 = (
            "Generate a video script with two narration and image prompt pairs for the following topic, focusing on the company's expertise related to the topic. "
            "The script should contain around 200 words total. Start by explaining the topic and then highlight the company's role or expertise in relation to it. "
            "The Narration must start with topic name. "
            "Ensure that the image prompts do not include any text, names, logos, or other identifying features. "
            "Provide a descriptive image prompt that clearly defines elements, colors, and subjects. For instance, 'The sky was a crisp blue with green hues' is more descriptive than just 'blue sky'."
            f"\n\n**Topic:** \n{topic}\n\n"
            f"**Company Website content:** \n{context}\n\n"
            "Expected Output: Two pairs of sentences. Enclose narration in <narration> narration here </narration> tags and image prompts in <image> image prompt here </image> tags."
        )
        script = self.llm1.run(prompt2)
        return script

    def create_video(self, script):
        prompt3 = f"Create a video for the follwing script. \n\n video script: {script}"
        video = self.llm.run(prompt3)
        return video
    
    def generate_video(self, topic, url):
        research_content = self.research(topic, url)
        # print(research_content)
        script = self.generate_script(topic, research_content)
        # print(script)
        video = self.create_video(script)
        return video

class YTBlogAgent:
    def __init__(self) -> None:
        self.llm1 = ChatOpenAI()
        self.tools = Tool([YouTubeTranscriptLoader, AddImagesToBlog])()
        self.llm = ChatOpenAI(tools=self.tools)

    def extract_transcript(self, url):
        prompt1 = f"Extract the text content from the youtube video. video url: {url}"
        context = self.llm.run(prompt1)
        return context

    def write_blog_text(self, url, context):
        prompt2 = (
            f"Given a youtube video content, write a comprehensive blog post. "
            f"Structure the blog with clear headings, and write it in a conversational style. "
            f"Use '<-IMAGE->' placeholders: one after the introduction and another at a point where it would enhance the narrative. "
            f"Output the blog in markdown format, including a title, introduction, body sections, and conclusion. Write in a conversational style to engage readers. "
            f"**\n\nYouTube video url: ** {url}"
            f"\n**YouTube video transcript: **{context}"
        )
        blog_text = self.llm1.run(prompt2, system_message="You are an effective Blog writer.")
        return blog_text

    def add_image_prompts(self,blog_content):
        prompt3 = (
            "Please replace all instances of '<-IMAGE->' with specific image prompts. "
            "Each image prompt should be enclosed within XML tag ('<image> promt here </image>'). "
            "Ensure that the image prompts avoid including any text, names of individuals, company names, logos, or other identifiable information. "
            "Think of the image prompt as 'what you want to see in the final image.' "
            "Provide a descriptive prompt that clearly defines the elements, colors, and subjects. "
            "For instance: 'The sky was a crisp (blue:0.3) and (green:0.8)' indicates a sky that is predominantly green with a hint of blue. "
            "The weights (e.g., 0.3 and 0.8) apply to all words in the prompt, guiding the emphasis of the colors and elements. "
            "While you may reduce the number of images, ensure that no two image prompts are identical."
            f"Blog: \n{blog_content}\n\n"
            "Expected Output: A complete blog with image prompts enclosed in <image> tags."
        )
        blog = self.llm1.run(prompt3)
        return blog
    
    def add_images(self, blog_content):
        prompt4 = f"Use tool to generate images and add them to below blog. \n\n Blog: {blog_content}"
        final_blog = self.llm.run(prompt4)
        return final_blog
    
    def generate_blog(self, url):
        transcript = self.extract_transcript(url)
        blog_text = self.write_blog_text(url, transcript)
        blog_content = self.add_image_prompts(blog_text)
        # print(blog_content)
        output = self.add_images(blog_content)
        return output
    
class VideoAudioBlogAgent:
    def __init__(self) -> None:
        self.llm1 = ChatOpenAI()
        self.tools = Tool([ExtractAudioFromVideo, TranscribeAudio, AddImagesToBlog])()
        self.llm = ChatOpenAI(tools=self.tools)
        self.video_formats = ["mp4", "avi", "mkv", "mov", "flv", "wmv", "webm", "mpeg", "mpg", "3gp", "m4v", "mxf", "vob", "ogv"]
        self.audio_formats = ["mp3", "wav", "aac", "flac", "ogg", "m4a"]


    def video_to_text(self, video_path):
        audio_path = self.llm.run(f"Extract audio fromt the video. video path: {video_path}")[0]
        text = self.llm.run(f"Transcribe the audio into text. audio_path: {audio_path}")[0]
        return text

    def audio_to_text(self, audio_path):
        text = self.llm.run(f"Transcribe the audio into text. audio_path: {audio_path}")[0]
        return text

    def write_blog_text(self, context):
        prompt2 = (
            f"Given transcription of a video, write a comprehensive blog post."
            f"The blog should include an engaging introduction to topic, then detailed stections about how the company addresses the topic, "
            f"and a conclusion summarizing the key points. Structure the blog with clear headings, and write it in a conversational style."
            f"Use '<-IMAGE->' placeholders: one after the introduction and another at a point where it would enhance the narrative.(total 2 images)"
            f"Output the blog in markdown format, including a title, introduction, body sections, and conclusion. Write in a conversational style to engage readers. "
            f"\n\nVideo Transcript: {context}"
        )
        blog_text = self.llm1.run(prompt2, system_message="You are an effective Blog writer.")
        return blog_text

    def add_image_prompts(self,blog_content):
        prompt3 = (
            "Please replace all instances of '<-IMAGE->' with specific image prompts. "
            "Each image prompt should be enclosed within XML tag ('<image>'). "
            "Ensure that the image prompts avoid including any text, names of individuals, company names, logos, or other identifiable information. "
            "Think of the image prompt as 'what you want to see in the final image.' "
            "Provide a descriptive prompt that clearly defines the elements, colors, and subjects. "
            "For instance: 'The sky was a crisp (blue:0.3) and (green:0.8)' indicates a sky that is predominantly green with a hint of blue. "
            "The weights (e.g., 0.3 and 0.8) apply to all words in the prompt, guiding the emphasis of the colors and elements. "
            "While you may reduce the number of images, ensure that no two image prompts are identical."
            f"Blog: \n{blog_content}\n\n"
            "Expected Output: A complete blog with image prompts enclosed in <image> tags."
        )
        blog = self.llm1.run(prompt3)
        return blog
    
    def add_images(self, blog_content):
        prompt4 = f"Use tool to generate images and add them to below blog. \n\n Blog: {blog_content}"
        final_blog = self.llm.run(prompt4)
        return final_blog
    
    def generate_blog(self, file_path):
        file_format = self._classify_file(file_path)
        if file_format == 'Video file':
            text = self.video_to_text(file_path)
        elif file_format == 'Audio file':
            text = self. audio_to_text(file_path)
        else:
            raise("Invalid file format.")
        blog_text = self.write_blog_text(text)
        blog_content = self.add_image_prompts(blog_text)
        output = self.add_images(blog_content)
        return output
    
    def _classify_file(self, file_path):
        video_extensions = ("mp4", "avi", "mkv", "mov", "flv", "wmv", "webm", "mpeg", "mpg", "3gp", "m4v", "mxf", "vob", "ogv")
        audio_extensions = ("mp3", "wav", "aac", "flac", "ogg", "m4a")
        
        if file_path.lower().endswith(video_extensions):
            return "Video file"
        elif file_path.lower().endswith(audio_extensions):
            return "Audio file"
        else:
            return "Unknown type"
