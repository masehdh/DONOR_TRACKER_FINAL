const express = require("express");
const mongoose = require("mongoose");
const connectDB = require("../scripts/connectDB");
const SearchTerm = require("../models/SearchTerm");
const Result = require("../models/Result");
const donor_tracker = require("../scripts/execDonorTracker");

// Set up
const router = express.Router();
connectDB();

// Get Results
router.get("/", async (req, res) => {
  res.status(200);
  res.json(await Result.find());
});

router.get("/search", async (req, res) => {
  try {
    res.status(200);
    res.send(await donor_tracker());
  } catch (err) {
      res.status(500);
      res.send(err);
    };
});

// Add Result
router.post("/", async (req, res) => {
  const searchTerm = new SearchTerm({
    term: req.body.term,
  });

  savedTerm = await searchTerm.save();

  res.status(201);
  res.send(savedTerm);
});

module.exports = router;
