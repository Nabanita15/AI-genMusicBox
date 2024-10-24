const express = require("express");
const { PythonShell } = require("python-shell");
const path = require("path");

const app = express();
const port = 5000;

app.use(express.json()); // Parse incoming JSON requests

// Endpoint to generate music using Python Jukebox
app.post("/generate_music", (req, res) => {
  const { artist, genre, lyrics, sample_length_in_seconds } = req.body;

  // Define options to pass to the Python script
  let options = {
    mode: "json",
    pythonOptions: ["-u"],
    scriptPath: "./", // Path to your Python script
    args: [artist, genre, lyrics, sample_length_in_seconds],
  };

  // Call the Python script
  PythonShell.run("generate_music.py", options, (err, results) => {
    if (err) throw err;

    // Send back the music URL or data
    res.json({
      status: "success",
      music_url: "http://localhost:5000/static/output_song.wav",
    });
  });
});

// Serve static files (for serving generated music files)
app.use("/static", express.static(path.join(__dirname, "static")));

app.get("/", (req, res) => {
  res.send("Hello world");
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
