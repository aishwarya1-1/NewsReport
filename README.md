# Karnataka News Subscription

## Overview
The **Karnataka News Subscription** project is an automated news summary system that fetches and delivers the latest news updates about Karnataka. The application leverages **CrewAI** to manage research agents, **Serper API** for web searches, and **Mailchimp** for email distribution. Users can subscribe to receive daily news summaries via email. The project is deployed on **GitHub Actions** and integrates with **Streamlit** for the user interface.

## Features
- **Automated News Summarization**: Utilizes CrewAI agents to fetch and summarize news.
- **Daily Email Updates**: Sends daily news summaries to subscribers via Mailchimp.
- **User Subscription Management**: Allows users to subscribe via a Streamlit UI.

## Architecture
### Technologies Used

- **Streamlit** (for frontend user interactions)
- **CrewAI** (for AI-powered news research and summarization)
- **Serper API** (for fetching the latest news via Google search)
- **Mailchimp API** (for email list management and sending news updates)
- **GitHub Actions** (for automating daily news summary execution.Runs at  9:00 AM IST)


### Workflow
1. **News Fetching**:
   - CrewAI agents use Serper API and Google Search API to fetch relevant news.
   - Extracted content is processed and stored.
2. **Summarization & Storage**:
   - CrewAI summarizes the latest news and saves it in `crewOpenAI/new-blog-post.md`.
3. **User Subscription**:
   - Users subscribe via a Streamlit form.
   - Email addresses are added to Mailchimp's subscriber list.
4. **Email Delivery**:
   - A GitHub Action runs daily at 09:00 AM.
   - News summaries are retrieved and emailed to subscribers.





## Contributing
Feel free to open issues and pull requests to improve the project. Contributions are welcome!





