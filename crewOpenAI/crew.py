from crewai import Crew,Process
from tasks import research_task,writer_task
from agents import news_researcher,news_writer
import time
import markdown
from bs4 import BeautifulSoup
import requests
import os


def convert_markdown_to_html(markdown_content):
    """
    Convert markdown content to HTML with proper numbering for news headlines

    Args:
        markdown_content (str): The markdown formatted content

    Returns:
        str: Properly formatted HTML content
    """
    # First convert markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all strong tags that contain numbered headlines
    headlines = soup.find_all('strong')

    # Counter for headlines
    headline_counter = 1

    for headline in headlines:
        # Check if this is a main headline (contains a number)
        text = headline.get_text()
        if text.strip().startswith(str(headline_counter) + '.'):
            # Replace with properly numbered headline
            new_text = f"{headline_counter}. {text.split('.', 1)[1].strip()}"
            headline.string = new_text
            headline_counter += 1

    # Convert back to string
    return str(soup)


crew=Crew(
    agents=[news_researcher,news_writer],
    tasks=[research_task,writer_task],
    process=Process.sequential
)

#starting the task execution process with enhanced feedback

# try:
#     # Attempt to run the task execution process
#     result = crew.kickoff()
#     print('raw result is')
#     print(result)
#     md_content = str(result)  # Assuming the result is in Markdown format
#     html_content = convert_markdown_to_html(md_content)
#     print('html contenet is')
#     print(html_content)
# except Exception as e:
#
#     # Catch any other exception that might occur
#     print("An unexpected error occurred:", e)
#     exit(1)
def execute_with_retry(crew, max_retries=3, delay_seconds=10):
    retries = 0
    while retries < max_retries:
        try:
            # Attempt to run the task execution process
            task_result = crew.kickoff()
            print(task_result)
            return task_result  # Return result if successful
        except Exception as e:
            # Catch any exception that might occur
            print(f"Attempt {retries + 1} failed with error: {e}")
            if "Resource has been exhausted" in str(e):
                print("Resource exhaustion detected. Retrying after a delay...")
                time.sleep(delay_seconds)  # Wait for a specified delay before retrying
                retries += 1
            else:
                # If it's a different error, print and exit
                print("An unexpected error occurred:", e)
                exit(1)
    print("Maximum retries reached. Exiting.")
    exit(1)

# Starting the task execution process with enhanced feedback and retry mechanism
result=execute_with_retry(crew, max_retries=3, delay_seconds=10)

md_content = str(result)  # Assuming the result is in Markdown format
html_content = convert_markdown_to_html(md_content)

# Mailchimp configuration
API_KEY = os.getenv('MAILCHIMP_API_KEY')
SERVER_PREFIX = os.getenv('MAILCHIMP_SERVER_PREFIX')
LIST_ID = os.getenv('LIST_ID')
campaign_url = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0/campaigns'
campaign_data = {
    "type": "regular",
    "recipients": {
        "list_id": LIST_ID
    },
    "settings": {
        "subject_line": "Daily News Summary",
        "from_name": "Aishwarya",
        "reply_to": "aishwaryakalburgi560@gmail.com"
    }
}

headers = {
    'Authorization': f'apikey {API_KEY}',
    'Content-Type': 'application/json'
}

response = requests.post(campaign_url, json=campaign_data, headers=headers)
campaign_id = response.json().get('id')

# Set campaign content
content_url = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0/campaigns/{campaign_id}/content'
content_data = {
    "html": html_content
}

response = requests.put(content_url, json=content_data, headers=headers)

# Send the campaign
send_url = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0/campaigns/{campaign_id}/actions/send'
response = requests.post(send_url, headers=headers)

if response.status_code == 204:
    print("Campaign sent successfully!")
else:
    print("Failed to send campaign:", response.json())

file_path = "crewOpenAI/new-blog-post.md"

if not os.path.exists(file_path):
    print(f"Error: {file_path} does not exist after script execution.")
else:
    print(f"Success: {file_path} exists.")
