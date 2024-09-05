import streamlit as st
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import os

# Initialize Mailchimp Client
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
MAILCHIMP_SERVER_PREFIX = os.getenv('MAILCHIMP_SERVER_PREFIX')
AUDIENCE_ID = os.getenv('MAILCHIMP_LIST_ID')

client = Client()
client.set_config({
    "api_key": MAILCHIMP_API_KEY,
    "server": MAILCHIMP_SERVER_PREFIX
})

# Streamlit UI
st.title("Karnataka News Subscription")
NEWS_FILE = "crewOpenAI/new-blog-post.md"

def load_news():
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, "r") as file:
            return file.read()
    else:
        return "No news available."

news_result = load_news()
st.markdown(news_result, unsafe_allow_html=True)

# Input box for email
email = st.text_input("Add your email ID to receive news updates via email:")

def add_email_to_mailchimp(email):
    try:
        response = client.lists.add_list_member(AUDIENCE_ID, {
            "email_address": email,
            "status": "subscribed"
        })
        return response
    except ApiClientError as error:
        return error.text

if st.button("Subscribe"):
    if email:
        try:
        # Add email to Mailchimp list
            response = add_email_to_mailchimp(email)
            if isinstance(response, dict) and "status" in response and response["status"] == "subscribed":
                st.success("User successfully subscribed.")
            else:
                st.error("Failed to subscribe user. Please try again.")

        except ConnectionError as ce:
            st.error(f"Connection error occurred: {ce}")
        except Exception as e:
             st.error(f"An unexpected error occurred: {e}")
