#!/usr/bin/env python3

import os
import json
import sys
import logging
from typing import List, Optional, Dict, Callable, TypeVar, Any
import asyncio
from pydantic import BaseModel
from openai import OpenAI, AsyncOpenAI, APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import argparse
import time
from functools import wraps

T = TypeVar('T')  # Type variable for generic return type

# Load environment variables (API keys, etc.)
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

"""
Single File AI Workflow for Use Case Generation

Workflow Steps:

1. IDENTIFY RESEARCH QUESTIONS (OpenAI mini model)
   - Reviews use case requirements and design
   - Generates 2-4 focused research questions
   - Each question is self-contained with enough context for independent processing
   - Uses o3-mini-2025-01-31 model for efficient analysis

2. DEEP RESEARCH (Perplexity sonar-pro)
   - Executes all research questions in parallel using Perplexity API
   - Uses sonar-pro model for each question
   - Combines results into a comprehensive research document
   - Includes context prefix with use case title, family, and objective

3. REFINE USE CASE WITH OPENAI REASONING (Structured Output)
   - Combines original use case content with research findings
   - Applies brand guidelines and use case guidelines
   - Outputs structured JSON matching UseCaseStructuredOutput schema
   - Uses OpenAI's parse() method with o3-mini-2025-01-31 model

4. FINAL POLISH WITH OPENAI CHAT (Structured Output)
   - Ensures clarity, brand compliance, and 8th-grade reading level
   - Maintains structured format using UseCaseStructuredOutput schema
   - Uses GPT-4o model for final refinement
   - Generates both JSON and Markdown outputs

5. EXAMPLE SOLUTION GENERATION (OpenAI GPT-4o)
   - Creates a practical, demonstrable solution for the use case
   - Generates a 2-3 minute video-ready demonstration script
   - Ensures solution steps align with use case steps
   - Includes setup time, prerequisites, validation steps
   - Provides key teaching points and common pitfalls
   - Outputs structured JSON matching ExampleSolutionOutput schema
   - Handles both tool-specific and generic implementations
   - Uses GPT-4o model with structured output parsing

6. VISUAL ELEMENT SUGGESTIONS (NEW)
   - Takes the output from step 5 (example solution)
   - Makes SPECIFIC suggestions about which visual elements (screenshots, GIFs, code snippets, etc.)
     might add value to the main body of the use case
   - Ensures alignment with the subject matter
   - Uses GPT-4o model to generate recommendations

The workflow uses a JobManager to handle partial results and resumability:
- Creates unique job directories with UUID and timestamps
- Saves intermediate results after each step
- Allows workflow resumption from last completed step
- Maintains metadata about the job execution

Output formats:
- Intermediate steps: JSON stored in job-specific directories
- Final output: Both structured JSON and formatted Markdown
- Markdown output includes all metadata and is ready for documentation
"""

# -------------------------------------------------------------------------------------
# CONFIG - Use Case Input (User Inputs)
# -------------------------------------------------------------------------------------

def get_use_case_config(args):
    """Get use case configuration from command line arguments or use defaults."""
    return {
        "title": args.title if args.title else "Craft Effective Code Prompts for AI Assistance",
        "family": args.family if args.family else "Core Skills",
        "ai_tool": args.ai_tool if args.ai_tool else "Coding Assistants",
        "objective": args.objective if args.objective else "Enable developers to effectively communicate programming intent through structured comments that trigger accurate AI code generation",
        "description": args.description if args.description else """This use case trains developers to harness AI tooling by writing precise comments and docstrings that function as prompts for automated code generation. It emphasizes the importance of natural language clarity in directives (e.g., docstrings and TODOs) and guides participants to refine prompts as needed while validating AI-generated outputs against the original intent.""",
        "prerequisites": args.prerequisites.split(',') if args.prerequisites else "Writing clear code comments, Understanding code structure, Basic algorithmic thinking, Familiarity with code completion tools, Basic understanding of natural language processing",
        "time_estimate": args.time_estimate if args.time_estimate else "20 minutes",
        "steps": args.steps.split(',') if args.steps else "Write a detailed function description in docstring format, Add TODO comments with specific algorithm requirements, Use natural language to describe complex logic before implementation, Refine prompts based on initial AI outputs, Validate generated code against original intent",
        "tool": args.tool if args.tool else "GitHub Copilot",
        "department": args.department.split(',') if args.department else "SWE",
        "role": args.role.split(',') if args.role else "front-end",
        "mode": args.mode if args.mode else "inline chat",
        "model": args.model if args.model else "GPT-4o",
        "coding_language": args.coding_language if args.coding_language else "Python",
    }

# -------------------------------------------------------------------------------------
# Format the USE_CASE_CONFIG in the expected XML-like format
# -------------------------------------------------------------------------------------
def format_use_case_content():
    """Format all USE_CASE_CONFIG fields into a structured XML-like format."""
    # Core sections that need special formatting
    prerequisites_str = "\n".join(f"- {prereq}" for prereq in USE_CASE_CONFIG['prerequisites'])
    steps_str = "\n".join(f"- {step}" for step in USE_CASE_CONFIG['steps'])

    # Optional lists that need array formatting
    department_str = ", ".join(USE_CASE_CONFIG['department']) if USE_CASE_CONFIG.get('department') else ""
    role_str = ", ".join(USE_CASE_CONFIG['role']) if USE_CASE_CONFIG.get('role') else ""

    return f"""
<Use_Case>{USE_CASE_CONFIG['title']}</Use_Case>
<Family>{USE_CASE_CONFIG['family']}</Family>
<AI_Tool>{USE_CASE_CONFIG['ai_tool']}</AI_Tool>
<Objective>{USE_CASE_CONFIG['objective']}</Objective>
<Description>{USE_CASE_CONFIG['description']}</Description>
<Prerequisites>
{prerequisites_str}
</Prerequisites>
<Time_Estimate>{USE_CASE_CONFIG['time_estimate']}</Time_Estimate>
<Steps>
{steps_str}
</Steps>
<Tool>{USE_CASE_CONFIG['tool']}</Tool>
<Department>{department_str}</Department>
<Role>{role_str}</Role>
<Mode>{USE_CASE_CONFIG['mode']}</Mode>
<Model>{USE_CASE_CONFIG['model']}</Model>
<Coding_Language>{USE_CASE_CONFIG['coding_language']}</Coding_Language>
"""

# -------------------------------------------------------------------------------------
# CONFIG - Brand Language and Use Case Guidelines
# -------------------------------------------------------------------------------------

BRAND_LANGUAGE_GUIDELINES = """
• Content is written at an 8th-grade reading level: Content is easy for anyone to understand.
• Content is written in the active voice: Writing empowers learners to find solutions and take action. Passive voice is avoided.
• Content addresses the reader as "you": Point of view is consistent and avoids third-person references like "business leaders" or "apprentices."
• Content is written in a conversational tone: The tone is action-oriented, clear, and energized. Content should assume the knowledge of an average junior developer and minimize the use of unnecessary jargon. Define any terms or processes that are more complex or advanced.
• Content is in US English: Content follows US spelling, grammar, and punctuation unless written explicitly for a UK-based audience.
• Content is concise: Writing is focused and to-the-point.
• Content is broken into digestible sections. Text that is longer than a sentence is broken down into bullets.
• Bullets, headings, and formatting help scanning: Formatting makes content easy to navigate and understand.
• Content is free of spelling, grammar, and punctuation errors: Writing adheres to professional standards.
• Grammar and punctuation follow the Chicago Manual of Style: There is consistency across all content.
• Sentence case is used for all titles and headings: Titles and headings are formatted with minimal capitalization.
• Numbers, dates, times, percentages, and money are consistently formatted: Words are used for numbers zero through nine, numerals for 10 and above, dates follow "Month Day, Year," times are formatted like "10:30am," percentages use %, and money uses currency symbols.
• All original sources are cited using Chicago style: Whenever data is referenced, the original source is cited and linked.
• Writing is bias-free: Content depicts diverse perspectives, avoids stereotypes, and uses gender-neutral terms. Militaristic, exclusionary language is not used. (eg: "sale representative" vs "salesman")
• Writing avoids outdated or inappropriate acronyms: Precise terms are used when referring to specific groups. ("Permit list" vs "Whitelist")
• Writing uses asset-based, specific language: Writing focuses on strengths and potential rather than deficits. (eg: "learners with additional learning needs" vs "special needs learners")
"""

