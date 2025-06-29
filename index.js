const functions = require("firebase-functions");
const express = require("express");
const cors = require("cors");
const genai = require("@google/generative-ai");

const app = express();
app.use(cors({ origin: true }));
app.use(express.json());

const GEMINI_API_KEY = "AIzaSyB3ccvQqCHh6Y_40OI0SWZjP_p-P0bQDYQ"; // 🔐 IMPORTANT

const model = new genai.GenerativeModel({
  model: "gemini-pro",
  apiKey: GEMINI_API_KEY,
});

app.post("/ask", async (req, res) => {
  const userMessage = req.body.message;
  try {
    const result = await model.generateContent(userMessage);
    res.json({ reply: result.response.text() });
  } catch (err) {
    console.error(err);
    res.json({ reply: "Oops! Something went wrong." });
  }
});

exports.ask = functions.https.onRequest(app);
