from phi.agent import Agent, RunResponse
from phi.model.google import Gemini
from phi.tools.googlesearch import GoogleSearch
import os
import json

# Set up Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDXVrAFGsuE3hp9_SIvnY0bmF0-RJoByHY"

# Image Decoder Agent
imageDecoderAgent = Agent(
    role="Analyse the given image",
    model=Gemini(id="gemini-1.5-flash"),
    system_prompt="""
        You are a highly capable AI agent specializing in analyzing social media posts. Your task is to:
        1. Identify and describe the content of an image (e.g., objects, scenes, or themes).
        2. Extract any text written on the image and present it verbatim.
        3. Provide a concise summary of what the post is likely about, integrating both visual and textual elements.
        4. Provide all the content in strict JSON format with keys as "Image Description", "Extracted Text", and "Post Summary".
    """,
    instructions="""
        Analyze the Image:
        1. Examine the content of the image thoroughly and describe objects, people, or activities.
        2. Check for text in the image:
            - Extract the text exactly as it appears.
            - If no text is present, state "No text found."
        3. Output results in JSON format:
            - Image Description: Detailed description of the image.
            - Extracted Text: Exact text from the image or "No text found."
            - Post Summary: Concise summary integrating visual and textual elements.
    """,
)

# Fact-Checking Agent
factCheckingAgent = Agent(
    model=Gemini(id="gemini-1.5-flash"),
    tools=[GoogleSearch()],
    role="Fact-Check the given news",
    description="You are a fact-checking agent that verifies news content by analyzing its relevance and accuracy based on web search results.",
    instructions=[
    "1. Extract key details from the news content (e.g., topic, events, entities).",
    "2. Search for at least 5 related news articles using key details in English.",
    "3. Compare the input news with fetched articles for matching details and consistency.",
    "4. If input matches a fetched article, classify it as TRUE. Otherwise, classify it as FALSE.",
    "5. If no relevant news is found, classify as FALSE and state the reason.",
    "6. Conclude the output strictly in JSON format with three keys: 'boolean_value' (boolean),Title (string) and 'summary' (string).",
    "7. If even one claim in the news is false, classify the entire news as FALSE."
],
    structured_outputs=True,
    show_tool_calls=True,
    debug_mode=True,
)

# Functions to use the agents

# 1. Decoding the image
def decode_image(image_url):
    response = imageDecoderAgent.run(image_url)
    return response

#testing
# response = decode_image("https://res.cloudinary.com/disl8qg3k/image/upload/v1736529208/mu8tci88fgh73uzfyuwj.png")
# print(response.content)

# # 2. Fact-checking the news
# def fact_check_news(news_content):
#     response = factCheckingAgent.run(news_content)
#     return response

# response2 = fact_check_news(response.content)
# print(response2)


