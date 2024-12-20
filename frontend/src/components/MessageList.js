import React from "react";

function MessageList({ messages }) {
  return (
    <div style={{ border: "1px solid #ccc", padding: "10px", height: "300px", overflowY: "scroll" }}>
      {messages.map((msg, index) => (
        <div key={index} style={{ marginBottom: "10px" }}>
          <strong>{msg.role === "user" ? "You" : "Bot"}:</strong> {msg.content}
        </div>
      ))}
    </div>
  );
}

export default MessageList;
