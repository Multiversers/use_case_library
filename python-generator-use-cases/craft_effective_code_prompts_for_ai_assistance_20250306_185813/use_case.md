# Craft Effective Code Prompts for AI Assistance

**Time to Complete:** 20 minutes

## Description
This use case guides you on how to use AI tools by writing precise comments and docstrings that serve as effective prompts for automated code generation. By following research-backed guidelines, you will learn to create clear, detailed function descriptions and specific TODO comments to express your algorithmic intent. This process highlights the importance of natural language clarity, iterative prompt refinement, and validating AI-generated outputs to ensure they match your original intent.

## Steps
### Step 1: Write detailed function docstring
Compose a comprehensive docstring that explains the function's purpose, parameters, return values, and usage examples. Ensure your description is clear and concise to guide the AI effectively.

1. **Clear function purpose**
   Begin with a high-level overview of what the function does.
   - Provide a concise summary.
   - State the main responsibility of the function.

2. **Parameter details**
   List each parameter with its type, acceptable range, and purpose.
   - Include default values if applicable.
   - Clarify expected input for each parameter.

3. **Return values**
   Describe the format and type of the value returned by the function.
   - Indicate any special cases or edge conditions.
   - Provide clarity on the expected output.

Ensure that your docstring adheres to common documentation conventions and serves as a clear prompt for AI code generation.

### Step 2: Add specific TODO comments
Insert inline TODO comments that outline specific algorithmic requirements and constraints. Use clear language to define the tasks that need to be completed.

1. **Specific action items**
   Detail what needs to be implemented with clear and actionable instructions.
   - List precise tasks to be completed.
   - Avoid vague descriptions.

2. **Context and constraints**
   Provide background information and mention any constraints related to the algorithm.
   - Include performance or error handling requirements.
   - Reference relevant documentation if necessary.

Detailed TODO comments guide the AI to generate code that meets your original specifications.

### Step 3: Describe complex logic in natural language
Before implementation, write out the logic behind complex parts in plain language to ensure that the AI understands the intended approach.

1. **Break down the logic**
   Outline the sequential steps of the algorithm in simple language.
   - Explain the reasoning behind each step.
   - Detail expected behavior and edge cases.

This approach enhances AI understanding and leads to more accurate code generation for complex tasks.

### Step 4: Refine your prompts based on initial output
Review the AI-generated code and adjust your prompts by adding more details or clarifications to address any shortcomings.

1. **Review initial output**
   Analyze the first version of the generated code to spot any misalignments with your intended functionality.
   - Identify missing features or discrepancies.
   - Note areas that require more detail.

2. **Iterative improvement**
   Modify your prompts and comments based on the review to refine the generated output.
   - Incorporate targeted feedback into your comments.
   - Focus on specific aspects that need clarification.

Iterative refinement of your prompts greatly enhances the accuracy and quality of the AI-generated code.

### Step 5: Validate the generated code
Test and review the AI-generated code to ensure it meets the functional, quality, and performance requirements.

1. **Conduct code review**
   Manually review the code for correctness, readability, and adherence to coding standards.
   - Inspect for any errors or oversights.
   - Ensure the documentation is complete.

2. **Perform testing**
   Develop and run test cases to verify that the code works as expected under various scenarios.
   - Use unit tests and integration tests.
   - Evaluate performance and edge case handling.

Thorough validation through review and testing ensures that the AI-generated code aligns perfectly with your original intent.