# The use case guidelines themselves (abbreviated to keep it manageable in the prompt)
USE_CASE_GUIDELINES = (
    "Use Case Guidelines:\n"
    "1. Structure and Format:\n"
    "   - Follow the provided XML structure consistently\n"
    "   - Include all required sections: Overview, Description, Objective, Prerequisites, Steps, Metrics\n"
    "   - Ensure each section has a clear purpose and adds value\n"
    "\n"
    "2. Content Quality Standards:\n"
    "   - Clear, specific, time-bound, relevant, achievable goals\n"
    "   - Repeatable, measurable processes and outcomes\n"
    "   - Each step must be essential and purposeful\n"
    "   - Steps should be sequential, logical, and self-contained\n"
    "\n"
    "3. Technical Aspects:\n"
    "   - Include accurate time estimates for completion\n"
    "   - Clearly define all prerequisites and dependencies\n"
    "   - Specify required tools, permissions, and resources\n"
    "   - Document potential obstacles and mitigation strategies\n"
    "\n"
    "4. Implementation Guidance:\n"
    "   - Provide concrete, actionable examples where appropriate\n"
    "   - Include verification steps to confirm successful completion\n"
    "   - Define measurable success criteria and metrics\n"
    "   - Address common variations and edge cases\n"
    "\n"
    "5. Integration:\n"
    "   - Reference related use cases when appropriate\n"
    "   - Ensure consistency with other documentation\n"
    "   - Identify where this use case fits in larger workflows\n"
)

# -------------------------------------------------------------------------------------
# Pydantic Models
# -------------------------------------------------------------------------------------

class UseCaseMetadata(BaseModel):
    """Holds all miscellaneous metadata about the use case,
    including basic IDs, tool references, complexity levels, etc.
    """
    ai_tool: Optional[str]
    family: Optional[str]
    status: Optional[str]
    complexity_level: Optional[str]
    customization_level: Optional[str]
    time_minutes: Optional[int]
    department: Optional[List[str]]
    role: Optional[List[str]]
    notes: Optional[str]
    tool: Optional[str]
    mode: Optional[str]
    model: Optional[str]
    coding_language: Optional[str]
    # Add any other metadata fields you need here

class SubStep(BaseModel):
    """
    Represents a single substep within a step.

    Attributes:
      - title: Brief title of the substep
      - description: Optional longer description or bullet points
      - bullets: Optional list of bullet points for additional detail
    """
    title: str
    description: Optional[str] = None
    bullets: Optional[List[str]] = None

class UseCaseStep(BaseModel):
    """
    Represents a single step in the use case workflow.

    Attributes:
      - step_title: Brief name of the step, e.g. "Draft a docstring."
      - step_instructions: Concise instructions for the user (1-3 sentences).
      - sub_steps: Optional list of SubStep objects for more detailed breakdown
      - advice: (Optional) Best practices, troubleshooting tips, or cautionary notes.
    """
    step_title: str
    step_instructions: str
    sub_steps: Optional[List[SubStep]] = None
    advice: Optional[str] = None

class Citation(BaseModel):
    """
    Represents a citation for a research source.
    
    Attributes:
        url: The URL of the source
        title: The title of the source
        snippet: A relevant snippet/quote from the source
        relevance_score: AI-assigned score for relevance (0-1)
    """
    url: str
    title: Optional[str] = None
    snippet: Optional[str] = None
    relevance_score: Optional[float] = None

class UseCaseStructuredOutput(BaseModel):
    """
    Fields:
      - title: e.g. "Craft Effective Code Prompts for AI Assistance"
      - time_to_complete: e.g. "20 minutes"
      - description: 2-3 sentences describing the primary objective
      - steps: A list of UseCaseStep objects
      - resources: A list of resource links or doc references
      - metadata: A UseCaseMetadata object for ID, tool references, prerequisites, etc.
      - citations: A list of Citation objects for research sources
    """
    title: str
    time_to_complete: str
    description: str
    steps: List[UseCaseStep]
    resources: List[str]
    metadata: Optional[UseCaseMetadata] = None
    citations: Optional[List[Citation]] = None

class Step(BaseModel):
    """
    Represents a single step in the example solution.
    """
    action: str
    code_or_prompt: str

class ExampleSolution(BaseModel):
    """
    Represents a complete example solution for a use case.
    
    Fields:
      - title: Brief title for the example (e.g. "Binary Search Implementation with AI-Assisted Comments")
      - setup_time: Estimated setup time in minutes
      - demo_time: Estimated demo time in minutes (2-3 minutes target)
      - prerequisites: List of required setup steps (environment, tools, etc.)
      - scenario: A real-world context for the example
      - steps: Ordered list of demo steps with code/prompts
      - validation: How to verify the solution works
      - key_points: Teaching points to emphasize
      - common_issues: Potential problems to watch for
      - variations: Optional variations for different contexts
    """
    title: str
    setup_time: int
    demo_time: int
    prerequisites: List[str]
    scenario: str
    steps: List[Step]
    validation: List[str]
    key_points: List[str]
    common_issues: List[str]
    variations: List[str]  # Make this required but allow empty list

class ExampleSolutionOutput(BaseModel):
    """
    The complete output including metadata and the solution.
    """
    metadata: UseCaseMetadata
    solution: ExampleSolution
    demo_script: str  # Natural language script for 2-3 min demo

# -------------------------------------------------------------------------------------
# Create specific retry decorators for each API
# -------------------------------------------------------------------------------------
def create_retry_decorator(
    max_retries: int = 3,
    min_wait: float = 1,
    max_wait: float = 10,
    logging_prefix: str = ""
) -> Callable:
    """Creates a retry decorator with exponential backoff for API calls.
    
    Args:
        max_retries: Maximum number of retry attempts
        min_wait: Minimum wait time between retries in seconds
        max_wait: Maximum wait time between retries in seconds
        logging_prefix: Prefix for log messages to identify the context
        
    Returns:
        Decorator function that implements the retry logic
    """
    def retry_decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            attempt = 1
            while attempt <= max_retries:
                try:
                    return func(*args, **kwargs)
                except (APIError, APIConnectionError, RateLimitError) as e:
                    if attempt == max_retries:
                        logging.error(
                            "%sFailed after %d attempts: %s", 
                            logging_prefix, max_retries, str(e)
                        )
                        raise  # Re-raise on final attempt
                    
                    # Calculate wait time with exponential backoff
                    wait_time = min(max_wait, min_wait * (2 ** (attempt - 1)))
                    
                    logging.warning(
                        "%sAttempt %d/%d failed: %s. Retrying in %.1f seconds...",
                        logging_prefix, attempt, max_retries, str(e), wait_time
                    )
                    
                    time.sleep(wait_time)
                    attempt += 1
                except Exception as e:
                    # Don't retry on other exceptions
                    logging.error("%sUnexpected error: %s", logging_prefix, str(e))
                    raise
        return wrapper
    return retry_decorator

