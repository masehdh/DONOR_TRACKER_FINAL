const mongoose = require("mongoose");

const searchTermSchema = new mongoose.Schema({
  term: {
    type: String,
    required: true,
  },
});

module.exports = mongoose.model("SearchTerms", searchTermSchema);
