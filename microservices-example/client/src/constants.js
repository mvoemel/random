const NODE_ENV = "production";

export const POSTS_SERVICE_BASEURL =
  NODE_ENV === "development" ? "http://localhost:4000" : "http://posts.com";

export const COMMENTS_SERVICE_BASEURL =
  NODE_ENV === "development" ? "http://localhost:4001" : "http://posts.com";

export const QUERY_SERVICE_BASEURL =
  NODE_ENV === "development" ? "http://localhost:4002" : "http://posts.com";