# Create specific retry decorators for each API
retry_openai = create_retry_decorator(
    logging_prefix="[OpenAI] "
)

retry_perplexity = create_retry_decorator(
    max_retries=5,  # More retries for Perplexity as it's less stable
    min_wait=2,     # Start with longer waits
    max_wait=15,    # Allow longer max wait
    logging_prefix="[Perplexity] "
)

# Wrap the API clients with retry logic
class RetryOpenAI:
    """Wrapper for OpenAI client that adds retry logic to all API calls."""
    def __init__(self, client: OpenAI):
        self._client = client
    
    @retry_openai
    def chat_completion_create(self, *args, **kwargs):
        return self._client.chat.completions.create(*args, **kwargs)
    
    @retry_openai
    def chat_completion_parse(self, *args, **kwargs):
        return self._client.beta.chat.completions.parse(*args, **kwargs)

class RetryPerplexity:
    """Wrapper for Perplexity client that adds retry logic to all API calls."""
    def __init__(self, client: AsyncOpenAI):
        self._client = client
    
    @retry_perplexity
    async def chat_completion_create(self, *args, **kwargs):
        return await self._client.chat.completions.create(*args, **kwargs)

# -------------------------------------------------------------------------------------
# Initialize API Clients
# -------------------------------------------------------------------------------------
_perplexity_client = AsyncOpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
_openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Wrap clients with retry logic
perplexity_client = RetryPerplexity(_perplexity_client)
openai_client = RetryOpenAI(_openai_client)

# -------------------------------------------------------------------------------------
# Basic Configuration Constants
# -------------------------------------------------------------------------------------
WORK_DIR = "partial_results"  # Base directory for all partial results
os.makedirs(WORK_DIR, exist_ok=True)

class JobManager:
    """Manages unique job directories for partial results."""
    
    def __init__(self, title: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "_".join(title.lower().split())
        self.job_id = f"{safe_title}_{timestamp}"
        # Create directory in use_cases/
        self.job_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "python-generator-use-cases", self.job_id)
        os.makedirs(self.job_dir, exist_ok=True)
        
        # Set up logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging to write to both file and console with different levels and formats."""
        log_file = os.path.join(self.job_dir, "execution.log")
        
        # Create formatters
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_formatter = logging.Formatter('%(message)s')  # Cleaner console output
        
        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)  # Capture all levels
        
        # Remove any existing handlers to avoid duplication
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # File handler - captures everything for debugging
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
        
        # Console handler - only shows important progress
        console_handler = logging.StreamHandler(sys.stdout)  # Explicitly use stdout
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)  # Only show INFO and above
        root_logger.addHandler(console_handler)
        
        # Test logging setup
        logging.debug("Logging setup complete - DEBUG message (file only)")
        logging.info("Logging setup complete - INFO message (console + file)")
        
    def get_filepath(self, step_name: str) -> str:
        """Get the full filepath for a step result."""
        return os.path.join(self.job_dir, f"{step_name}.json")
    
    def save_metadata(self, use_case_config: dict):
        """Save job metadata for reference."""
        metadata = {
            "job_id": self.job_id,
            "created_at": datetime.now().isoformat(),
            "use_case_title": use_case_config["title"]
        }
        with open(os.path.join(self.job_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

    def handle_step_failure(self, step_name: str, error: Exception) -> Optional[str]:
        """Handle a step failure by attempting to provide partial results.
        
        Args:
            step_name: Name of the failed step
            error: The exception that occurred
            
        Returns:
            Optional[str]: Partial results if available, None otherwise
        """
        # Log the failure
        logging.error("Step '%s' failed: %s", step_name, str(error))
        
        # Check if we have partial results from a previous run
        partial_result = load_partial_result(self, step_name)
        if partial_result:
            logging.warning(
                "Using partial results from previous run for step '%s'", 
                step_name
            )
            return partial_result
            
        # For certain steps, we can provide empty but valid results
        if step_name == "research_questions":
            return "What are the current best practices for this use case?\nWhat are common pitfalls to avoid?"
        elif step_name == "deep_research":
            return json.dumps({
                "content": "Research unavailable due to API error. Please review manually.",
                "citations": []
            })
        elif step_name == "visual_suggestions":
            return "Visual suggestions unavailable due to processing error."
            
        # For critical steps that can't be skipped, re-raise the error
        if step_name in ["refined_draft", "final_use_case", "example_solution"]:
            raise error
            
        return None

# Update helper functions to use JobManager
def load_partial_result(job_manager: JobManager, step_name: str) -> Optional[str]:
    """Load a partial result from the job-specific directory."""
    filepath = job_manager.get_filepath(step_name)
    if os.path.isfile(filepath):
        logging.info(f"[Resume] Found existing {step_name}...")  # Standardized to logging
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("content", "")
    return None

def save_partial_result(job_manager: JobManager, step_name: str, content: str):
    """Save a partial result to the job-specific directory."""
    filepath = job_manager.get_filepath(step_name)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"content": content}, f, indent=2)

# -------------------------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------------------------

def log_ai_interaction(step: str, prompt: str, response: str):
    """Log AI interactions to console with clear formatting."""
    logging.debug(f"\n{'='*80}")
    logging.debug(f"STEP: {step}")
    logging.debug(f"{'-'*80}")
    logging.debug("PROMPT:")
    logging.debug(f"{'-'*40}")
    logging.debug(prompt)
    logging.debug(f"{'-'*40}")
    logging.debug("RESPONSE:")
    logging.debug(f"{'-'*40}")
    logging.debug(response)
    logging.debug(f"{'='*80}\n")

def log_prompt(step: str, messages: list):
    """Log the full prompt before execution."""
    logging.debug(f"\n{'='*80}")
    logging.debug(f"INITIATING STEP: {step}")
    logging.debug(f"{'-'*80}")
    logging.debug("FULL PROMPT:")
    logging.debug(f"{'-'*40}")
    for msg in messages:
        # Handle both 'system' and 'developer' roles as system messages
        role = "system" if msg['role'] in ['system', 'developer'] else msg['role']
        logging.debug(f"[{role}]")
        logging.debug(msg['content'])
        logging.debug(f"{'-'*40}")
    logging.debug(f"{'='*80}\n")

