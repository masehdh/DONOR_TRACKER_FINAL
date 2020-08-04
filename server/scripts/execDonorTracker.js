const { exec } = require("child_process");
const path = require('path');

const donor_tracker = () => {
  return new Promise((resolve, reject) => {
    exec(
      `python ${path.join(__dirname, "donor_tracker.py")}`,
      (err, stdout, stderr) => {
      if (err) {
        reject(err);
      }
      resolve(stdout);
    });
  });
};

// const donor_tracker = () => {
//   return new Promise((resolve, reject) => {
//     exec(
//       `py donor_tracker.py`,
//       (err, stdout, stderr) => {
//       if (err) {
//         reject(err);
//       }
//       resolve(stdout);
//     });
//   });
// };

module.exports = donor_tracker;
