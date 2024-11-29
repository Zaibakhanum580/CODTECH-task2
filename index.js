const express = require("express");
const cors = require("cors");
const multer = require("multer");
const { Server } = require("socket.io");
const http = require("http");

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

const posts = [];
const upload = multer({ dest: "uploads/" });

app.use(cors());
app.use(express.json());

app.get("/posts", (req, res) => {
  res.json(posts);
});

app.post("/posts", (req, res) => {
  const post = { id: posts.length + 1, content: req.body.content };
  posts.unshift(post);
  io.emit("newPost", post);
  res.status(201).json(post);
});

app.post("/upload", upload.single("profilePicture"), (req, res) => {
  res.status(200).json({ message: "Profile picture uploaded!" });
});

server.listen(5000, () => console.log("Server running on http://localhost:5000"));