def convert_json_to_markdown(json_content: str, example_solution_json: Optional[str] = None, visual_suggestions: Optional[str] = None) -> str:
    """Convert the structured JSON output to a readable markdown format."""
    try:
        data = json.loads(json_content)
        
        markdown = f"""# {data['title']}

**Time to Complete:** {data['time_to_complete']}

## Description
{data['description']}

## Steps
"""
        for i, step in enumerate(data['steps'], 1):
            markdown += f"### Step {i}: {step['step_title']}\n"
                
            markdown += f"{step['step_instructions']}\n\n"
            
            if step.get('sub_steps'):
                for j, sub_step in enumerate(step['sub_steps'], 1):
                    markdown += f"{j}. **{sub_step['title']}**\n"
                    if sub_step.get('description'):
                        markdown += f"   {sub_step['description']}\n"
                    if sub_step.get('bullets'):
                        for bullet in sub_step['bullets']:
                            markdown += f"   - {bullet}\n"
                    markdown += "\n"
                
            if step.get('advice'):
                markdown += f"{step['advice']}\n\n"

        if data['resources']:
            markdown += "## Resources\n"
            # Group resources by type
            resources_by_type = {
                'tool': [],
                'language': [],
                'mode': []
            }
            
            for resource in data['resources']:
                if isinstance(resource, dict):
                    resource_type = resource.get('type', 'tool')  # Default to tool if not specified
                    resources_by_type[resource_type].append(resource)
                else:
                    # Legacy format - treat as tool resource
                    resources_by_type['tool'].append({'url': resource, 'title': 'Official Resource'})
            
            # Output resources in priority order with headers
            type_headers = {
                'tool': 'Tool Documentation',
                'language': 'Language Documentation',
                'mode': 'Mode-specific Documentation'
            }
            
            for res_type, header in type_headers.items():
                resources = resources_by_type[res_type]
                if resources:
                    markdown += f"### {header}\n"
                    for resource in resources:
                        title = resource.get('title', 'Official Resource')
                        url = resource['url']
                        section = resource.get('section', '')
                        markdown += f"* [{title}]({url})"
                        if section:
                            markdown += f" - {section}"
                        markdown += "\n"
                    markdown += "\n"

        if data.get('citations'):
            markdown += "## Additional References\n"
            # Sort citations by relevance score (highest first)
            sorted_citations = sorted(
                data['citations'], 
                key=lambda x: float(x.get('relevance_score', 0)), 
                reverse=True
            )
            for citation in sorted_citations:
                markdown += f"* [{citation.get('title', 'Untitled')}]({citation['url']})"
                if citation.get('snippet'):
                    markdown += f"\n  > {citation['snippet']}"
                markdown += "\n"
            markdown += "\n"

        if example_solution_json:
            example = json.loads(example_solution_json)
            solution = example['solution']
            
            markdown += f"""## Example Solution: {solution['title']}

**Setup Time:** {solution['setup_time']} minutes  
**Demo Time:** {solution['demo_time']} minutes

### Scenario
{solution['scenario']}

### Prerequisites
"""
            for prereq in solution['prerequisites']:
                markdown += f"* {prereq}\n"
            
            markdown += "\n### Demo Steps\n"
            for i, step in enumerate(solution['steps'], 1):
                markdown += f"{i}. **{step['action']}**\n"
                if 'code_or_prompt' in step:
                    markdown += f"```\n{step['code_or_prompt']}\n```\n"
            
            markdown += "\n### Validation\n"
            for check in solution['validation']:
                markdown += f"* {check}\n"
            
            markdown += "\n### Key Teaching Points\n"
            for point in solution['key_points']:
                markdown += f"* {point}\n"
            
            markdown += "\n### Common Issues to Watch For\n"
            for issue in solution['common_issues']:
                markdown += f"* {issue}\n"
            
            if solution.get('variations'):
                markdown += "\n### Variations\n"
                for variation in solution['variations']:
                    markdown += f"* {variation}\n"
            
            markdown += f"\n### Demo Script\n{example['demo_script']}\n"

        # Add visual suggestions section if provided
        if visual_suggestions:
            markdown += "\n## Visual Elements\n"
            markdown += "The following visual elements are recommended to enhance this use case:\n\n"
            markdown += visual_suggestions + "\n"

        if data.get('metadata'):
            markdown += "\n## Metadata\n"
            meta = data['metadata']
            for key, value in meta.items():
                if value is not None:
                    if isinstance(value, list):
                        markdown += f"* **{key}:** {', '.join(value)}\n"
                    else:
                        markdown += f"* **{key}:** {value}\n"

        return markdown
    except Exception as e:
        print(f"Error converting JSON to Markdown: {e}")
        return ""

def write_markdown_file(markdown_content: str, title: str, job_manager: JobManager):
    """Write the markdown content to a file in the use cases directory."""
    # Create markdown file in the same directory as partial results
    filename = "use_case.md"
    filepath = os.path.join(job_manager.job_dir, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        logging.info("📝 Wrote markdown file to: %s", filepath)
    except Exception as e:
        logging.error("❌ Error writing markdown file: %s", e)

def validate_environment() -> None:
    """Validate required environment variables are set."""
    required_vars = ["PERPLEXITY_API_KEY", "OPENAI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# -------------------------------------------------------------------------------------
# STEP 1: IDENTIFY RESEARCH QUESTIONS (OpenAI Reasoning)
# -------------------------------------------------------------------------------------
def identify_research_questions(openai_client, use_case_content, job_manager: JobManager):
    """
    Use OpenAI to generate 2-4 distinct research questions for Perplexity.
    Each question should be self-contained with enough context and incorporate
    critical elements from the use case configuration.
    """
    step_name = "research_questions"
    existing_content = load_partial_result(job_manager, step_name)
    if existing_content:
        logging.info("↻ Resuming from existing research questions")
        return existing_content.split("\n")

    messages = [
        {
            "role": "developer",
            "content": (
                "You are an AI researcher tasked with generating research questions for a software development use case. "
                "Your questions will be processed independently by another AI system to gather comprehensive information.\n\n"
                "CRITICAL REQUIREMENTS FOR QUESTION GENERATION:\n\n"
                "1. CONTENT INTEGRATION:\n"
                "   - Extract and incorporate key technical elements from the use case (tools, models, languages, etc.)\n"
                "   - Include specific version numbers, frameworks, or technologies when mentioned\n"
                "   - Reference any unique methodologies or approaches specified\n\n"
                "2. QUESTION STRUCTURE:\n"
                "   - Each question must be fully self-contained with sufficient context\n"
                "   - Focus on distinct aspects or subtopics\n"
                "   - Include relevant technical terms and industry standards\n\n"
                "3. COVERAGE REQUIREMENTS:\n"
                "   - At least one question must focus on tool-specific capabilities or features, if provided\n"
                "   - At least one question must address best practices or common pitfalls\n"
                "   - If specific models/versions are mentioned, include version-specific research\n\n"
                "4. SCOPE AND SPECIFICITY:\n"
                "   - Questions should be specific enough to yield actionable insights\n"
                "   - Include temporal context (e.g., 'current best practices', 'latest features')\n"
                "   - Reference any relevant prerequisites or dependencies\n\n"
                "FORMAT REQUIREMENTS:\n"
                "- Generate exactly 2-4 questions\n"
                "- One question per line\n"
                "- No numbering or prefixes\n"
                "- Each question should be a complete, well-formed research query\n"
            )
        },
        {
            "role": "user",
            "content": f"Generate research questions for this use case:\n\n{use_case_content}"
        }
    ]

    try:
        # Log the full prompt before execution
        log_prompt("1 - Identify Research Questions", messages)
        
        response = openai_client.chat_completion_create(
            model="o3-mini-2025-01-31",
            reasoning_effort="medium",
            messages=messages,
        )
        questions = response.choices[0].message.content.strip().split("\n")
        questions = [q.strip() for q in questions if q.strip()]
        
        log_ai_interaction(
            "1 - Identify Research Questions",
            messages[-1]["content"],
            "\n".join(questions)
        )
        
        save_partial_result(job_manager, step_name, "\n".join(questions))
        return questions
    except Exception as e:
        logging.error("Failed to identify research questions: %s", str(e))
        raise  # Re-raise to maintain error handling chain

# -------------------------------------------------------------------------------------
# STEP 2: RESEARCH ALL QUESTIONS (Perplexity API)
# -------------------------------------------------------------------------------------
async def fetch_url_title(url: str, session: aiohttp.ClientSession) -> Optional[str]:
    """
    Fetch the title of a webpage asynchronously.
    Returns None if the request fails or no title is found.
    """
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title
                if title and title.string:
                    return title.string.strip()
    except Exception as e:
        logging.warning("Could not fetch title for %s: %s", url, e)
    return None

async def deep_research(perplexity_client, use_case_content, research_questions, job_manager: JobManager):
    """
    Execute research using Perplexity API with a single comprehensive prompt.
    """
    step_name = "deep_research"
    existing_content = load_partial_result(job_manager, step_name)
    if existing_content:
        logging.info("↻ Resuming from existing research results")
        return existing_content

    # Extract context from use case content
    use_case_title = None
    use_case_family = None
    use_case_objective = None
    
    for line in use_case_content.splitlines():
        if ("<Use_Case>" in line):
            use_case_title = line.replace("<Use_Case>", "").replace("</Use_Case>", "").strip()
        elif ("<Family>" in line):
            use_case_family = line.replace("<Family>", "").replace("</Family>", "").strip()
        elif ("<Objective>" in line):
            use_case_objective = line.replace("<Objective>", "").replace("</Objective>", "").strip()
    
    # Build comprehensive research prompt
    context = f"""I'm researching for a use case titled '{use_case_title}' in the category '{use_case_family}'. 
The objective is: '{use_case_objective}'. 
This is for creating developer educational content about AI skills.

Please research and provide comprehensive information addressing these questions:
{chr(10).join(f"- {q}" for q in research_questions)}

Format your response to be directly usable in educational materials about AI technologies and software development practices.
Include specific examples, code samples when relevant, and cite recent sources."""

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a specialized AI researcher providing comprehensive information for educational "
                    "content creation. Your responses should be thorough, well-structured, and include "
                    "relevant technical details, best practices, and real-world examples."
                )
            },
            {
                "role": "user",
                "content": context
            }
        ]
        
        # Log the full prompt before execution
        log_prompt("2 - Deep Research", messages)
        
        response = await perplexity_client.chat_completion_create(
            model="sonar-pro",
            messages=messages,
        )
        
        # Handle citations if present
        citations = []
        if hasattr(response, 'citations') and response.citations:
            async with aiohttp.ClientSession() as session:
                title_tasks = [fetch_url_title(url, session) for url in response.citations]
                titles = await asyncio.gather(*title_tasks)
                
                for url, title in zip(response.citations, titles):
                    citations.append({
                        'url': url,
                        'title': title,
                        'snippet': None,
                        'relevance_score': None
                    })
        
        # Format research results
        research_results = {
            'content': response.choices[0].message.content.strip(),
            'citations': citations
        }
        
        log_ai_interaction(
            "2 - Deep Research",
            context,
            json.dumps(research_results, indent=2)
        )
        
        save_partial_result(job_manager, step_name, json.dumps(research_results))
        return research_results
        
    except Exception as e:
        print(f"ERROR in Step 2 (Deep Research): {e}")
        raise

