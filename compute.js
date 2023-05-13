// const readline = require("readline");
const { spawn } = require("child_process");

// Spawn a child process to run the Python script as a module
const pythonProcess = spawn("python", ["-m", "main"]);

async function compute(input) {
  return new Promise((resolve, reject) => {
    // enter the input
    pythonProcess.stdin.write(`${input}\n`);

    pythonProcess.stdout.on("data", (data) => {
      resolve(data.toString());
    });

    // Handle errors and close events
    pythonProcess.on("error", (error) => {
      reject(error);
    });

    pythonProcess.on("close", () => {
      reject("Python process closed");
    });
  });
}

module.exports = compute;
