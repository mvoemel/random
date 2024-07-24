const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const axios = require("axios");
const { randomBytes } = require("crypto");

const SERVICE_NAME = "Comments";
const PORT = 4001;
const NODE_ENV = "production";

const app = express();
app.use(bodyParser.json());
app.use(cors());

// Database Mockup
const commentsByPostId = {};

/**
 * @desc Get all comments for a specific post
 * @route GET /posts/:id/comments
 * @deprecated
 */
app.get("/posts/:id/comments", (req, res) => {
  const { id: postId } = req.params;

  if (!commentsByPostId[postId]) {
    return res.status(404).send([]);
  }

  res.status(200).send(commentsByPostId[postId]);
});

/**
 * @desc Create a new comment for a specific post
 * @route POST /posts/:id/comments
 */
app.post("/posts/:id/comments", async (req, res) => {
  const { id: postId } = req.params;
  const { content } = req.body;

  const commentId = randomBytes(4).toString("hex");
  const comments = commentsByPostId[postId] || [];

  comments.push({ id: commentId, content, status: "pending" });
  commentsByPostId[postId] = comments;

  // Publish comment created event to the event bus
  await axios
    .post(
      `http://${
        NODE_ENV === "development" ? "localhost" : "event-bus-srv"
      }:4005/events`,
      {
        type: "COMMENT_CREATED",
        data: { id: commentId, content, postId, status: "pending" },
      }
    )
    .catch((error) => {
      console.log(error.message);
    });

  res.status(201).send(comments);
});

/**
 * @desc Receive new events from the event bus
 * @route POST /events
 */
app.post("/events", async (req, res) => {
  console.log("Received event:", req.body.type);

  const { type, data } = req.body;

  if (type === "COMMENT_MODERATED") {
    const { id, postId, status, content } = data;

    const comments = commentsByPostId[postId] || [];
    const comment = comments.find((comment) => comment.id === id);
    comment.status = status;

    // Publish comment updated event to the event bus
    await axios
      .post(
        `http://${
          NODE_ENV === "development" ? "localhost" : "event-bus-srv"
        }:4005/events`,
        {
          type: "COMMENT_UPDATED",
          data: { id, postId, status, content },
        }
      )
      .catch((error) => {
        console.log(error.message);
      });

    console.log("Processed event:", req.body.type);
  }

  res.status(200).send({});
});

app.listen(PORT, () => {
  console.log(`${SERVICE_NAME} Service running on port ${PORT}`);
});
