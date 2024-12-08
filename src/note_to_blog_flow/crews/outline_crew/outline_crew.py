from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, MDXSearchTool
from crewai import LLM
from note_to_blog_flow.config import LLM_CONFIGS, FILE_PATH
from note_to_blog_flow.types import BlogOutline


read_notes = FileReadTool(file_path=FILE_PATH)
semantic_search_notes = MDXSearchTool(mdx=FILE_PATH)


@CrewBase
class OutlineCrew:
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
    def outliner(self) -> Agent:
        return Agent(
            config=self.agents_config["outliner"],  # pyright: ignore
            llm=self.openai_llm,
            tools=[read_notes, semantic_search_notes],
            verbose=True,
        )

    @task
    def generate_outline(self) -> Task:
        return Task(
            config=self.tasks_config["generate_outline"],  # pyright: ignore
            output_pydantic=BlogOutline,
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
