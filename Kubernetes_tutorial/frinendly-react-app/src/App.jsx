import { useState } from "react";

function App() {
  const [name, setName] = useState(""); // user input
  const [message, setMessage] = useState(""); // backend response

  // const backendUrl = process.env.REACT_APP_BACKEND_URL;
  // const backendUrl = "http://backend-service:5000";
  const backendUrl = "http://myapp.example.com";

  const handleFetchMessage = () => {
    fetch(`${backendUrl}/api/message?name=${name || "Guest"}`)
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("Error fetching message"));
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>React Frontend</h1>

      <input
        type="text"
        placeholder="Enter your name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={{ padding: "0.5rem", marginRight: "1rem" }}
      />

      <button onClick={handleFetchMessage} style={{ padding: "0.5rem 1rem" }}>
        Get Message
      </button>

      {message && (
        <p style={{ marginTop: "1rem", fontWeight: "bold" }}>{message}</p>
      )}
    </div>
  );
}

export default App;
