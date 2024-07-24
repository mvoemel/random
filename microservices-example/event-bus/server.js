const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");

const SERVICE_NAME = "Event-bus";
const PORT = 4005;
const NODE_ENV = "production";

const app = express();
app.use(bodyParser.json());

// Record of all events published to the event bus
const events = [];

/**
 * @desc Event bus route to publish events to all services
 * @route POST /events
 */
app.post("/events", async (req, res) => {
  const event = req.body;

  events.push(event);

  // Posts Service
  axios
    .post(
      `http://${
        NODE_ENV === "development" ? "localhost" : "posts-clusterip-srv"
      }:4000/events`,
      event
    )
    .catch((error) => {
      console.log(error.message);
    });
  // Comments Service
  axios
    .post(
      `http://${
        NODE_ENV === "development" ? "localhost" : "comments-srv"
      }:4001/events`,
      event
    )
    .catch((error) => {
      console.log(error.message);
    });
  // Query Service
  axios
    .post(
      `http://${
        NODE_ENV === "development" ? "localhost" : "query-srv"
      }:4002/events`,
      event
    )
    .catch((error) => {
      console.log(error.message);
    });
  // Moderation Service
  axios
    .post(
      `http://${
        NODE_ENV === "development" ? "localhost" : "moderation-srv"
      }:4003/events`,
      event
    )
    .catch((error) => {
      console.log(error.message);
    });

  res.status(200).send({ status: "OK" });
});

/**
 * @desc Event bus route to fetch all events published to the event bus
 * @route GET /events
 */
app.get("/events", (req, res) => {
  res.status(200).send(events);
});

app.listen(PORT, () => {
  console.log(`${SERVICE_NAME} Service running on port ${PORT}`);
});
