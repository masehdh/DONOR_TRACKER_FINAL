const express = require("express");
const cors = require("cors");
require("dotenv/config");

// Set up
const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cors());

// Routes
const resultsRoute = require("./routes/results");
app.use("/results", resultsRoute);

// Handle Production
// if (process.env.NODE_ENV === "production") {
//   app.use(express.static(`${__dirname}/public`));
//   app.get(/.*/, (req, res) => res.sendFile(`${__dirname}/public/index.html`));
// }
app.use(express.static(`${__dirname}/public`));
app.get(/.*/, (req, res) => res.sendFile(`${__dirname}/public/index.html`));

// Listen
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
