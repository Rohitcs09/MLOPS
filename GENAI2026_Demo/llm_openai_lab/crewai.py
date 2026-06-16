from crewai import Agent, Task, Crew
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0.5)

# Agent 1 — Researcher
researcher = Agent(
    role="Research Specialist",
    goal="Find key information about given topic",
    backstory="Expert researcher who extracts important insights.",
    llm=llm
)

# Agent 2 — Writer
writer = Agent(
    role="Content Writer",
    goal="Write engaging content from research",
    backstory="Professional writer who converts info into readable content.",
    llm=llm
)

# Agent 3 — Editor
editor = Agent(
    role="Editor",
    goal="Improve content quality and readability",
    backstory="Expert editor ensuring polished output.",
    llm=llm
)

# Tasks
task1 = Task(
    description="Research top 5 AI tools for developers",
    agent=researcher
)

task2 = Task(
    description="Write a short blog using research",
    agent=writer
)

task3 = Task(
    description="Edit and improve the blog",
    agent=editor
)

# Crew setup
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[task1, task2, task3],
    verbose=True
)

# Run
result = crew.kickoff()
print(result)

