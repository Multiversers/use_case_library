import { parseTwoColumnEmailCsv } from './parseTwoColumns';

// Mock the FileReader API
class MockFileReader {
  onload: () => void = () => {};
  onerror: () => void = () => {};
  result: string | null = null;
  
  readAsText(file: File): void {
    // Simulate async behavior
    setTimeout(() => {
      if (file.size === 0) {
        this.result = '';
      } else {
        this.result = (file as any)._content;
      }
      this.onload();
    }, 0);
  }
}

// Mock the File class
const createMockFile = (content: string, name = 'test.csv'): File => {
  const file = new Blob([content], { type: 'text/csv' }) as any;
  file.name = name;
  file._content = content;
  return file as File;
};

// Replace global FileReader with mock
(global as any).FileReader = MockFileReader;

describe('parseTwoColumnEmailCsv', () => {
  // Normal cases
  test('should parse a valid CSV with multiple rows', async () => {
    const csvContent = 
      'manager1@example.com,learner1@example.com\n' +
      'manager2@example.com,learner2@example.com\n' +
      'manager3@example.com,learner3@example.com';
    
    const file = createMockFile(csvContent);
    const result = await parseTwoColumnEmailCsv(file);
    
    expect(result).toEqual([
      ['manager1@example.com', 'learner1@example.com'],
      ['manager2@example.com', 'learner2@example.com'],
      ['manager3@example.com', 'learner3@example.com']
    ]);
  });

  test('should parse a valid CSV with a single row', async () => {
    const csvContent = 'manager@example.com,learner@example.com';
    const file = createMockFile(csvContent);
    const result = await parseTwoColumnEmailCsv(file);
    
    expect(result).toEqual([
      ['manager@example.com', 'learner@example.com']
    ]);
  });

  test('should trim whitespace from emails', async () => {
    const csvContent = ' manager@example.com , learner@example.com ';
    const file = createMockFile(csvContent);
    const result = await parseTwoColumnEmailCsv(file);
    
    expect(result).toEqual([
      ['manager@example.com', 'learner@example.com']
    ]);
  });

  test('should handle different line endings (CRLF)', async () => {
    const csvContent = 'manager1@example.com,learner1@example.com\r\nmanager2@example.com,learner2@example.com';
    const file = createMockFile(csvContent);
    const result = await parseTwoColumnEmailCsv(file);
    
    expect(result).toEqual([
      ['manager1@example.com', 'learner1@example.com'],
      ['manager2@example.com', 'learner2@example.com']
    ]);
  });

  // Edge cases
  test('should handle valid complex email addresses', async () => {
    const csvContent = 'first.last+tag@example.com,name.with-symbols_123@sub.domain.com';
    const file = createMockFile(csvContent);
    const result = await parseTwoColumnEmailCsv(file);
    
    expect(result).toEqual([
      ['first.last+tag@example.com', 'name.with-symbols_123@sub.domain.com']
    ]);
  });

  test('should skip empty lines', async () => {
    const csvContent = 
      'manager1@example.com,learner1@example.com\n\n' +
      'manager2@example.com,learner2@example.com\n\n';
    
    const file = createMockFile(csvContent);
    const result = await parseTwoColumnEmailCsv(file);
    
    expect(result).toEqual([
      ['manager1@example.com', 'learner1@example.com'],
      ['manager2@example.com', 'learner2@example.com']
    ]);
  });

  // Error cases
  test('should reject if the file is empty', async () => {
    const file = createMockFile('');
    await expect(parseTwoColumnEmailCsv(file)).rejects.toThrow('Empty file content');
  });

  test('should reject if a row has more than two columns', async () => {
    const csvContent = 
      'manager1@example.com,learner1@example.com\n' +
      'manager2@example.com,learner2@example.com,extra@example.com';
    
    const file = createMockFile(csvContent);
    await expect(parseTwoColumnEmailCsv(file)).rejects.toThrow('Row 2 must have exactly two columns');
  });

  test('should reject if a row has less than two columns', async () => {
    const csvContent = 
      'manager1@example.com,learner1@example.com\n' +
      'manager2@example.com';
    
    const file = createMockFile(csvContent);
    await expect(parseTwoColumnEmailCsv(file)).rejects.toThrow('Row 2 must have exactly two columns');
  });

  test('should reject if the manager email is invalid', async () => {
    const csvContent = 'invalid-email,learner@example.com';
    const file = createMockFile(csvContent);
    await expect(parseTwoColumnEmailCsv(file)).rejects.toThrow('Invalid manager email in row 1: invalid-email');
  });

  test('should reject if the learner email is invalid', async () => {
    const csvContent = 'manager@example.com,invalid-email';
    const file = createMockFile(csvContent);
    await expect(parseTwoColumnEmailCsv(file)).rejects.toThrow('Invalid learner email in row 1: invalid-email');
  });

  test('should reject if multiple rows have invalid emails', async () => {
    const csvContent = 
      'manager1@example.com,learner1@example.com\n' +
      'invalid-email,learner2@example.com';
    
    const file = createMockFile(csvContent);
    await expect(parseTwoColumnEmailCsv(file)).rejects.toThrow('Invalid manager email in row 2: invalid-email');
  });

  test('should reject when FileReader encounters an error', async () => {
    const file = createMockFile('valid@example.com,another@example.com');
    
    // Override the readAsText method to trigger an error
    (global as any).FileReader = class ErrorFileReader {
      onload: () => void = () => {};
      onerror: () => void = () => {};
      
      readAsText(): void {
        setTimeout(() => {
          this.onerror();
        }, 0);
      }
    };
    
    await expect(parseTwoColumnEmailCsv(file)).rejects.toThrow('Error reading file');
    
    // Restore the mock for other tests
    (global as any).FileReader = MockFileReader;
  });
}); 