# Use Case Generator Workflow

This repository supports two methods for generating use cases: via GitHub Issues (recommended) or through the manual workflow process.

## Method 1: GitHub Issues (Recommended)

The preferred way to submit new use cases is through GitHub Issues:

1. Go to the "Issues" tab in GitHub
2. Click "New Issue"
3. Select the "Use Case Submission" template
4. Fill out all the required fields in the template:
   - Title: Clear, descriptive title for your use case
   - Family: Select from the dropdown list of categories
   - AI Tool: Primary AI tool being used
   - Objective: One-sentence goal statement
   - Description: Detailed explanation (2-3 paragraphs)
   - Prerequisites: Required skills (comma-separated)
   - Time Estimate: Expected completion time (10-30 minutes)
   - Steps: Main steps (comma-separated)
   - Tool: Specific tool name
   - Department: Target department
   - Role: Target role
   - Mode: Mode of operation
   - Model: AI model to use
   - Coding Language: Primary programming language
5. Click "Submit new issue"

The issue will automatically trigger the use case generation workflow.

## Method 2: Manual Workflow (Legacy)

The original workflow method remains available for advanced users or special cases:

1. Copy the contents of `use_case_template.json`
2. Go to the "Actions" tab in GitHub
3. Select "Generate Use Case" workflow
4. Click "Run workflow"
5. Paste your modified JSON into the `config_json` input field
6. Click "Run workflow"

## JSON Configuration Fields

```json
{
  "title": "...",              // Clear, descriptive title
  "family": "Core Skills",     // Category (Core Skills, LLM API Fundamentals, etc.)
  "ai_tool": "...",           // Primary AI tool being used
  "objective": "...",         // One-sentence goal statement
  "description": "...",       // Detailed explanation (2-3 paragraphs)
  "prerequisites": "...",     // Comma-separated list of required skills
  "time_estimate": "...",     // Expected completion time (e.g., "20 minutes")
  "steps": "...",            // Comma-separated list of main steps
  "tool": "...",             // Specific tool name (e.g., "GitHub Copilot")
  "department": "...",       // Target department (e.g., "SWE")
  "role": "...",            // Target role (e.g., "front-end")
  "mode": "...",            // Mode of operation (e.g., "inline chat")
  "model": "...",           // AI model to use (e.g., "GPT-4o")
  "coding_language": "..."  // Primary programming language
}
```

## Example

```json
{
    "title": "Craft Effective Code Prompts for AI Assistance",
    "family": "Core Skills",
    "ai_tool": "Coding Assistants",
    "objective": "Enable developers to effectively communicate programming intent through structured comments that trigger accurate AI code generation",
    "description": """This use case trains developers to harness AI tooling by writing precise comments and docstrings that function as prompts for automated code generation. It emphasizes the importance of natural language clarity in directives (e.g., docstrings and TODOs) and guides participants to refine prompts as needed while validating AI-generated outputs against the original intent.""",
    "prerequisites": "Writing clear code comments, Understanding code structure, Basic algorithmic thinking, Familiarity with code completion tools, Basic understanding of natural language processing",
    "time_estimate": "20 minutes",
    "steps": "Write a detailed function description in docstring format, Add TODO comments with specific algorithm requirements, Use natural language to describe complex logic before implementation, Refine prompts based on initial AI outputs, Validate generated code against original intent",
    "tool": "GitHub Copilot",
    "department": "SWE",
    "role": "front-end",
    "mode": "inline chat",
    "model": "GPT-4o",
    "coding_language": "Python"
}
```

## Available Categories

Our use cases are organized into the following families:

- Core Skills
  - Fundamental skills for working with AI coding tools
- LLM API Fundamentals
  - Working with AI APIs and prompt engineering
- Challenges of Unstructured LLM Output
  - Parsing and managing AI-generated text
- Tool Use & API Integrations with LLMs
  - Integrating AI with external tools and services
- Retrieval-Augmented Generation (RAG) and Memory
  - Enhancing AI responses with context and memory
- AI Agent Workflows and Architecture
  - Building autonomous AI systems
- Fine-Tuning LLMs for Custom Use Cases
  - Customizing AI models for specific needs
- Deploying AI Applications
  - MLOps, containers, and cloud deployment
- AI Observability & Logging
  - Monitoring LLM behavior in production
- Testing & Evaluating AI Systems
  - Best practices for testing AI applications
- Security & Governance for AI Applications
  - Safe and ethical AI deployment

## Example Use Case

Here's an example of a well-structured use case:

```json
{
    "title": "Generate Unit Tests with AI Assistance",
    "family": "Testing & Quality Assurance",
    "ai_tool": "Coding Assistants",
    "objective": "Learn to use AI to generate comprehensive unit tests for your code",
    "description": "This use case demonstrates how to leverage AI coding assistants to generate effective unit tests. You'll learn to provide the right context and requirements to ensure thorough test coverage.",
    "prerequisites": "Basic testing concepts,Python or JavaScript knowledge,Understanding of unit testing principles",
    "time_estimate": "25 minutes",
    "steps": "Select code to test,Describe test requirements,Generate initial tests,Review and refine coverage,Validate test quality",
    "tool": "GitHub Copilot",
    "department": "SWE",
    "role": "back-end",
    "mode": "inline chat",
    "model": "GPT-4o",
    "coding_language": "Python"
}
```

## Notes

- All fields are required in both submission methods
- Use commas to separate items in lists (prerequisites, steps, etc.)
- Keep descriptions clear and concise
- Follow the 8th-grade reading level guideline
- Ensure steps are achievable within the time estimate (10-30 minutes)
- When using the issue template, follow the field-specific guidance provided in the template 