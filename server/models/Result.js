const mongoose = require("mongoose");

const resultSchema = new mongoose.Schema({
  country: String,
  title: String,
  link: String,
});

module.exports = mongoose.model("Article_results", resultSchema);