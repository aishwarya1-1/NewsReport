from crewai import Task
from agents import news_researcher,news_writer
from tools import tool

research_task = Task(
    description=("Identify and gather 7 latest news updates from all prominent kannada and english"
                 " newspapers of Karnataka State,"
                 ),
    expected_output='A comprehensive 7 paragraphs long report on the '
                    'collection of summarized news covering the latest events in Karnataka State.'
                    'which should include the title, key details (who, what, when, where, why, how)'
                    ' and source attribution and source link',
    tools=[tool],
    agent=news_researcher,
)
writer_task = Task(
    description=("Write well-researched, engaging, and informative headlines based on the "
                 "latest news events in Karnataka State, "
                 "The information should be in "
                 "compelling narrative style"),
    expected_output='A 7 headlines  covering the latest news events in Karnataka State ,each headline containing '
                    ' a title,'
                    ' detailed narrative, background information, and source attribution and '
                    'the source link formatted as markdown',
    tools=[tool],
    agent=news_writer,
    async_execution=False,
    output_file='new-blog-post.md'
)