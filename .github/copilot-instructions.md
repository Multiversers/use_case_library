
# Technical Instructions for Use Case Generation

You (the AI assistant) are helping to build a **Use Case Library** for Software Developers looking to upskill with AI. These use cases will be handed off to Instructional Designers who will tailor the content further. We have a list of 70+ use cases that we need to **augment with additional information** according to the guidelines and the **multi-step AI workflow** summarized below. The end goal is to produce a set of well-polished, time-bound, and relevant use cases.

---

## CRITICAL AI ASSISTANT INSTRUCTIONS

1. **ALWAYS** activate and use the virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. **ALWAYS** return complete, functional code.
3. **ONLY** make changes relevant to the current task.
4. **NEVER** make unrelated changes.
5. **NEVER** delete existing functionality without user agreement.
6. **ADD** clear code comments explaining the "why" (in addition to the "what").
7. **MAINTAIN** strict Python best practices.
8. **FOLLOW** Perplexity and OpenAI API Documentation (models, usage, etc.).
9. **PRESERVE** existing functionality unless explicitly asked to remove it.
10. **ONLY** add dependencies when absolutely necessary.

---

## CORE PHILOSOPHY: RUTHLESSLY SIMPLE, LEAN, LIGHT, FAST, CLEVER
- If you have to explain it, don’t build it.
- If it requires extensive documentation, don’t add it.
- If it adds a dependency, don’t include it without checking with the user first.
- If it’s not absolutely necessary, don’t create it.

---

## USE CASE CATEGORIES

Use cases fall into one of these categories:

- **Core Skills**: Fundamental skills for working with AI coding tools.  
- **LLM API Fundamentals**: Working with AI APIs and prompt engineering.  
- **Challenges of Unstructured LLM Output (Parsing and Managing AI-Generated Text)**  
- **Tool Use & API Integrations with LLMs**  
- **Retrieval-Augmented Generation (RAG) and Memory**  
- **AI Agent Workflows and Architecture (Prompt Chaining & Agentic Behavior)**  
- **Fine-Tuning LLMs for Custom Use Cases**  
- **Deploying AI Applications (MLOps, Containers, and Cloud Deployment)**  
- **AI Observability & Logging (Monitoring LLM Behavior in Production)**  
- **Testing & Evaluating AI Systems (Best Practices for Software Developers)**  
- **Security & Governance for AI Applications (Safe and Ethical AI Deployment)**  

---

## WHAT WE ARE BUILDING

We use a **multi-step AI workflow** to generate each use case:

1. **Review Use Case High-level Design**
   - Review the use case high-level design requirements that our instructional designers compiled. Here's an example of how they look:

<use_case_high_level_design_requirements>
<AI_Tool>
Coding Assistants
</AI_Tool>

<Family>
Core Skills
</Family>

<Use_Case>
Craft Effective Code Prompts for AI Assistance
</Use_Case>

<Use_Case_ID>
CORE-02
</Use_Case_ID>

<Prerequisite_Dependency_Use_Case_IDs>
CORE-01
</Prerequisite_Dependency_Use_Case_IDs>

<Use_Case_Overview>
This use case trains developers to harness AI tooling by writing precise comments and docstrings that function as prompts for automated code generation. It emphasizes the importance of natural language clarity in directives (e.g., docstrings and TODOs) and guides participants to refine prompts as needed while validating AI-generated outputs against the original intent. The goal is to reduce cognitive load, minimize context switching, and ensure at least 80% of generated functions pass unit tests, using Python or JavaScript examples and tools like GitHub Copilot or VS Code IntelliCode.
</Use_Case_Overview>

<Description>
Treating your comments and function descriptions as prompts. For example, writing a clear docstring or a comment like ""// TODO: implement binary search"" can prompt the AI to generate the code for you. This is a skill – the better you describe the task or formula in natural language, the better the AI can help. Developers learn to phrase their intentions (in comments or chat with the assistant) precisely to get useful outputs.
</Description>

<Objective>
Enable developers to effectively communicate programming intent through structured comments that trigger accurate AI code generation.
</Objective>

<AI_Native>
Yes
</AI_Native>

<Assumed_Dev_Skills_Applied>
-Writing clear code comments
-Understanding code structure
-Basic algorithmic thinking
</Assumed_Dev_Skills_Applied>

<Assumed_AI_Skills_Applied>
-Familiarity with code completion tools
-Basic understanding of natural language processing
</Assumed_AI_Skills_Applied>

