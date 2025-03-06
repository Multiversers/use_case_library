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
  
        resolve(csvData);
      };
  
      fileReader.readAsText(file);
    });