# Use Case Generator

This tool automates the process of enriching and polishing use cases through a sophisticated six-step AI workflow. It's designed for instructional designers who want to create high-quality, consistent learning materials without needing to code.

## Critical Configuration Inputs

Before running the generator, ensure you have the following configuration details ready:

### Required Fields
- `id`: Unique identifier (e.g., "CORE-02")
- `title`: Action-oriented title of the use case
- `family`: Skill category (e.g., "Core Skills", "LLM API Fundamentals")
- `ai_tool`: Primary AI tool being taught
- `objective`: Clear, measurable learning objective
- `description`: 2-3 sentence overview
- `prerequisites`: List of required skills/knowledge
- `time_estimate`: Expected completion time (10-30 minutes)
- `steps`: List of sequential steps to complete the use case

### Optional Fields
- `department`: Target department(s) (e.g., ["SWE", "DevOps"])
- `role`: Target role(s) (e.g., ["front-end", "back-end"])
- `mode`: Tool interaction mode (e.g., "inline chat", "agent")
- `model`: Specific AI model version
- `coding_language`: Required programming language (if applicable)

## Six-Step Generation Process

### 1. Research Question Identification
The generator first analyzes your use case to create focused research questions that will guide content enrichment. It uses OpenAI's reasoning model to:
- Extract key technical elements
- Identify areas needing additional context
- Generate 2-4 specific research queries

### 2. Deep Research
Using the Perplexity API, the system:
- Executes all research questions in parallel
- Gathers recent best practices and documentation
- Collects relevant code examples and tutorials
- Validates technical accuracy of specifications

### 3. Content Refinement
The OpenAI reasoning model then:
- Merges research findings with original content
- Ensures technical accuracy and completeness
- Maintains configuration fidelity
- Structures content according to guidelines

### 4. Final Polish
The content receives a final polish focusing on:
- 8th-grade reading level
- Active voice and clear language
- Consistent formatting
- Brand alignment
- Technical accuracy preservation

### 5. Example Solution Generation
Creates a practical demonstration including:
- Setup instructions
- 2-3 minute video-ready script
- Step-by-step implementation guide
- Validation steps and common pitfalls
- Tool-specific examples

### 6. Visual Element Suggestions
Recommends specific visual aids such as:
- Screenshots of tool interfaces
- Process diagrams
- Code snippet comparisons
- GIFs of key interactions

## Outputs

The generator produces several key outputs:

1. **Structured JSON**
   - Complete use case content
   - Example solution
   - Technical metadata

2. **Markdown Documentation**
   - Formatted use case content
   - Visual element recommendations
   - Implementation guide

3. **Job Directory**
   - Partial results from each step
   - Execution logs
   - Source materials

## Quality Standards

All generated content adheres to:
- Brand language guidelines
- Technical accuracy requirements
- 8th-grade reading level
- Active voice
- Bias-free language
- Chicago Manual of Style

## Usage

The generator requires:
1. API keys for OpenAI and Perplexity (stored in `.env`)
2. Complete configuration inputs
3. Any existing use case content

Output is stored in a job-specific directory with:
- Unique timestamp
- Execution logs
- Partial results
- Final deliverables

## Best Practices

1. **Configuration Completeness**
   - Provide all required fields
   - Be specific about tools and versions
   - Include clear prerequisites

2. **Content Quality**
   - Keep time estimates realistic (10-30 minutes)
   - Ensure steps are achievable
   - Include measurable outcomes

3. **Technical Accuracy**
   - Verify tool versions and capabilities
   - Test example solutions
   - Validate all prerequisites

4. **Brand Alignment**
   - Follow writing guidelines
   - Maintain consistent tone
   - Use appropriate terminology

## Error Handling

The generator includes robust error handling for:
- Missing configuration
- API failures
- Invalid content structure
- Character encoding issues

## Future Enhancements

Planned improvements include:
1. Automated validation of use case structure
2. Content generation pipelines
3. Integration with CI/CD
4. Batch processing capabilities
5. Enhanced error reporting
