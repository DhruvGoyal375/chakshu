// Import the necessary libraries
const mjAPI = require("mathjax-node");
const SRE = require("speech-rule-engine");

let sreInitialized = false; // To check if SRE has been initialized

// Configure MathJax
mjAPI.config({
  MathJax: {
    tex: {
      inlineMath: [["$", "$"], ["\\(", "\\)"]],
      displayMath: [["$$", "$$"], ["\\[", "\\]"]],
    },
    mml: true,
  },
});
mjAPI.start();

// Initialize the Speech Rule Engine
async function setupSre(locale = "en") {
  if (!sreInitialized) {
    await SRE.setupEngine({
      locale: locale,
      domain: "clearspeak",
      style: "default",
    });
    sreInitialized = true; // Mark SRE as initialized
  }
}

// Convert LaTeX input to MathML
async function convertLatexToMathML(latex) {
  return new Promise((resolve, reject) => {
    mjAPI.typeset(
      {
        math: latex,
        format: "TeX", // Input is LaTeX
        mml: true, // Output MathML
      },
      function (data) {
        if (!data.errors) {
          resolve(data.mml);
        } else {
          reject(data.errors);
        }
      }
    );
  });
}

// Convert MathML to ClearSpoken output
function convertMathMLToSpeech(mathml) {
  return SRE.toSpeech(mathml);
}

// Main function to convert LaTeX to ClearSpoken output
async function convertLatexToClearspeak(latex) {
  await setupSre("en"); // Set up SRE with English locale
  const mathml = await convertLatexToMathML(latex);
  const clearSpokenOutput = convertMathMLToSpeech(mathml);
  return clearSpokenOutput;
}

// Example usage for testing
async function testConversion() {
  const latexInput = `\\displaystyle {\\frac {\\partial \\rho }{\\partial t}}=0.`;
  console.time("Conversion Time");
  try {
    const output = await convertLatexToClearspeak(latexInput);
    console.log("Final ClearSpoken output:", output);
  } catch (error) {
    console.error("Error during conversion:", error);
  }
  console.timeEnd("Conversion Time");
}

// Uncomment this line to run the example directly when this file is executed
// testConversion();

module.exports = convertLatexToClearspeak;
