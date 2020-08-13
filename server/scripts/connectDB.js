const mongoose = require("mongoose");

const connectDB = () => {
  mongoose.connect("mongodb://maseh:shareef@mongo:27017/donortrackerdb?authSource=admin", {
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