# -------------------------------------------------------------------------------------
# STEP 3: REFINE USE CASE WITH OPENAI REASONING (Structured)
# -------------------------------------------------------------------------------------
def refine_use_case_with_reasoning(openai_client, raw_research, use_case_content, job_manager: JobManager):
    """
    Combine the research results with the use case content, producing a structured JSON
    that matches the UseCaseStructuredOutput Pydantic model.

    We'll store the final JSON as a string in partial results.
    """
    step_name = "refined_draft"
    existing_content = load_partial_result(job_manager, step_name)
    if existing_content:
        print("[Resume] Found existing refined draft.")
        return existing_content

    # Load research content and citations
    if isinstance(raw_research, str):
        # Handle legacy format or resumption from string
        research_data = {'content': raw_research, 'citations': []}
    else:
        research_data = raw_research

    # First, have OpenAI score and select the best citations
    citation_scoring_prompt = (
        "You will be given a list of citations from research. Score each citation's relevance "
        "to our use case (0.0 to 1.0) and classify them into two categories.\n\n"
        f"Context:\n"
        f"- Tool: {USE_CASE_CONFIG.get('tool', 'Not specified')}\n"
        f"- Language: {USE_CASE_CONFIG.get('coding_language', 'Not specified')}\n"
        f"- Mode: {USE_CASE_CONFIG.get('mode', 'Not specified')}\n\n"
        "1. Official Resources (score >= 0.9):\n"
        "   - Official documentation from the tool/language vendor\n"
        "   - Official blogs or tutorials from the tool/language creator\n"
        "   - Official GitHub repositories or documentation\n"
        "Priority order:\n"
        "a) Tool-specific documentation (e.g. GitHub Copilot docs)\n"
        "b) Language-specific documentation (e.g. Python docs)\n"
        "c) Mode-specific documentation (e.g. inline chat docs)\n"
        "2. Other Resources (score based on):\n"
        "   - Recency of the source\n"
        "   - Authority of the source\n"
        "   - Direct relevance to our specific use case\n"
        "   - Practical value for developers\n\n"
        "Return a JSON object with two arrays:\n"
        "1. 'official_resources': Array of 2-4 best official documentation URLs, each containing:\n"
        "   - url: The documentation URL\n"
        "   - title: Clear title describing the resource\n"
        "   - type: One of ['tool', 'language', 'mode']\n"
        "   - section: Specific section of docs if applicable\n"
        "2. 'citations': Array of other relevant citations with scores >= 0.7\n"
        "Each citation should include url, title, and relevance_score fields."
    )

    citation_messages = [
        {
            "role": "developer",
            "content": citation_scoring_prompt
        },
        {
            "role": "user",
            "content": (
                f"Score these citations for the use case:\n{use_case_content}\n\n"
                f"Citations:\n{json.dumps(research_data['citations'], indent=2)}"
            )
        }
    ]

    try:
        # Log the full prompt before execution
        log_prompt("3 - Citation Scoring", citation_messages)
        
        # First get the citations scored and categorized
        citation_response = openai_client.chat_completion_create(
            model="o3-mini-2025-01-31",
            reasoning_effort="low",
            messages=citation_messages,
        )
        scored_results = json.loads(citation_response.choices[0].message.content)
        
        # Extract official resources and other citations
        official_resources = scored_results.get('official_resources', [])
        other_citations = [c for c in scored_results.get('citations', []) 
                         if c.get('relevance_score', 0) >= 0.7]

        # Now proceed with the main refinement
        system_prompt = (
            "You are an AI assistant tasked with creating a comprehensive, structured use case by merging research findings "
            "with the original use case design. The output must be valid JSON following the 'UseCaseStructuredOutput' schema.\n\n"
            
            "CRITICAL INTEGRATION REQUIREMENTS:\n\n"
            "1. TECHNICAL ACCURACY:\n"
            "   - Preserve all specific tool versions, models, and technical details from the original config\n"
            "   - Maintain accuracy of any programming languages, frameworks, or platforms specified\n"
            "   - Ensure all technical prerequisites and dependencies are correctly represented\n\n"
            
            "2. CONFIGURATION FIDELITY:\n"
            "   - Retain and emphasize the specific AI tools and models mentioned (e.g., exact versions, capabilities)\n"
            "   - Preserve the intended complexity level and time estimates\n"
            "   - Maintain alignment with specified roles and departments\n"
            "   - Honor any mode-specific requirements (e.g., agentic, interactive)\n\n"
            
            "3. RESEARCH INTEGRATION:\n"
            "   - Incorporate relevant research findings while preserving config-specified constraints\n"
            "   - Validate that research aligns with specified tools and versions\n"
            "   - Ensure best practices are compatible with the configured environment\n\n"
            
            "4. CONTENT STRUCTURE:\n"
            "   - Each step must directly relate to the configured tools and environment\n"
            "   - Examples and code snippets must match specified language and tool versions\n"
            "   - Maintain traceability between steps and original requirements\n\n"
            
            "ADDITIONAL POLISH REQUIREMENTS:\n"
            "- Keep the example solution step intact and aligned with config specifications\n"
            "- Ensure steps are bullet-listed, time-bound, and guideline-compliant\n"
            "- Maintain conversational tone while preserving technical accuracy\n"
            "- Address the reader as 'you' while maintaining professional tone\n"
            "- Focus on tool-specific usage rather than fundamental concepts\n"
            "- Preserve all critical metadata from the original configuration\n\n"
            
            "OUTPUT REQUIREMENTS:\n"
            "- Must be valid JSON matching UseCaseStructuredOutput schema\n"
            "- All technical details must be accurate and config-aligned\n"
            "- Content must be immediately actionable and environment-ready\n\n"
            
            f"{BRAND_LANGUAGE_GUIDELINES}\n\n"
            f"{USE_CASE_GUIDELINES}"
        )

        messages = [
            {
                "role": "developer",
                "content": system_prompt
            },
            {
                "role": "assistant",
                "content": f"Research Findings:\n{research_data['content']}\n\nSelected Citations:\n{json.dumps(other_citations, indent=2)}"
            },
            {
                "role": "user",
                "content": (
                    "Please combine the research findings with this use case design to create "
                    "an end-to-end, structured use case. The use case must preserve all critical "
                    "configuration details while incorporating relevant research insights.\n\n"
                    "Return valid JSON adhering to the Pydantic schema:\n\n"
                    "UseCaseStructuredOutput:\n\n"
                    f"{use_case_content}"
                )
            }
        ]

        # Log the full prompt before execution
        log_prompt("3 - Refine Use Case", messages)

        completion = openai_client.chat_completion_parse(
            model="o3-mini-2025-01-31",
            reasoning_effort="high",
            messages=messages,
            response_format=UseCaseStructuredOutput,  # Our Pydantic model
        )

        parsed_message = completion.choices[0].message
        if parsed_message.refusal:
            structured_dict = {
                "title": "Refusal",
                "time_to_complete": "0 minutes",
                "description": "The model refused to comply.",
                "steps": [],
                "resources": official_resources,
                "metadata": USE_CASE_CONFIG,
                "citations": []
            }
        else:
            structured_obj = parsed_message.parsed
            structured_dict = structured_obj.model_dump()
            # Always attach original config as metadata
            structured_dict["metadata"] = USE_CASE_CONFIG
            # Add our official resources and other citations
            structured_dict["resources"] = official_resources
            structured_dict["citations"] = other_citations

        refined_draft_json = json.dumps(structured_dict, indent=2)

        log_ai_interaction(
            "3 - Refine Use Case",
            messages[-1]["content"],
            refined_draft_json
        )

        save_partial_result(job_manager, step_name, refined_draft_json)
        return refined_draft_json

    except Exception as e:
        print(f"ERROR in Step 3 (Refining Use Case): {e}")
        raise

