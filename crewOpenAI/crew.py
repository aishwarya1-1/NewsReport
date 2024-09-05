from crewai import Crew,Process
from tasks import research_task,writer_task
from agents import news_researcher,news_writer

import markdown
import requests
import os
crew=Crew(
    agents=[news_researcher,news_writer],
    tasks=[research_task,writer_task],
    process=Process.sequential
)

#starting the task execution process with enhanced feedback

result=crew.kickoff()
print(result)


md_content = str(result)  # Assuming the result is in Markdown format
html_content = markdown.markdown(md_content)

# Mailchimp configuration
API_KEY = os.getenv('MAILCHIMP_API_KEY')
SERVER_PREFIX = os.getenv('MAILCHIMP_SERVER_PREFIX')
LIST_ID = os.getenv('MAILCHIMP_LIST_ID')
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
