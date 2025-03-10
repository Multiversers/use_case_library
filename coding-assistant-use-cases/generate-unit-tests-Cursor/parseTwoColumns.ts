/**
 * Parses a CSV file containing two columns of email addresses.
 * 
 * @param file - A File object containing CSV data with two columns of email addresses
 * @returns A Promise that resolves to an array of email address pairs, where each pair is 
 *          represented as a tuple [managerEmail, learnerEmail]. The function validates that
 *          both columns contain valid email addresses and rejects the promise with an error
 *          message if the file format is invalid or if any row is missing required emails.
 */
export const parseTwoColumnEmailCsv = (
    file: File
  ): Promise<[string, string][]> =>
    new Promise((resolve, reject) => {
      const csvData: [string, string][] = [];
  
      const fileReader = new FileReader();
  
      fileReader.onload = () => {
        // Code that parses the CSV file
        try {
          const content = fileReader.result as string;
          if (!content) {
            return reject(new Error('Empty file content'));
          }

          // Split the content by lines and filter out empty lines
          const lines = content.split(/\r?\n/).filter(line => line.trim() !== '');
          
          // Simple email validation regex
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          
          for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            // Split the line by comma and trim whitespace
            const columns = line.split(',').map(col => col.trim());
            
            // Validate row has exactly two columns
            if (columns.length !== 2) {
              return reject(new Error(`Row ${i + 1} must have exactly two columns`));
            }
            
            const [managerEmail, learnerEmail] = columns;
            
            // Validate both emails are valid
            if (!emailRegex.test(managerEmail)) {
              return reject(new Error(`Invalid manager email in row ${i + 1}: ${managerEmail}`));
            }
            
            if (!emailRegex.test(learnerEmail)) {
              return reject(new Error(`Invalid learner email in row ${i + 1}: ${learnerEmail}`));
            }
            
            // Add valid pair to results
            csvData.push([managerEmail, learnerEmail]);
          }
          
          resolve(csvData);
        } catch (error) {
          reject(new Error(`Failed to parse CSV file: ${error.message}`));
        }
      };
      
      fileReader.onerror = () => {
        reject(new Error('Error reading file'));
      };
  
      fileReader.readAsText(file);
    });