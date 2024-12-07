---
title: Advance CrewAI Setup for Long Format Content Creation
topic: Advance CrewAI Setup for Long Format Content Creation
goal: To create a blog post sharing tips on effective CrewAI Flow setup to achieve the best long format content creation results.
writing_style:  personal, first person view, technically informative with simple vocabulary
word_count: 3,000
---
Notes :
- The following our my notes on reviewing [Joao Moura and Matthew Berman on Advanced CrewAI Setup](https://youtu.be/KAsrbqJ8yas?t=283) video
- It is common to see or poor results for long format content pass to LLMs. It is also common to think that we just need a more advance model to provide better results, but in many cases its has to do more about the setup of the crew and the specific focus we have given the crew to optimize their output.
- In addition to that, OpenAi's o1 model has been noted to hallucinate more often compared to older models when it comes to  agent behavior, because normal model allows agents use tools that are provided for them while o1 model  uses their chain of thought processes in concluding their answers before allowing the agents to use any tools 
- A better approach in general Agentic collaboration or for long format content is to separate the crew into specialized crews.  For example, lets say we wanted to create a blog writing crew, we would create a research crew, planning crew and a writing crew.  
- This was explained by [Joao Moura in this video](https://youtu.be/KAsrbqJ8yas?t=283)   about this approach
- Choice of words is important to avoid the agent from straying off course of the intended task. For example, if we have a research task for a an agent to hand off its findings to an agent assigned for planning, we want the research agent to perform a thorough research report with information to be used by the agent planner. Below was the original context for the `expected_output`:

```yaml
expected_output: >
A thorough reserach report on {topic} with relevant information that can be turned into an educational piece of content afterwards.
```

- An improved context for the `expected_output` would be replacing  `turned into` with  `inspire` to avoid the agent from straying off to attempt in writing the content pieces and keep as much of a raw data for the planner.

```yaml
expected_output: >
A thorough reserach report on {topic} with relevant information that inspire educational content afterwards.
```

- Agents are taking text in and giving text out, and its good for a lot of use cases.  But when we have a specific output that is structured (i.e. keys and values and types) , we can use function calling from this agent to get us an actual object.  So then the object to do any programming things, like loops, For example, we can loop each of the object by calling another crew to work with. 
