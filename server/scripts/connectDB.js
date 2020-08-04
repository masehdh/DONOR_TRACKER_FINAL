const mongoose = require("mongoose");

const connectDB = () => {
  mongoose.connect("mongodb://mongo:27017/donortrackerdb", {
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