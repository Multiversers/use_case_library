function processUserInput(input) {
  // Simulate processing user input
  if (input === undefined) {
      throw new Error('User input is undefined');
  }
  return `Processed: ${input}`;
}

// Simulate user input
const userInput = undefined;
console.log(processUserInput(userInput));
