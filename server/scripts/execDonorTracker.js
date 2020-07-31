const { exec } = require("child_process");
const path = require('path');

const donor_tracker = () => {
  return new Promise((resolve, reject) => {
    exec(
      `py ${path.join(__dirname, "donor_tracker.py")}`,
      (err, stdout, stderr) => {
      if (err) {
        reject(err);
      }
      resolve(stdout);
    });
  });
};

module.exports = donor_tracker;
