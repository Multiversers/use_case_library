# Creating MARP Slide Decks with Microsoft Copilot

Marp is a markdown presentation ecosystem that allows you to create beautiful slide decks using simple markdown syntax. It offers flexibility in styling and is easily integrated with tools like VS Code for live previews and exports to various formats like PDF and HTML. Using AI to generate MARP slides can significantly speed up the slide creation process by automating content generation and formatting, allowing you to focus on refining the presentation's message and style.

Here's a step-by-step tutorial on how to use Microsoft Copilot to create a slide deck with MARP:

**Step 1: Setting up Your Environment**

* **Microsoft Copilot Access:** Ensure you have access to Microsoft Copilot within an application like VS Code, GitHub, or a browser where it's available.
* **Markdown Editor:** You'll need a markdown editor. VS Code is highly recommended due to its extensions and integration capabilities.
* **Marp Extension (VS Code):**
    * If using VS Code, install the "Marp for VS Code" extension. This lets you preview your slides as you write.
    * Search for "Marp for VS Code" in the VS Code extensions marketplace and click "Install." [Here's a direct link](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode).

**Step 2: Creating the Markdown File and Prompting Copilot**

1.  **Create a New Markdown File:**
    * Open your markdown editor (VS Code).
    * Create a new file and save it with a `.md` extension (e.g., `marp_slides.md`).

2.  **Trigger Copilot:**
    * Depending on your Copilot setup, you might need to press a keyboard shortcut or use a command to activate it. In VS Code, Copilot often suggests completions as you type, or can be triggered by pressing `Ctrl + I`.
    * You can also access GitHub Copilot chat in the View menu in VS Code.

3.  **Prompt Copilot to create slides:**
    * Inside the markdown file or in the chat, type your prompt. This is where Copilot will understand and execute your request.
    * Your prompt:

    ```markdown
    Create a slide deck using MARP. Return the markdown in this markdown file. The slides will cover [add topic]. Start with an intro slide, then create a slide for each of the following subtopics: [add list of subtopics]. For each slide: [add additional instructions].
    ```
    * Copilot will process your prompt and generate the markdown for your slide deck directly into your file. This will include the MARP syntax. You may need to adjust your prompt to get the results in your desired format.

**Step 3: Previewing the Slides (VS Code with Marp Extension)**

1.  **Open the Preview:**
    * In VS Code, with the "Marp for VS Code" extension installed, you can preview your slides.
    * Click on the preview icon in the top right corner of your markdown file.
    * The preview window will show your slides as they will appear.
    * You can also copy and paste the contents of the markdown file into markdown viewer in your browser.

<p <img align="center" >
<img src="VSCodePreview.jpg" alt="Preview Icon" width="400" height="300" >
</p

**Step 4: Editing and Refining the Slides**

1.  **Review the Generated Content:**
    * Carefully read through the generated slides. Check for accuracy, clarity, and style.

2.  **Make Simple Edits:**
    * **Text Edits:**
        * Correct any typos or grammatical errors.
        * Adjust the wording for clarity or to better fit your presentation style.
        * Expand or shorten paragraphs as needed.
    * **Code Adjustments:**
        * Ensure code examples are accurate and relevant.
        * Add or modify comments to explain the code.
        * Change the language of the code blocks.
    * **MARP Syntax Changes:**
        * **Themes:** Change the theme by adding `theme: <theme_name>` to the top of the file. Example: `theme: uncover`.
        * **Slide Separators:** Make sure the slide seperators are correct (---).
        * **Image Insertion:** Insert images using standard markdown image syntax: `![Alt text](image_path.png)`.
        * **Font sizes:** Add `` to a slide, then define the class in the header of the markdown file. Example:
            ```markdown
            ---
            marp: true
            theme: uncover
            style: |
              .my-custom-font-size h1 {
                font-size: 50px;
              }
            ---
            ```
        * **Adding lists:** Use standard markdown list syntax.
        * **Adding bold or italics:** Use standard markdown bold and italics syntax.
    * **Adding additional slides:** Simply add `---` to create a new slide, and then add your content.
    * **Removing slides:** Delete the markdown content for the slide.

**Step 5: Exporting the Slides (VS Code with Marp Extension)**

1.  **Export Options:**
    * Right-click within the markdown file and select "Command Pallette".
    * Select "Marp: Export Slide Deck"
    * Choose the desired export format (e.g., PDF, HTML, PPTX).

2.  **Save the Exported File:**
    * Select the location to save the exported file.


**Example MARP Markdown Structure (Generated by Copilot):**

```markdown
---
marp: true
theme: uncover
---

# AI Coding Assistant Use Cases

---

## Introduction

AI coding assistants are revolutionizing software development by providing real-time assistance, code generation, and automation.

---

## 1. Code Completion

AI coding assistants can predict and suggest code completions, saving developers time and reducing errors.

```python
# Example Python code completion
def calculate_area(width, height):
    return width * height
```
## Solution Walkthrough

The video belows walks through the process to produce a MARP slide deck using and GitHub Copilot in VS Code. We suggest you take a similar approach when creating your own slides. Take a look! 

<p align="center">
  <video width="600" height="400" controls>
    <source src="Create a Slide Deck using MARP with GitHub Copilot.mp4" type="video/mp4">
  </video>
</p>

## Additional Resources

For more information on MARP and how to create stunning slide decks, check out the following resources:

* [MARP Official Documentation](https://marp.app/docs/)
* [MARP GitHub Repository](https://github.com/marp-team/marp)
* [MARP for VS Code Extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
* [MARP Themes and Customization](https://marp.app/customize)
* [MARP CLI Usage](https://marp.app/cli)