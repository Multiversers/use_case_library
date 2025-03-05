# Generating unit tests using Cursor 
Quickly generate a comprehensive suite of unit tests for a basic function with Cursor. Complete this use case to save time and ensure better coverage of edge cases with automated test creation.

**Time to Complete:** 10-15 minutes per unit test


## Watch a demo

<video width="100%" controls>
  <source src="generate_unit_tests.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Steps

### 1. Open Source Code File
Open one of your project's source code files that contains a function you'd like to test:
- In Cursor, open a file that contains a function that you would like to write tests for
- Low complexity functions work best

#### Example Function
Here's our example function that formats a user's full name:

```javascript
/**
 * Formats a user's full name
 * @param {string} firstName - The user's first name
 * @param {string} lastName - The user's last name
 * @returns {string} The formatted full name
 */
export function formatFullName(firstName, lastName) {
  if (typeof firstName !== 'string' || typeof lastName !== 'string') {
    throw new Error('Both firstName and lastName must be strings');
  }

  firstName = firstName.trim();
  lastName = lastName.trim();

  if (firstName === '' && lastName === '') {
    return '';
  }

  if (firstName === '') {
    return lastName;
  }

  if (lastName === '') {
    return firstName;
  }

  return `${firstName} ${lastName}`;
}
```

### 2. Configure Cursor Settings
1. Toggle open the AI pane
2. Select the following settings:
   - Model: claude-3.7-sonnet-thinking
   - Mode: Chat/Composer
   - Context

![AI Pane](AI%20Pane.png)
![Models](Models.png)

#### Building Context
Ask Cursor to write a description of your function to serve as context for testing:
- Use [+ Add Context] or @ to mention features
- Attach relevant files for reference

**Example Prompt:**
```
Write a comprehensive description of this function that will be used to help you generate unit tests.
@[fileName]
```

### 3. Create Test File and Generate Tests
1. Create a new test file (e.g., `formatFullName.test.js`)
2. Use this prompt template:
```
Generate comprehensive unit tests for the [fileName] function. Include tests for:
- Normal cases with valid inputs
- Edge cases ([provide example(s)])
- Error cases ([provide example(s)])

Use [test framework] as the testing framework.
```

### 4. Review and Refine Test Cases
Review the generated tests for:
- Coverage of key scenarios
- Edge cases
- Error handling

#### Example Test Output:
```javascript
import { describe, test, expect } from '@jest/globals';
import { formatFullName } from './formatFullName.js';

describe('formatFullName', () => {
  test('formats full name correctly', () => {
    expect(formatFullName('John', 'Doe')).toBe('John Doe');
  });

  test('trims whitespace from names', () => {
    expect(formatFullName(' Jane ', ' Smith ')).toBe('Jane Smith');
  });

  test('returns single name if one is empty', () => {
    expect(formatFullName('Alice', '')).toBe('Alice');
    expect(formatFullName('', 'Cooper')).toBe('Cooper');
  });

  test('returns empty string if both names are empty', () => {
    expect(formatFullName('', '')).toBe('');
  });

  test('throws error for non-string inputs', () => {
    expect(() => formatFullName(123, 'Smith')).toThrow('Both firstName and lastName must be strings');
    expect(() => formatFullName('John', null)).toThrow('Both firstName and lastName must be strings');
  });

  test('handles names with multiple spaces', () => {
    expect(formatFullName('Mary Jane', 'Watson Parker')).toBe('Mary Jane Watson Parker');
  });
});
```

### 5. Run and Verify Tests
1. Save the test file
2. Run tests using Cursor's terminal (`npm test` or `jest`)
3. Review results in the output pane
4. Debug any failures

#### Troubleshooting Tip
For test failures, ask Cursor for help:
```
The formatFullName function is failing the test case for names with hyphens. 
Can you suggest how to update the function to properly format 'John Smith-Jones'?
```

## Additional Resources
- [Github Copilot Cookbook: Generate Unit Tests]()