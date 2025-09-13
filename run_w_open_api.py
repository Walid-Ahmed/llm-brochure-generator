
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
from openAILinksExtractor import OpenAILinksExtractor

def get_all_details(url,helper):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = helper.get_links(url)
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result


system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

# Or uncomment the lines below for a more humorous brochure - this demonstrates how easy it is to incorporate 'tone':

# system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
# and creates a short humorous, entertaining, jokey brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
# Include details of company culture, customers and careers/jobs if you have the information."


def get_brochure_user_prompt(company_name, url,helper):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url,helper)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt


def create_brochure(company_name,url,helper):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url,helper)}
          ],
    )
    brochure_text = response.choices[0].message.content
    return brochure_text


if __name__ == "__main__":

    MODEL = 'gpt-4o-mini'

    # Load environment variables (like OPENAI_API_KEY) from .env file
    load_dotenv(override=True)
    api_key = os.getenv('OPENAI_API_KEY')


    # Initialize OpenAI client
    openai = OpenAI()
    helper = OpenAILinksExtractor()
    company,url="Diamond Fruits ", "https://diamondfruits.com/"
    brochure_text=create_brochure(company,url,helper)

    # Print brochure to console
    print("\n=== Generated Company Brochure ===\n")
    print(brochure_text)

    # Save brochure to Markdown file
    filename = f"{company.strip().replace(' ', '_')}_brochure.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(brochure_text)

    print(f"\n✅ Brochure saved to {filename}")