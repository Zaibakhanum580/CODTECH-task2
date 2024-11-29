import React, { useState, useEffect } from "react";
import axios from "axios";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000");

const App = () => {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState("");
  const [profilePicture, setProfilePicture] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:5000/posts").then((response) => {
      setPosts(response.data);
    });

    socket.on("newPost", (post) => {
      setPosts((prev) => [post, ...prev]);
    });
  }, []);

  const handlePost = () => {
    axios.post("http://localhost:5000/posts", { content: newPost }).then(() => {
      setNewPost("");
    });
  };

  const handleProfilePictureUpload = (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("profilePicture", file);

    axios.post("http://localhost:5000/upload", formData).then((response) => {
      alert("Profile picture uploaded!");
    });
  };

  return (
    <div>
      <h1>Social Media App</h1>

      <div>
        <h2>Upload Profile Picture</h2>
        <input type="file" onChange={handleProfilePictureUpload} />
      </div>

      <div>
        <h2>Create a Post</h2>
        <textarea
          value={newPost}
          onChange={(e) => setNewPost(e.target.value)}
        />
        <button onClick={handlePost}>Post</button>
      </div>

      <div>
        <h2>Posts</h2>
        {posts.map((post) => (
          <div key={post.id}>
            <p>{post.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
