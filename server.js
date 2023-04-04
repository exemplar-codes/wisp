const exec = require("./myUtil");

const express = require("express");
const app = express();

// request body parser
app.use(express.json());
app.use(express.raw({ type: "mp3", limit: 1e9 }));
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res, next) => {
  res.sendFile(__dirname + "/index.html");
});

const fs = require("fs/promises");
const path = require("path");
const TEMP_AUDIO_FILE = "temp.mp3";
const audioFilePath = path.join(__dirname, TEMP_AUDIO_FILE);

app.post("/audio", async (req, res, next) => {
  try {
    await fs.writeFile(audioFilePath, req.body);

    const { stderr, stdout } = await exec(`python main.py ${audioFilePath}`);

    res.status(200).json(JSON.parse(stdout || stderr || {}));
  } catch (error) {
    res.status(500).json({ error });
  }
});

app.use((req, res, next) => {
  res.status(404).json({ error: "Page Not Found" });
});

app.listen(3000 || process.env.PORT, () => console.log("VoTT server ON"));
