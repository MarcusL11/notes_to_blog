from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
from note_to_blog_flow.config import LLM_CONFIGS
from crewai_tools import FileReadTool, MDXSearchTool
from note_to_blog_flow.tools.CharacterCounterTool import CharacterCounterTool
from note_to_blog_flow.types import Section


read_notes = FileReadTool(file_path="./notes.md")
semantic_search_notes = MDXSearchTool(mdx="./notes.mdx")
character_counter = CharacterCounterTool()


@CrewBase
class EditingCrew:
    """Review and Edit Blog Crew"""

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
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config["editor"],  # pyright: ignore
            llm=self.openai_llm,
            tools=[read_notes, semantic_search_notes, character_counter],
            verbose=True,
        )

    @task
    def review_edit_blog(self) -> Task:
        return Task(
            config=self.tasks_config["review_edit_blog"],  # pyright: ignore
            output_pydantic=Section,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Editing Crew"""
        return Crew(
            agents=self.agents,  # pyright: ignore
            tasks=self.tasks,  # pyright: ignore
            process=Process.sequential,
            verbose=True,
        )
