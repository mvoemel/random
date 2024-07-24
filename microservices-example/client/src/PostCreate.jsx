import React, { useState } from "react";
import axios from "axios";
import { POSTS_SERVICE_BASEURL } from "./constants";

const PostCreate = () => {
  const [title, setTitle] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    await axios.post(`${POSTS_SERVICE_BASEURL}/posts/create`, {
      title,
    });

    setTitle("");
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <small id="titleHelp" className="form-text text-muted">
            Please enter a title for your post.
          </small>
          <input
            type="text"
            className="form-control"
            id="title"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            placeholder="Enter title"
          />
          <button type="submit" className="btn btn-primary">
            Create Post
          </button>
        </div>
      </form>
    </div>
  );
};

export default PostCreate;
