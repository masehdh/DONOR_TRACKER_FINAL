const mongoose = require("mongoose");
require("dotenv/config");

const connectDB = () => {
  mongoose.connect(`mongodb://${process.env.DB_USER}:${process.env.DB_PASSWORD}@${process.env.DB_HOST}/donortrackerdb?authSource=admin`, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useFindAndModify: false,
  });
  const db = mongoose.connection;
  db.once('open', () => {
    console.log(`Connected to DB`);
  });
};

module.exports = connectDB;