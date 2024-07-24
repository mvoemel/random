import React, { useState, useEffect } from "react";
import CommentsCreate from "./CommentsCreate";
import CommentsList from "./CommentsList";
import { QUERY_SERVICE_BASEURL } from "./constants";

const PostList = () => {
  const [postsWithComments, setPostsWithComments] = useState({});

  const fetchPosts = async () => {
    const response = await fetch(`${QUERY_SERVICE_BASEURL}/posts`).catch(
      (error) => {
        console.error(error);
      }
    );
    const responseData = (await response?.json()) || {};

    setPostsWithComments(responseData);
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  return (
    <div className="d-flex flex-row flex-wrap justify-content-between">
      {Object.values(postsWithComments)?.map((post) => {
        return (
          <div
            className="card"
            style={{ width: "30%", marginBottom: "20px" }}
            key={post.id}
          >
            <div className="card-body">
              <h3 className="card-title">{post.title}</h3>
              <CommentsList comments={post.comments} />
              <CommentsCreate postId={post.id} />
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default PostList;
