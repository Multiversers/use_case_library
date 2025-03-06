1. 
#### Follow along example
In this use case, we will look at an example function: `formatFullName()`, which takes a person's first and last name as separate inputs and combines them into a properly formatted full name. We can imagine this function as part of a user registration system where properly formatted names are crucial for consistent data display, sorting, and searching across an application.

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