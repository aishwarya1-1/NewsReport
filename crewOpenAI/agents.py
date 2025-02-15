#agents.py
from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()
import os
from tools import tool


api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print(f"GEMINI_API_KEY Loaded: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
else:
    print("GEMINI_API_KEY is not set!")

my_llm = LLM(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini/gemini-1.5-flash",
)
#CREATING A SENIOR RESEARCHER AGENT

news_researcher=Agent(
    role="Senior Researcher",
    goal='To provide comprehensive and up-to-date summaries of todays news happening in Karnataka State, '
         ' by gathering information from all the prominent newspapers of Karnataka',
    verbose=True,
    memory=True,
    backstory=(
        "The News Researcher acts as a tireless sentinel, meticulously scanning prominent newspapers," 
         "websites, and other digital sources to gather the latest news on Karnataka's politics, "
         "society, economy, and culture. With a strong sense of duty, the Researcher strives to sift through"
        " the noise, identifying key stories that truly matter to the people of Karnataka"
    ),
    max_iter=180,
    max_execution_time= 250,
    tools=[tool],
    llm=my_llm,
    allow_delegation=True

)

#creating a write agent to create news blogs
news_writer=Agent(
    role="Senior News Writer",
    goal='To write well-researched, engaging, and '
         ' and informative headlines covering todays news happening in the state of, '
         'Karnataka, sourced from all the prominent local newspapers.',
    verbose=True,
    memory=True,
    backstory=(
        "You are dedicated to providing high-quality content and your passion "
        "for storytelling continue to drive Karnataka's mission of keeping the community informed and engaged."
    ),
    tools=[tool],
    llm=my_llm,
    max_iter=180,
    max_execution_time= 250,
    allow_delegation=False

)