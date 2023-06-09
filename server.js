const compute = require("./compute.js");

const express = require("express");
const cors = require("cors");
const app = express();

app.use(cors());
// request body parser
app.use(express.json());
app.use(express.raw({ type: ["mp3", "ogg"], limit: 1e9 }));
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

    // const result = await compute("do_something(23)");
    const result = await compute(`getDataFinal('${audioFilePath}')`);

    // deserialize
    const modelResultObject = JSON.parse(result?.data);
    res.status(200).json(modelResultObject);
  } catch (error) {
    res.status(500).json({ error });
  }
});

app.use((req, res, next) => {
  res.status(404).json({ error: "Page Not Found" });
});

const listener = app.listen(process.env.PORT || 3000, () =>
  console.log(`VoTT server ON ${listener.address().port}`)
);