<New_AI_Skills_Taught>
-Prompt engineering for code generation
-Context-aware comment structuring
-AI output validation techniques
</New_AI_Skills_Taught>

<Manageable_Steps>
1. Write a detailed function description in docstring format
2. Add TODO comments with specific algorithm requirements
3. Use natural language to describe complex logic before implementation
4. Refine prompts based on initial AI outputs
5. Validate generated code against original intent
</Manageable_Steps>

<Time_Estimate(minutes)>
20
</Time_Estimate(minutes)>

<Measurable_Impact>
- reduction in manual coding time for boilerplate functions
- increase in first-attempt code correctness
- improvement in documentation coverage
</Measurable_Impact>

<Demo_Output_Brainstorm>
- AI-generated binary search implementation
- Complete docstring for matrix multiplication function
- Automated parameter validation code block
</Demo_Output_Brainstorm>

<Common_Pitfalls>
- Overly vague prompt phrasing
- Failure to validate type signatures
- Ignoring edge cases in generated code
- Blind acceptance of hallucinated solutions
</Common_Pitfalls>

<Success_Criteria>
- 80% of generated functions pass unit tests
- Comments match implementation behavior
- Reduced cognitive load measured by fewer context switches
</Success_Criteria>

<References>
- https://devblogs.microsoft.com/visualstudio/how-to-use-comments-to-prompt-github-copilot-visual-studio/ [4]
- https://dev.to/techiesdiary/chatgpt-prompts-for-adding-code-comments-5cod [1]
- https://www.mrlacey.com/2024/04/comments-in-code-written-by-ai.html [7]
</References>

<Status>
In Consideration
</Status>

<Maturity_Level>
Established
</Maturity_Level>

<Department(s)>
Software Development & DevOps
</Department(s)>

<Role(s)>
All Roles
</Role(s)>

<Platform_Link>

</Platform_Link>

<Comments>
Repurpose from GitHub Copliot M1-M4 modules?
</Comments>

<Considerations_for_Instructor_SME>
• Areas of Uncertainty:
   - 'Optimal level of granularity when describing a function or logic in comments
   - Criteria for determining when a prompt is sufficiently refined before moving on to implementation
   - Extent to which AI code generation tools handle edge cases or advanced scenarios without additional guiding comments'
• Potential Weaknesses:
   - 'Limited guidance on how to systematically debug or correct AI-generated mistakes when prompts are unclear
   - Possible overreliance on AI to generate final solutions without ensuring thorough human review
   - Risk of inadequate coverage if unit tests are not well-defined or comprehensive'
• Implementation Considerations:
   - 'Encourage iterative refinement of docstrings and TODO prompts to improve AI-generated outputs
   - Incorporate short, targeted unit tests to quickly validate generated code in real time
   - Demonstrate best practices for structuring function docstrings and inline comments so AI tools access consistent context
   - Provide diverse examples (e.g., simple search algorithms and more complex calculations) to illustrate the range of prompting techniques'
• Additional Guidance:
   - 'Begin with simple function prompts and gradually introduce more complex logic to illustrate how prompt detail impacts AI output
   - Highlight counterexamples where unclear or ambiguous comments lead to incorrect or incomplete generation
   - Emphasize the importance of reviewing and validating AI-generated code to maintain accountability and accuracy
   - Show how to apply prompt-engineering strategies to multiple programming languages while focusing on transferable principles
</Considerations_for_Instructor_SME>

</use_case_high_level_design_requirements>

2. **Deep Research** (using Perplexity)  
   - Gather and summarize additional context for the use case, searching recent/best practices.  
   - Optionally store partial results for troubleshooting or resumption.

3. **OpenAI Reasoning**  
   - Integrate the research and existing base use case content.  
   - Determine prerequisites or dependencies for the current use case.  
   - Produce a refined draft ensuring we do not re-teach skills already covered in earlier use cases.

4. **OpenAI Final Polishing**  
   - Ensure cohesive language, clarity, brand alignment, and 8th-grade reading level.  
   - Output final text, which is then appended to a CSV or stored for the next step in the pipeline.

We iterate over the list of use cases until we’ve reached the end. Each use case is time-bound (10–30 minutes), has a **measurable impact**, and **does not** re-teach basic dev skills (like how to manage API keys).

---

## USE CASE REQUIREMENTS

1. **Clear Objective**  
   - Each use case must have a specific, well-defined goal or task.

2. **Manageable Steps**  
   - Break tasks into small, achievable steps.

3. **Time-Bound**  
   - Completion must be possible within 10–30 minutes.

4. **Measurable Impact**  
   - Ideally, the use case should improve productivity or user satisfaction in a quantifiable way.

