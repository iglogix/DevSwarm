import React, { useState } from "react";

function MessageInput({ onSendMessage, loading }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput("");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div style={{ marginTop: "10px" }}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message here..."
        style={{ width: "80%", padding: "5px" }}
      />
      <button onClick={handleSend} disabled={loading} style={{ marginLeft: "10px", padding: "5px" }}>
        {loading ? "Sending..." : "Send"}
      </button>
    </div>
  );
}

export default MessageInput;
