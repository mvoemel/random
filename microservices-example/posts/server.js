const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const axios = require("axios");
const { randomBytes } = require("crypto");

const SERVICE_NAME = "Posts";
const PORT = 4000;
const NODE_ENV = "production";

const app = express();
app.use(bodyParser.json());
app.use(cors());

// Database Mockup
const posts = {};

/**
 * @desc Get all posts
 * @route GET /posts
 * @deprecated
 */
app.get("/posts", (req, res) => {
  res.status(200).send(posts);
});

/**
 * @desc Create a new post
 * @route POST /posts/create
 */
app.post("/posts/create", async (req, res) => {
  const { title } = req.body;
  const id = randomBytes(4).toString("hex");

  posts[id] = { id, title };

  // Publish post created event to the event bus
  await axios
    .post(
      `http://${
        NODE_ENV === "development" ? "localhost" : "event-bus-srv"
      }:4005/events`,
      {
        type: "POST_CREATED",
        data: { id, title },
      }
    )
    .catch((error) => {
      console.log(error.message);
    });

  res.status(201).send(posts[id]);
});

/**
 * @desc Receive new events from the event bus
 * @route POST /events
 */
app.post("/events", (req, res) => {
  console.log("Received event:", req.body.type);
  res.status(200).send({});
});

app.listen(PORT, () => {
  console.log(`${SERVICE_NAME} Service running on port ${PORT}`);
});
