from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, MDXSearchTool
from crewai import LLM
from note_to_blog_flow.config import LLM_CONFIGS, FILE_PATH
from note_to_blog_flow.types import BlogFrontMatter


read_notes = FileReadTool(file_path="./notes.md")
semantic_search_notes = MDXSearchTool(mdx="./notes.mdx")


@CrewBase
class ScrapeCrew:
    """Blog Outline Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    openai_llm = LLM(
        model=LLM_CONFIGS["openai"]["model"],
        api_key=LLM_CONFIGS["openai"]["api_key"],
    )
    anthropic_llm = LLM(
        model=LLM_CONFIGS["anthropic"]["model"],
        api_key=LLM_CONFIGS["anthropic"]["api_key"],
    )

    @agent
    def scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["scraper"],  # pyright: ignore
            llm=self.openai_llm,
            tools=[read_notes, semantic_search_notes],
            verbose=True,
        )

    @task
    def scrape_front_matter(self) -> Task:
        return Task(
            config=self.tasks_config["scrape_front_matter"],  # pyright: ignore
            output_pydantic=BlogFrontMatter,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Blog Outline Crew"""
        return Crew(
            agents=self.agents,  # pyright: ignore
            tasks=self.tasks,  # pyright: ignore
            process=Process.sequential,
            verbose=True,
        )