5. **Targeted Instructional Design**  
   - Teach the new “AI-native” skills needed to complete the task (e.g., prompt engineering, using an AI tool, analyzing outputs).
   - Avoid re-teaching universal developer skills such as “how to store an API key.”

---

## RULES FOR YOU

- Never break functional code.
- Ask clarifying questions to the user when needed.
- Avoid unnecessary complexity.

---

## API KEYS

All API keys (Perplexity, OpenAI, etc.) are **loaded from a `.env` file** for security.

---

## SUPPORTED MODELS

When generating or refining content, only use these models:

### Perplexity
- **Testing**: `sonar`
- **Single questions**: `sonar-pro`
- **Reasoning**: `sonar-reasoning-pro`
- **Deep research**: `sonar-deep-research`

### OpenAI
- **Reasoning (testing)**: `o3-mini-2025-01-31`
- **Reasoning (production)**: `o1`
- **Chat (testing)**: `gpt-4o-mini`
- **Chat (production)**: `gpt-4o`

Use them according to the workflow step you’re implementing or as directed in the script logic.

---

## ADDITIONAL NOTES

- You can skip teaching basic tasks that developers already know (e.g., “How to set up a Python environment”).
- Each use case will likely evolve as we integrate new research or user feedback; thus, the pipeline approach ensures we store partial results, handle errors, and produce a final refined deliverable.
- Always follow the brand language guidelines (concise, direct, US English, 8th-grade reading level, active voice).

That’s it—keep it **ruthlessly simple**, use the AI workflow effectively, and produce final use cases that meet the time-bound and measurable impact requirements.

<perplexity_API_documentation>
Perplexity API Documentation:

from openai import OpenAI

YOUR_API_KEY = "INSERT API KEY HERE"

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        ),
    },
    {   
        "role": "user",
        "content": (
            "How many stars are in the universe?"
        ),
    },
]

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="sonar-pro",
    messages=messages,
)
print(response)

# chat completion with streaming
response_stream = client.chat.completions.create(
    model="sonar-pro",
    messages=messages,
    stream=True,
)
for response in response_stream:
    print(response)

Prompt Guide
​
System Prompt
You can use the system prompt to provide instructions related to style, tone, and language of the response.

The real-time search component of our models does not attend to the system prompt.

Example of a system prompt

You are a helpful AI assistant.

Rules:
1. Provide only the final answer. It is important that you do not include any explanation on the steps below.
2. Do not show the intermediate steps information.

Steps:
1. Decide if the answer should be a brief sentence or a list of suggestions.
2. If it is a list of suggestions, first, write a brief and natural introduction based on the original query.
3. Followed by a list of suggestions, each suggestion should be split by two newlines.
​
User Prompt
You should use the user prompt to pass in the actual query for which you need an answer for. The user prompt will be used to kick off a real-time web search to make sure the answer has the latest and the most relevant information needed.

Example of a user prompt

What are the best sushi restaurants in the world currently?
</perplexity_API_documentation>

<openai_API_documentation>
OpenAI API Documentation:

from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)

Conversations and context:

const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [
    {
      "role": "user",
      "content": [{ "type": "text", "text": "knock knock." }]
    },
    {
      "role": "assistant",
      "content": [{ "type": "text", "text": "Who's there?" }]
    },
    {
      "role": "user",
      "content": [{ "type": "text", "text": "Orange." }]
    }
  ],
  store: true,
});

Reasoning Models Documentation:

from openai import OpenAI
client = OpenAI()

prompt = """
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

response = client.chat.completions.create(
    model="o3-mini",
    reasoning_effort="medium",
    messages=[
        {
            "role": "user", 
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)

Planning example:

from openai import OpenAI

client = OpenAI()

prompt = """
I want to build a Python app that takes user questions and looks 
them up in a database where they are mapped to answers. If there 
is close match, it retrieves the matched answer. If there isn't, 
it asks the user to provide an answer and stores the 
question/answer pair in the database. Make a plan for the directory 
structure you'll need, then return each file in full. Only supply 
your reasoning at the beginning and end, not throughout the code.
"""

response = client.chat.completions.create(
    model="o3-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
            ],
        }
    ]
)

print(response.choices[0].message.content)

Structured Outputs:

from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed

Structured Data Extraction:

from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class ResearchPaperExtraction(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure."},
        {"role": "user", "content": "..."}
    ],
    response_format=ResearchPaperExtraction,
)

research_paper = completion.choices[0].message.parsed
</openai_API_documentation>