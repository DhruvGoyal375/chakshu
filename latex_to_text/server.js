const express = require("express");
const cors = require("cors");
const router = express.Router();
const clearspoken = require("./clearspoken.js");

const app = express();
app.use(cors());
app.use(express.json());

// @route   GET /api
// @desc    Test API endpoint
app.post("/api", async (req, res) => {
  try {
    const { latexInput } = req.body;
    console.log(latexInput);
    const clearSpokenOutput = await clearspoken(latexInput); // Await the conversion
    res.json({ message: "Conversion successful", output: clearSpokenOutput });
  } catch (error) {
    console.error("Error in GET /api:", error);
    res.status(500).json({ message: "Server Error", error: error.toString() });
  }
});

const PORT = 8080;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
