import React from "react";

const CommentsList = ({ comments }) => {
  return (
    <ul>
      {comments.map((comment) => {
        let content;

        if (comment.status === "approved") {
          content = comment.content;
        } else if (comment.status === "pending") {
          content = <i>This comment awaits approval.</i>;
        } else if (comment.status === "rejected") {
          content = <i>This comment has been rejected.</i>;
        }

        return <li key={comment.id}>{content}</li>;
      })}
    </ul>
  );
};

export default CommentsList;
