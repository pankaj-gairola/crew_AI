import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()


llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose = True,
                             temperature = 0.5,
                             google_api_key="GOOGLE_API_KEY")
# Create Agents
prompteng = Agent(
    role='prompt engineer',
    goal="write a prompt which can help in writing a code",
    backstory="You're an Highly  expert in writing a good prompt based on input ",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

Architect = Agent(
    role='Architect',
    goal="Write a High level design by which anyone can write code",
    backstory="You're a specialised software architecture who can design high level diagram based on prompt given",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

Developer = Agent(
    role='Developer',
    goal="write a python optimised code based on high level design",
    backstory="You're highly skilled python developer who can write python code based on high level design. He also check that there should not be any issue in code.code should run fine",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

# Create Tasks
task_search = Task(
    description="python program to analyse banknifty option chain data",
    agent=prompteng
)

task_design = Task(
    description="Create a high level design to analyse BANKNIFTY option chain data",
    agent=Architect
)

task_code = Task(
    description="write optimised python code which do good analysis for trader ",
    agent=Developer
)

# Create Crew
crew = Crew(
    agents=[prompteng, Architect, Developer],
    tasks=[task_search, task_design, task_code],
    verbose=2,
    process=Process.sequential
)

# Get your crew to work!
result = crew.kickoff()

print("#############")
print(result)
