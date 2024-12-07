from typing import List, Optional
from crewai.flow.flow import Flow, listen, start, router, or_
from pydantic import BaseModel
from note_to_blog_flow.types import BlogOutline
from note_to_blog_flow.crews.outline_crew.outline_crew import OutlineCrew
from note_to_blog_flow.crews.writing_crew.writing_crew import WriteBlogSectionCrew
from note_to_blog_flow.crews.review_crew.review_crew import ReviewBlogCrew
from note_to_blog_flow.crews.editing_crew.editing_crew import EditingCrew
from note_to_blog_flow.crews.scrape_crew.scrape_crew import ScrapeCrew
from note_to_blog_flow.config import LANGTRACE_API_KEY
from langtrace_python_sdk import langtrace
import os
import json

langtrace.init(api_key=LANGTRACE_API_KEY)


class BlogState(BaseModel):
    title: str = ""
    topic: str = ""
    goal: str = ""
    word_count: str = ""
    writing_style: str = ""
    blog: str = ""
    blog_outline: List[BlogOutline] = []
    feedback: Optional[str] = None
    date_time: str = ""
    retry_count: int = 0
    valid: bool = False


class BlogFlow(Flow[BlogState]):
    initial_state = BlogState

    if not os.path.exists("output"):
        os.makedirs("output")

    @start()
    def scrape_crew(self):
        print("Kickoff the Scrape Crew")
        output = ScrapeCrew().crew().kickoff()

        print("Front Matter:", output)
        print("Output type:", type(output))

        try:
            self.state.title = output["title"]
            self.state.topic = output["topic"]
            self.state.goal = output["goal"]
            self.state.word_count = output["word_count"]
            self.state.writing_style = output["writing_style"]
        except AttributeError:
            raise ValueError(
                "CrewOutput does not return the expected attributes. Verify its structure."
            )

        return output

    @listen(scrape_crew)
    def outline_crew(self):
        print("Kickoff the Outline Crew")

        output = (
            OutlineCrew()
            .crew()
            .kickoff(
                inputs={
                    "goal": self.state.goal,
                    "topic": self.state.topic,
                    "word_count": self.state.word_count,
                }
            )
        )
        sections = output["sections"]
        print("Sections:", sections)
        self.state.blog_outline = sections
        print("Blog Outline:", self.state.blog_outline)

        return sections

    @listen(outline_crew)
    def save_outline(self):
        print("Saving the Outline")
        file_name = f"./output/{self.state.title.replace(' ', '_')}_outline.json"
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(
                [section.model_dump() for section in self.state.blog_outline],
                file,
                ensure_ascii=False,
                indent=4,
            )

    @listen(or_(outline_crew, "retry"))
    def generate_blog_content(self):
        if self.state.retry_count == 0:
            print("Kickoff the Writing Crew")

            output = (
                WriteBlogSectionCrew()
                .crew()
                .kickoff(
                    inputs={
                        "blog_outline": self.state.blog_outline,
                        "goal": self.state.goal,
                        "topic": self.state.topic,
                        "word_count": self.state.word_count,
                        "writing_style": self.state.writing_style,
                        "title": self.state.title,
                        "feedback": self.state.feedback,
                    }
                )
            )
            blog_content = output["content"]
            print("Blog:", blog_content)
            self.state.blog = blog_content

            return blog_content

        if not self.state.valid and self.state.retry_count > 0:
            print("Kickoff the Revised Writing Crew")

            output = (
                EditingCrew()
                .crew()
                .kickoff(
                    inputs={
                        "blog": self.state.blog,
                        "feedback": self.state.feedback,
                    }
                )
            )
            blog_content = output["content"]
            print("Blog:", blog_content)
            self.state.blog = blog_content

            return blog_content

    @router(generate_blog_content)
    def evaluate_blog(self):
        print("Kickoff Verify the Blog Crew")
        print("Retry count:", self.state.retry_count)

        if self.state.retry_count > 3:
            print("Max retry exceeded")
            return "max_retry_exceeded"
        else:
            print("Retrying, current count:", self.state.retry_count)

        result = (
            ReviewBlogCrew()
            .crew()
            .kickoff(
                inputs={
                    "blog_outline": self.state.blog_outline,
                    "blog": self.state.blog,
                    "goal": self.state.goal,
                    "topic": self.state.topic,
                    "word_count": self.state.word_count,
                    "writing_style": self.state.writing_style,
                    "title": self.state.title,
                    "date_time": self.state.date_time,
                }
            )
        )
        self.state.valid = result["valid"]
        self.state.feedback = result["feedback"]

        print("valid", self.state.valid)
        print("feedback", self.state.feedback)
        self.state.retry_count += 1

        if self.state.valid:
            print("Validation successful, transitioning to complete")
            return "complete"

        print("Validation failed, transitioning to retry")
        return "retry"  # Emit retry state explicitly

    @listen("complete")
    def save_blog(self):
        print("Saving the Blog")
        print("Blog is valud")
        print("Blog:", self.state.blog)

        file_name = f"./output/{self.state.title.replace(' ', '_')}_complete.md"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(self.state.blog)

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")
        print("Blog:", self.state.blog)
        print("Feedback:", self.state.feedback)

        file_name = (
            f"./output/{self.state.title.replace(' ', '_')}_max_retry_exceeded.md"
        )
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(self.state.blog)


def kickoff():
    blog_flow = BlogFlow()
    blog_flow.kickoff()
    blog_flow.plot()


if __name__ == "__main__":
    kickoff()
