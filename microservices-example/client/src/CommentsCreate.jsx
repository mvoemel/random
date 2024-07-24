import React, { useState } from "react";
import axios from "axios";
import { COMMENTS_SERVICE_BASEURL } from "./constants";

const CommentsCreate = ({ postId }) => {
  const [content, setContent] = useState("");
  const handleSubmit = async (event) => {
    event.preventDefault();

    const response = await axios.post(
      `${COMMENTS_SERVICE_BASEURL}/posts/${postId}/comments`,
      { content }
    );

    console.log(response.data);

    setContent("");
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>New Comment</label>
          <input
            value={content}
            onChange={(event) => setContent(event.target.value)}
            type="text"
            className="form-control"
            id="commentText"
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Add Comment
        </button>
      </form>
    </div>
  );
};

export default CommentsCreate;
