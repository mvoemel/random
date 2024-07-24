const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const axios = require("axios");

const SERVICE_NAME = "Query";
const PORT = 4002;
const NODE_ENV = "production";

const app = express();
app.use(bodyParser.json());
app.use(cors());

// Database Mockup
const postsWithComments = {};

/**
 * Function to handle incoming events and update the post-comments map accordingly.
 *
 * @param {string} type
 * @param {string} data
 */
const handleEvent = (type, data) => {
  if (type === "POST_CREATED") {
    const { id, title } = data;
    postsWithComments[id] = { id, title, comments: [] };
    console.log("Processed event:", type);
  } else if (type === "COMMENT_CREATED") {
    const { id, content, postId, status } = data;
    postsWithComments[postId].comments.push({ id, content, status });
    console.log("Processed event:", type);
  } else if (type === "COMMENT_UPDATED") {
    const { id, postId, status, content } = data;
    const comment = postsWithComments[postId].comments.find(
      (comment) => comment.id === id
    );
    comment.status = status;
    comment.content = content;
    console.log("Processed event:", type);
  }
};

/**
 * @desc Get all posts with their comments
 * @route GET /posts
 */
app.get("/posts", (req, res) => {
  res.status(200).send(postsWithComments);
});

/**
 * @desc Receive new events from the event bus
 * @route POST /events
 */
app.post("/events", (req, res) => {
  console.log("Received event:", req.body.type);

  const { type, data } = req.body;

  handleEvent(type, data);

  res.status(200).send({});
});

app.listen(PORT, async () => {
  console.log(`${SERVICE_NAME} Service running on port ${PORT}`);

  // Fetch and process past events from the event bus
  const response = await axios
    .get(
      `http://${
        NODE_ENV === "development" ? "localhost" : "event-bus-srv"
      }:4005/events`
    )
    .catch((error) => {
      console.log(error.message);
    });
  response.data.forEach((event) => {
    handleEvent(event.type, event.data);
  });
});