## Resources
### Tool Documentation
* [Official Resource](https://docs.github.com/en/copilot/using-github-copilot/best-practices-for-using-github-copilot)
* [Official Resource](https://docs.github.com/en/copilot/using-github-copilot/copilot-chat/prompt-engineering-for-copilot-chat)
* [Official Resource](https://github.blog/developer-skills/github/how-to-write-better-prompts-for-github-copilot/)

## Additional References
* [A Guide to Crafting Effective Prompts for Diverse Applications - OpenAI Developer Community](https://community.openai.com/t/a-guide-to-crafting-effective-prompts-for-diverse-applications/493914)
* [Effective Prompts for AI: The Essentials - MIT Sloan Teaching & Learning Technologies](https://mitsloanedtech.mit.edu/ai/basics/effective-prompts/)
* [How to write better AI prompts - LeadDev](https://leaddev.com/velocity/how-write-better-ai-prompts)
* [Expert’s Guide: Generative AI Prompts for Maximum Efficiency](https://hatchworks.com/blog/gen-ai/generative-ai-prompt-guide/)
* [AI Prompting Best Practices | Codecademy](https://www.codecademy.com/article/ai-prompting-best-practices)
* [Getting started with prompts for text-based Generative AI tools | Harvard University Information Technology](https://www.huit.harvard.edu/news/ai-prompts)
* [Comments and Documentation in Python | CodeSignal Learn](https://codesignal.com/learn/courses/clean-code-basics-with-python/lessons/comments-and-documentation-in-python)
* [GenAIScript - Comment Code with AI - DEV Community](https://dev.to/bsorrentino/genaiscript-comment-code-with-ai-509f)
* [AI Code Generation Benefits & Risks | Sonar](https://www.sonarsource.com/learn/ai-code-generation-benefits-risks/)
* [Validating AI-Generated Code with Live Programming - YouTube](https://www.youtube.com/watch?v=aviT9zbqF5o)

## Example Solution: Craft Effective Code Prompts for AI Assistance

**Setup Time:** 3 minutes  
**Demo Time:** 3 minutes

### Scenario
A front-end developer utilizes GitHub Copilot in inline chat mode powered by GPT-4o to iteratively generate and improve Python code. The developer writes detailed docstrings, adds specific TODO comments, clearly explains complex logic in plain language, refines prompts based on initial outputs, and validates the final code through testing.

### Prerequisites
* Writing clear code comments
* Understanding code structure
* Basic algorithmic thinking
* Familiarity with code completion tools
* Basic understanding of natural language processing

### Demo Steps
1. **Write detailed function docstring: Compose a comprehensive Python function docstring that details the function's purpose, parameters, return values, and usage examples to guide the AI.**
```
def calculate_discounted_price(price, discount):
    """
    Calculate the final price after applying a discount.

    Parameters:
        price (float): The original price of the item. Must be non-negative.
        discount (float): Discount rate as a float between 0 and 1 (e.g., 0.20 for 20% discount).

    Returns:
        float: Final price after discount. Returns 0 if discount is 1.

    Example:
        >>> calculate_discounted_price(100.0, 0.2)
        80.0
    """
    return price * (1 - discount)
```
2. **Add specific TODO comments: Insert inline TODO comments that clearly outline specific algorithmic tasks and constraints.**
```
def fetch_user_data(user_id: int) -> dict:
    """Fetch user data from the database using a unique user ID."""
    # TODO: Establish a secure connection to the user database
    # TODO: Execute an SQL query to retrieve user details
    # TODO: Implement error handling for connection timeouts and query failures
    # TODO: Validate the format of the returned data
    return {}
```
3. **Describe complex logic in natural language: Explain the detailed logic behind a function in plain language to ensure clarity before implementation.**
```
def sort_numbers(numbers: list) -> list:
    """Sort a list of numbers using the merge sort algorithm."""
    # The merge sort algorithm works as follows:
    # 1. If the list has zero or one element, it is already sorted.
    # 2. Divide the list into two nearly equal halves.
    # 3. Recursively sort each half.
    # 4. Merge the two sorted halves by comparing the smallest elements from each.
    # 5. Return the fully merged and sorted list.
    if len(numbers) <= 1:
        return numbers
    mid = len(numbers) // 2
    left = sort_numbers(numbers[:mid])
    right = sort_numbers(numbers[mid:])
    sorted_list = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list
```
4. **Refine your prompts based on initial output: Review the AI-generated code and adjust your prompts with added clarifications for error handling and edge cases.**
```
# Initial review of the fetch_user_data function revealed missing input validation and error handling for invalid user IDs.
# Refined prompt for GitHub Copilot:
"@copilot, update the fetch_user_data function to include validation that the user_id is a positive integer and add try-except blocks to handle potential database errors."
```
5. **Validate the generated code: Test and review the code to ensure it meets functional requirements and handles edge cases appropriately.**
```
if __name__ == '__main__':
    # Validate calculate_discounted_price function
    result = calculate_discounted_price(100.0, 0.2)
    print('Discounted Price:', result)  # Expected output: 80.0

    # Validate sort_numbers function
    test_numbers = [34, 7, 23, 32, 5, 62]
    sorted_numbers = sort_numbers(test_numbers)
    print('Sorted Numbers:', sorted_numbers)  # Expected sorted list: [5, 7, 23, 32, 34, 62]

    # Further testing and manual code review should be performed to ensure all edge cases and error handling are in place.
```

### Validation
* Run the main block to verify the expected outputs for each function.
* Inspect inline comments and TODO items to confirm they guide the AI effectively.
* Verify that GitHub Copilot's refined suggestions address initial shortcomings.
* Conduct manual code reviews and run unit tests to cover error handling and edge cases.

### Key Teaching Points
* Craft clear and comprehensive docstrings as effective AI prompts.
* Include specific and actionable TODO comments.
* Describe complex logic in plain natural language.
* Iteratively refine prompts based on AI output feedback.
* Validate generated code through thorough testing and reviews.

### Common Issues to Watch For
* Ambiguous prompts may not capture all functional requirements.
* Overreliance on auto-generated code without manual validation.
* Insufficient error handling or unclear TODO instructions.
* Missing detailed inline explanations can reduce code clarity.

### Demo Script
Welcome to this demo on crafting effective code prompts for AI assistance using GitHub Copilot with GPT-4o. In this 2-3 minute walkthrough, you'll see how to start by writing a detailed function docstring that defines a function's purpose, parameters, and return values. Next, you'll add specific TODO comments that precisely outline each task and constraint. We'll then describe complex logic in plain language to guide the AI in generating robust code. After reviewing the initial output from Copilot, you'll refine your prompts to handle edge cases and improve error handling. Finally, you'll validate the generated code by running tests and reviewing the outputs to ensure everything meets your requirements. Follow along with the provided Python examples to reproduce this process in your own projects.

## Visual Elements
The following visual elements are recommended to enhance this use case:

Here are suggestions for visual elements to enhance learning and comprehension for the use case "Craft Effective Code Prompts for AI Assistance." These visuals focus on tool-specific interactions and technical concepts related to GitHub Copilot and Python programming.

### Visual Element 1: Docstring Composition 
1. **Specific description**: Capture a screenshot of the VS Code editor showing a detailed Python function docstring. Ensure the function includes purpose, parameters, return values, and an example.
2. **Technical requirements**: 
   - Tools: Visual Studio Code
   - Version: Latest version as of October 2023
   - Settings: Python extension enabled for syntax highlighting
3. **Educational value**: Demonstrates how to write comprehensive docstrings, which are crucial for guiding AI tools like GitHub Copilot.
4. **Supports**: Step 1 - "Write detailed function docstring."
5. **Format recommendation**: Screenshot 

### Visual Element 2: Creating TODO Comments
1. **Specific description**: Provide an animated GIF showing the process of adding inline TODO comments in a Python function to outline specific tasks.
2. **Technical requirements**: 
   - Tools: GitHub Copilot integrated with Visual Studio Code
   - Version: Copilot running with GPT-4o support
   - Settings: Inline chat mode enabled
3. **Educational value**: Visualizes how developers can use TODO comments to communicate algorithmic requirements and constraints effectively.
4. **Supports**: Step 2 - "Add specific TODO comments."
5. **Format recommendation**: GIF demonstrating dynamic interaction

### Visual Element 3: Natural Language Logic Description
1. **Specific description**: Diagram illustrating the steps of a complex algorithm (e.g., merge sort) along with plain language explanations.
2. **Technical requirements**: 
   - Tools: Lucidchart or similar diagramming tool
   - Version: Online or desktop version with Python code support options
   - Settings: Use simple graphics to ensure clarity
3. **Educational value**: Breaks down complex logic into understandable steps, facilitating better comprehension and AI guidance.
4. **Supports**: Step 3 - "Describe complex logic in natural language."
5. **Format recommendation**: Flowchart or step-by-step diagram

### Visual Element 4: Refining Prompts and Validating Outputs
1. **Specific description**: Create a split-view screenshot showing both initial AI-generated code and refined code after prompt adjustments in VS Code, highlighting changes with annotations.
2. **Technical requirements**: 
   - Tools: Visual Studio Code with GitHub Copilot enabled
   - Version: Fully updated as of October 2023
   - Settings: Use comparison or diff view if available
3. **Educational value**: Clearly shows the impact of refining prompts on the quality of AI-generated code, emphasizing the iterative improvement process.
4. **Supports**: Step 4 - "Refine your prompts based on initial output."
5. **Format recommendation**: Annotated comparison screenshot 

### Visual Element 5: Testing and Validating Code 
1. **Specific description**: A video screen capture showing the process of running unit tests in a terminal to validate the AI-generated Python code.
2. **Technical requirements**: 
   - Tools: Visual Studio Code, Python's unittest framework
   - Version: Use Python 3.8 or later
   - Settings: Terminal panel open within the IDE
3. **Educational value**: Demonstrates the importance of testing AI-generated code to ensure it meets functional requirements and handles edge cases properly.
4. **Supports**: Step 5 - "Validate the generated code."
5. **Format recommendation**: Short video recording

These visual aids align with the use case guidelines, support learning objectives, and can be readily recreated in the specified environments. They provide both practical insights and enhance conceptual understanding for junior developers learning to use AI-assisted code generation tools like GitHub Copilot.

## Metadata
* **id:** CORE-02
* **title:** Craft Effective Code Prompts for AI Assistance
* **family:** Core Skills
* **ai_tool:** Coding Assistants
* **objective:** Enable developers to effectively communicate programming intent through structured comments that trigger accurate AI code generation
* **description:** This use case trains developers to harness AI tooling by writing precise comments and docstrings that function as prompts for automated code generation. It emphasizes the importance of natural language clarity in directives (e.g., docstrings and TODOs) and guides participants to refine prompts as needed while validating AI-generated outputs against the original intent.
* **prerequisites:** Writing clear code comments, Understanding code structure, Basic algorithmic thinking, Familiarity with code completion tools, Basic understanding of natural language processing
* **time_estimate:** 20 minutes
* **steps:** Write a detailed function description in docstring format, Add TODO comments with specific algorithm requirements, Use natural language to describe complex logic before implementation, Refine prompts based on initial AI outputs, Validate generated code against original intent
* **tool:** GitHub Copilot
* **department:** SWE
* **role:** front-end
* **mode:** inline chat
* **model:** GPT-4o
* **coding_language:** Python