# -------------------------------------------------------------------------------------
# STEP 4: FINAL POLISH WITH OPENAI CHAT (Structured)
# -------------------------------------------------------------------------------------
def finalize_use_case(openai_client, refined_json, job_manager: JobManager):
    """
    Pass the Step 3 structured JSON to the chat model for final polish,
    returning final structured JSON (UseCaseStructuredOutput).

    The entire final result is stored as JSON in partial results.
    """
    step_name = "final_use_case"
    existing_content = load_partial_result(job_manager, step_name)
    if existing_content:
        print("[Resume] Found existing final output.")
        return existing_content

    system_prompt = (
        "You are an AI writing assistant focused on improving prose clarity and readability while strictly preserving "
        "technical accuracy and meaning. You are given a valid JSON object conforming to the 'UseCaseStructuredOutput' schema.\n\n"
        
        "CRITICAL PRESERVATION REQUIREMENTS:\n"
        "1. Technical Fidelity:\n"
        "   - Never alter technical specifications or requirements\n"
        "   - Preserve all tool names, versions, and capabilities exactly\n"
        "   - Maintain all configuration details precisely\n"
        "   - Keep all code snippets and technical steps intact\n\n"
        
        "2. Structural Integrity:\n"
        "   - Maintain exact step ordering and dependencies\n"
        "   - Preserve all metadata and configuration values\n"
        "   - Keep all field names and schema structure unchanged\n"
        "   - Retain all technical prerequisites and requirements\n\n"
        
        "PROSE IMPROVEMENT FOCUS:\n"
        "1. Readability Enhancements:\n"
        "   - Align with 8th-grade reading level\n"
        "   - Use active voice consistently\n"
        "   - Break down complex sentences\n"
        "   - Clarify technical concepts without oversimplifying\n\n"
        
        "2. Style Refinements:\n"
        "   - Maintain professional but conversational tone\n"
        "   - Address the reader as 'you'\n"
        "   - Use consistent terminology throughout\n"
        "   - Ensure clear transitions between steps\n\n"
        
        "3. Format Polish:\n"
        "   - Structure content in bullet-list style where appropriate\n"
        "   - Add time estimates to steps when missing\n"
        "   - Ensure proper paragraph breaks\n"
        "   - Maintain consistent formatting\n\n"
        
        "BOUNDARIES OF MODIFICATION:\n"
        "✓ DO:\n"
        "  - Improve sentence structure and flow\n"
        "  - Enhance clarity of explanations\n"
        "  - Fix grammatical issues\n"
        "  - Standardize formatting\n\n"
        
        "✗ DO NOT:\n"
        "  - Change technical requirements or specifications\n"
        "  - Alter tool names, versions, or capabilities\n"
        "  - Modify step ordering or dependencies\n"
        "  - Remove or add technical content\n\n"
        
        "OUTPUT REQUIREMENTS:\n"
        "- Must return valid JSON matching UseCaseStructuredOutput schema\n"
        "- All technical details must remain unchanged\n"
        "- Only prose and formatting improvements allowed\n\n"
        
        f"{BRAND_LANGUAGE_GUIDELINES}\n\n"
        f"{USE_CASE_GUIDELINES}"
    )

    messages = [
        {
            "role": "developer",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": (
                "Polish the prose and formatting of this use case while strictly preserving all technical content, "
                "meaning, and configuration details. Focus only on improving readability and clarity.\n\n"
                f"{refined_json}"
            )
        }
    ]

    try:
        # Log the full prompt before execution
        log_prompt("4 - Final Polish", messages)
        
        completion = openai_client.chat_completion_parse(
            model="gpt-4o",
            messages=messages,
            response_format=UseCaseStructuredOutput,  # same schema
        )

        parsed_message = completion.choices[0].message
        if parsed_message.refusal:
            final_struct = {
                "title": "Refusal",
                "time_to_complete": "0 minutes",
                "description": "The model refused to comply.",
                "steps": [],
                "resources": [],
                "metadata": USE_CASE_CONFIG
            }
        else:
            final_struct = parsed_message.parsed.model_dump()
            # Always attach original config as metadata
            final_struct["metadata"] = USE_CASE_CONFIG

        final_json = json.dumps(final_struct, indent=2)

        log_ai_interaction(
            "4 - Final Polish",
            messages[-1]["content"],
            final_json
        )
        save_partial_result(job_manager, step_name, final_json)
        return final_json

    except Exception as e:
        print(f"ERROR in Step 4 (Final Polish): {e}")
        raise

