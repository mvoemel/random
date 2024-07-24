const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");

const SERVICE_NAME = "Moderation";
const PORT = 4003;
const NODE_ENV = "production";

const WORD_TO_BLOCK = "orange";

const app = express();
app.use(bodyParser.json());

/**
 * @desc Receive new events from the event bus
 * @route POST /events
 */
app.post("/events", async (req, res) => {
  console.log("Received event:", req.body.type);

  const { type, data } = req.body;

  if (type === "COMMENT_CREATED") {
    const status = data.content.includes(WORD_TO_BLOCK)
      ? "rejected"
      : "approved";

    // Publish comment moderated event to the event bus
    await axios
      .post(
        `http://${
          NODE_ENV === "development" ? "localhost" : "event-bus-srv"
        }:4005/events`,
        {
          type: "COMMENT_MODERATED",
          data: {
            id: data.id,
            postId: data.postId,
            content: data.content,
            status,
          },
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
