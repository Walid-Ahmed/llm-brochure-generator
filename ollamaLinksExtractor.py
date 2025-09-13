# Load environment variables from a .env file
from dotenv import load_dotenv
# OpenAI client
from openai import OpenAI
# For accessing environment variables
import os
# Your custom Website class for scraping links
from website import Website
# For working with JSON objects
import json
import ollama



class OllamaLinksExtractor:
    def __init__(self):
        # Define which OpenAI model to use
        self.MODEL = "llama3.2"


    def link_system_prompt(self, website):
        """
        Build the system prompt that tells the model how to behave.
        Here, we include **one JSON example** of the expected output format.
        → This makes it **one-shot prompting** (one demonstration is given).
        """
        link_system_prompt = (
            "You are provided with a list of links found on a webpage. "
            "You are able to decide which of the links would be most relevant to include in a brochure about the company, "
            "such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
        )
        link_system_prompt += "You should respond in JSON as in this example:"  # One-shot example starts here
        link_system_prompt += """
        {
            "links": [
                {"type": "about page", "url": "https://full.url/goes/here/about"},
                {"type": "careers page", "url": "https://another.full.url/careers"}
            ]
        }
        """
        return link_system_prompt

    def get_links_user_prompt(self, website):
        """
        Build the user prompt, which contains the actual scraped links.
        The model is asked to filter these links and return only the relevant ones.
        """
        user_prompt = f"Here is the list of links on the website of {website.url} - "
        user_prompt += (
            "please decide which of these are relevant web links for a brochure about the company, "
            "respond with the full https URL in JSON format. "
            "Do not include Terms of Service, Privacy, email links.\n"
        )
        user_prompt += "Links (some might be relative links):\n"
        user_prompt += "\n".join(website.links)  # Join all links into one string
        return user_prompt

    def get_links(self, url):
        """
        Main method: fetch the links from a webpage using the Website class,
        send them to the OpenAI API, and parse the model’s JSON response.
        """
        # Scrape the given URL for links using your Website class
        website = Website(url)

        response = ollama.chat(model=self.MODEL, messages=[
                {"role": "system", "content": self.link_system_prompt(website)},  # ✅ one-shot example included
                {"role": "user", "content": self.get_links_user_prompt(website)}
            ],format="json")
        result= response['message']['content']





        # Parse the JSON string into a Python dict
        return json.loads(result)


if __name__ == "__main__":
    # Instantiate the class
    ollamaLinksExtractor = OllamaLinksExtractor()
    # Run link extraction on Hugging Face’s homepage
    response = ollamaLinksExtractor.get_links("https://huggingface.co")
    # Print the JSON result
    print(response)