# -------------------------------------------------------------------------------------
# STEP 5: EXAMPLE SOLUTION GENERATION
# -------------------------------------------------------------------------------------
def generate_example_solution(
    openai_client: OpenAI,
    use_case_config: dict,
    polished_content: str,
    raw_research: dict,
    job_manager: JobManager
) -> str:
    """
    Generate a complete example solution for the use case.
    
    Args:
        openai_client: OpenAI client instance
        use_case_config: Original use case configuration
        polished_content: Final polished use case content
        raw_research: Raw research results from step 2
        job_manager: JobManager instance for partial results
    
    Returns:
        JSON string containing the example solution
    """
    step_name = "example_solution"
    existing_content = load_partial_result(job_manager, step_name)
    if existing_content:
        print("[Resume] Found existing example solution...")
        return existing_content

    # Extract key fields for context
    is_generic = not all([
        use_case_config.get('coding_language'),
        use_case_config.get('tool'),
        use_case_config.get('role')
    ])

    # Extract steps from the polished use case content
    try:
        polished_data = json.loads(polished_content)
        use_case_steps = [step['step_title'] for step in polished_data.get('steps', [])]
    except (json.JSONDecodeError, KeyError):
        # Fallback to original use case steps if polished content parsing fails
        use_case_steps = use_case_config.get('steps', [])

    # Build the system prompt
    system_prompt = f"""You are an expert AI instructor creating a practical example solution for a software development use case.
The solution will be demonstrated in a 2-3 minute video by a subject matter expert.

CRITICAL CONFIGURATION DETAILS:
- Title: {use_case_config['title']}
- Family: {use_case_config['family']}
- Tool: {use_case_config.get('tool', 'Any AI coding assistant')}
- Language: {use_case_config.get('coding_language', 'Any')}
- Role: {use_case_config.get('role', 'Any')}
- Mode: {use_case_config.get('mode', 'Any')}
- Model: {use_case_config.get('model', 'Not specified')}

SOLUTION REQUIREMENTS:

1. TECHNICAL PRECISION:
   - Use exact tool versions and models specified in config
   - Follow language-specific best practices when specified
   - Maintain compatibility with configured environment
   - Include all necessary setup and prerequisites

2. TIME AND SCOPE MANAGEMENT:
   - Solution must be demonstrable in 2-3 minutes
   - Setup time should be realistic and clearly stated
   - Each step should have clear time expectations
   - Complex steps should be broken down appropriately

3. TOOL AND MODEL SPECIFICITY:
   {'- Provide tool/language agnostic examples with clear alternatives' if is_generic else '- Use specified tool and language exclusively'}
   - Leverage unique features of configured tools/models
   - Include version-specific capabilities and syntax
   - Document any version-dependent behavior

4. VALIDATION AND QUALITY:
   - Include explicit validation steps
   - Address common pitfalls specific to chosen tools
   - Provide error handling appropriate to config
   - Ensure reproducibility in specified environment

5. STEP ALIGNMENT:
   - Each solution step must map directly to these use case steps:
{json.dumps(use_case_steps, indent=2)}
   - Maintain consistent terminology with use case
   - Preserve step ordering and dependencies
   - Include transition guidance between steps

OUTPUT STRUCTURE:
1. Must be valid JSON matching ExampleSolutionOutput schema
2. All steps must include:
   - Clear action description
   - Concrete code or prompt examples
   - Expected outcome
3. Demo script must:
   - Reference specific tools and versions
   - Include setup requirements
   - Highlight key technical details
   - Address common issues

BRAND GUIDELINES:
{BRAND_LANGUAGE_GUIDELINES}"""

    # Build the user prompt with research context
    user_prompt = f"""Generate a complete example solution that rigorously follows the configuration specifications:

USE CASE CONTENT:
{polished_content}

RESEARCH FINDINGS:
{raw_research.get('content', '')}

CRITICAL REQUIREMENTS:
1. Solution must be immediately actionable in the configured environment
2. All examples must use exact versions and syntax for specified tools
3. Each step must demonstrate clear value while maintaining technical precision
4. Code and prompts must be production-ready and fully validated

SCHEMA REQUIREMENTS:
- All fields in ExampleSolutionOutput are required
- Each step needs both 'action' and 'code_or_prompt' fields
- Variations list must exist (can be empty for specific configurations)
- Demo script must be a clear 2-3 minute technical walkthrough
- Steps must align exactly with use case steps:
{json.dumps(use_case_steps, indent=2)}

Focus on creating a solution that:
1. Maximizes the capabilities of specified tools and versions
2. Demonstrates best practices for the configured environment
3. Provides clear validation and error handling
4. Can be reproduced exactly as shown"""

    try:
        # Log the full prompt before execution
        log_prompt("5 - Example Solution Generation", [
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        # Generate the structured solution
        completion = openai_client.chat_completion_parse(
            model="o3-mini-2025-01-31",
            reasoning_effort="high",
            messages=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=ExampleSolutionOutput
        )

        # Extract the solution
        solution = completion.choices[0].message.parsed
        
        # Validate that the number of steps matches
        if len(solution.solution.steps) != len(use_case_steps):
            print(f"Warning: Generated solution has {len(solution.solution.steps)} steps but use case has {len(use_case_steps)} steps")
        
        solution_json = json.dumps(solution.model_dump(), indent=2)

        log_ai_interaction(
            "5 - Example Solution Generation",
            user_prompt,
            solution_json
        )

        save_partial_result(job_manager, step_name, solution_json)
        return solution_json

    except Exception as e:
        print(f"ERROR in Step 5 (Example Solution): {e}")
        raise

# -------------------------------------------------------------------------------------
# STEP 6: SUGGEST VISUAL ELEMENTS (NEW)
# -------------------------------------------------------------------------------------
def suggest_visual_elements(
    openai_client: OpenAI,
    final_use_case_json: str,
    example_solution_json: str,
    job_manager: JobManager
) -> str:
    """
    Takes the output from step 5 (example solution) and the final use case,
    and makes SPECIFIC suggestions about which visual elements (screenshots,
    GIFs, code snippets, etc.) might add value to the main body of the use case.
    Ensures alignment with the subject matter.
    """
    step_name = "visual_suggestions"
    existing_content = load_partial_result(job_manager, step_name)
    if existing_content:
        print("[Resume] Found existing visual suggestions...")
        return existing_content

    system_prompt = (
        "You are an instructional designer creating visual element suggestions for a software development use case. "
        "Your goal is to propose specific visual aids that enhance understanding while maintaining technical accuracy.\n\n"
        
        "VISUAL ELEMENT GUIDELINES:\n"
        "1. Tool-Specific Visualization:\n"
        "   - Focus on interface elements unique to specified tools\n"
        "   - Capture version-specific features when relevant\n"
        "   - Show actual tool interactions and outputs\n\n"
        
        "2. Technical Accuracy:\n"
        "   - All code snippets must match specified language and versions\n"
        "   - Screenshots should reflect current tool interfaces\n"
        "   - Diagrams must align with documented workflows\n\n"
        
        "3. Educational Value:\n"
        "   - Each visual must serve a clear learning purpose\n"
        "   - Complex concepts should be broken down visually\n"
        "   - Key steps should have supporting visuals\n\n"
        
        "CRITICAL REQUIREMENTS:\n"
        "- All suggestions must align with the subject matter and steps\n"
        "- Visual elements must be reproducible in the specified environment\n"
        "- Focus on practical, high-impact visualizations\n\n"
        
        f"{BRAND_LANGUAGE_GUIDELINES}\n"
    )

    user_prompt = f"""Review the use case and example solution to suggest visual elements that enhance learning and comprehension.
Focus particularly on visualizing tool-specific interactions and technical concepts.

Final Use Case JSON:
{final_use_case_json}

Example Solution JSON:
{example_solution_json}

For each suggested visual element (3-5 total), provide:
1. Specific description of what to capture
2. Technical requirements (tools, versions, settings)
3. Clear explanation of educational value
4. Step or concept it supports
5. Format recommendation (screenshot, GIF, diagram, etc.)

Ensure all suggestions:
- Match the specified tool versions and environments
- Support key learning objectives
- Can be easily reproduced
- Add genuine educational value
"""

    try:
        # Log the full prompt before execution
        log_prompt("6 - Visual Elements Suggestions", [
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        response = openai_client.chat_completion_create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )
        suggestions = response.choices[0].message.content.strip()

        # Log, store, and return suggestions
        log_ai_interaction("6 - Visual Elements Suggestions", user_prompt, suggestions)
        save_partial_result(job_manager, step_name, suggestions)

        return suggestions

    except Exception as e:
        print(f"ERROR in Step 6 (Suggest Visual Elements): {e}")
        raise

# Update main to handle async
def main():
    """Main orchestrator function."""
    # Add argument parsing
    parser = argparse.ArgumentParser(description='Generate a use case document')
    parser.add_argument('--title', help='Use case title')
    parser.add_argument('--family', help='Use case family')
    parser.add_argument('--ai_tool', help='AI tool name')
    parser.add_argument('--objective', help='Use case objective')
    parser.add_argument('--description', help='Use case description')
    parser.add_argument('--prerequisites', help='Comma-separated list of prerequisites')
    parser.add_argument('--time_estimate', help='Time estimate')
    parser.add_argument('--steps', help='Comma-separated list of steps')
    parser.add_argument('--tool', help='Tool name')
    parser.add_argument('--department', help='Comma-separated list of departments')
    parser.add_argument('--role', help='Comma-separated list of roles')
    parser.add_argument('--mode', help='Mode')
    parser.add_argument('--model', help='Model')
    parser.add_argument('--coding_language', help='Coding language')
    
    args = parser.parse_args()
    
    # Get configuration from arguments or defaults
    global USE_CASE_CONFIG
    USE_CASE_CONFIG = get_use_case_config(args)
    
    try:
        validate_environment()  # Add environment validation
        
        # Initialize
        job_manager = JobManager(USE_CASE_CONFIG["title"])
        job_manager.save_metadata(USE_CASE_CONFIG)
        logging.info("\n🚀 Starting use case generation for: %s", USE_CASE_CONFIG["title"])
        logging.info("Job ID: %s", job_manager.job_id)
        logging.debug("Full configuration: %s", json.dumps(USE_CASE_CONFIG, indent=2))
        
        # Track success of each step
        step_results = {}
        
        try:
            # Step 1: Format and identify research questions
            logging.info("\n📋 Step 1/6: Identifying research questions...")
            use_case_content = format_use_case_content()
            questions_to_ask = identify_research_questions(openai_client, use_case_content, job_manager)
            logging.debug("Generated questions:\n%s", "\n".join(f"- {q}" for q in questions_to_ask))
            logging.info("✓ Research questions identified")
            step_results['research_questions'] = True
        except Exception as e:
            questions_to_ask = job_manager.handle_step_failure("research_questions", e)
            if not questions_to_ask:
                raise
            step_results['research_questions'] = False
        
        try:
            # Step 2: Research (async)
            logging.info("\n🔍 Step 2/6: Conducting deep research...")
            deep_research_results = asyncio.run(deep_research(
                perplexity_client, 
                use_case_content, 
                questions_to_ask, 
                job_manager
            ))
            logging.info("✓ Research completed")
            logging.debug("Research results: %s", json.dumps(deep_research_results, indent=2))
            step_results['deep_research'] = True
        except Exception as e:
            deep_research_results = job_manager.handle_step_failure("deep_research", e)
            if not deep_research_results:
                raise
            step_results['deep_research'] = False
        
        try:
            # Step 3: Refine with reasoning
            logging.info("\n🔄 Step 3/6: Refining use case with research findings...")
            refined_draft_json = refine_use_case_with_reasoning(
                openai_client,
                raw_research=deep_research_results,
                use_case_content=use_case_content,
                job_manager=job_manager
            )
            logging.info("✓ Initial refinement complete")
            step_results['refined_draft'] = True
        except Exception as e:
            refined_draft_json = job_manager.handle_step_failure("refined_draft", e)
            if not refined_draft_json:
                raise
            step_results['refined_draft'] = False
        
        try:
            # Step 4: Final polish
            logging.info("\n✨ Step 4/6: Applying final polish...")
            final_use_case_json = finalize_use_case(
                openai_client, 
                refined_draft_json, 
                job_manager
            )
            logging.info("✓ Polish complete")
            step_results['final_use_case'] = True
        except Exception as e:
            final_use_case_json = job_manager.handle_step_failure("final_use_case", e)
            if not final_use_case_json:
                raise
            step_results['final_use_case'] = False
        
        try:
            # Step 5: Example solution
            logging.info("\n📝 Step 5/6: Generating example solution...")
            example_solution_json = generate_example_solution(
                openai_client,
                USE_CASE_CONFIG,
                final_use_case_json,
                deep_research_results,
                job_manager
            )
            logging.info("✓ Example solution generated")
            step_results['example_solution'] = True
        except Exception as e:
            example_solution_json = job_manager.handle_step_failure("example_solution", e)
            if not example_solution_json:
                raise
            step_results['example_solution'] = False
        
        try:
            # Step 6: Visual suggestions
            logging.info("\n🎨 Step 6/6: Creating visual element suggestions...")
            visual_suggestions = suggest_visual_elements(
                openai_client,
                final_use_case_json,
                example_solution_json,
                job_manager
            )
            logging.info("✓ Visual suggestions created")
            step_results['visual_suggestions'] = True
        except Exception as e:
            visual_suggestions = job_manager.handle_step_failure("visual_suggestions", e)
            if not visual_suggestions:
                raise
            step_results['visual_suggestions'] = False
        
        # Convert to markdown and write file
        logging.info("\n📄 Generating final markdown document...")
        markdown_content = convert_json_to_markdown(
            final_use_case_json, 
            example_solution_json,
            visual_suggestions
        )
        write_markdown_file(
            markdown_content, 
            USE_CASE_CONFIG['title'],
            job_manager
        )
        
        # Log completion status
        failed_steps = [step for step, success in step_results.items() if not success]
        if failed_steps:
            logging.warning(
                "\n⚠️ Use case generated with partial results. Failed steps: %s", 
                ", ".join(failed_steps)
            )
        else:
            logging.info("\n✅ Use case generation complete!")
        
        logging.info("📁 Results stored in: %s", job_manager.job_dir)
        logging.debug("Job completed with status: %s", json.dumps(step_results, indent=2))
        
    except Exception as err:
        logging.error("❌ Error during use case generation: %s", err)
        raise

if __name__ == "__main__":
    main()
