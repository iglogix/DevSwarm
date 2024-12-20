import React, { useState } from "react";
import axios from "axios";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

const API_URL = "http://localhost:5000"; // Update with your deployed backend URL

function Chat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSendMessage_1 = async (userMessage) => {
    const newMessage = { role: "user", content: userMessage };
    setMessages([...messages, newMessage]);
    setLoading(true);

    try {
        const response = await axios.post(`${API_URL}/coordinator`, {
            query: userMessage,
        });

        const botResponses = response.data.data;
        botResponses.forEach((subtask) => {
            const botMessage = {
                role: "assistant",
                content: `Subtask: ${subtask.subtask}\nResult: ${subtask.result}`,
            };
            setMessages((prevMessages) => [...prevMessages, botMessage]);
        });
    } catch (error) {
        setMessages((prevMessages) => [
            ...prevMessages,
            { role: "assistant", content: "An error occurred. Please try again." },
        ]);
    } finally {
        setLoading(false);
    }
};

  const handleSendMessage = async (userMessage) => {
    const newMessage = { role: "user", content: userMessage };
    setMessages([...messages, newMessage]);
    setLoading(true);

    try {
        const response = await axios.post(`${API_URL}/coordinator`, {
            query: userMessage,
        });

        const taskId = response.data.task_id;

        // Poll task status
        const pollStatus = async () => {
            const statusResponse = await axios.get(`${API_URL}/status/${taskId}`);
            const taskStatus = statusResponse.data;

            if (taskStatus.status === 'completed' ) {
              // const botResponse = taskStatus.result.data.response;
              // const botMessage = {
              //   role: "assistant",
              //   content: typeof botResponse === "string" ? botResponse : JSON.stringify(botResponse, null, 2),
              // };
              
              const botMessage = {
                  role: "assistant",
                  content: JSON.stringify(taskStatus.result, null, 2),
              };
              
                setMessages((prevMessages) => [...prevMessages, botMessage]);
                setLoading(false);
            } else {
                setTimeout(pollStatus, 2000); // Retry after 2 seconds
            }
        };

        pollStatus();
    } catch (error) {
        setMessages((prevMessages) => [
            ...prevMessages,
            { role: "assistant", content: "An error occurred. Please try again." },
        ]);
        setLoading(false);
    }
};

const handleSendMessage_0 = async (userMessage) => {
    const newMessage = { role: "user", content: userMessage };
    setMessages([...messages, newMessage]);
    setLoading(true);
  
    try {
      const response = await axios.post(`${API_URL}/coordinator`, {
        query: userMessage,
      });
  
      const botResponse = response.data.data.response;
      const botMessage = {
        role: "assistant",
        content: typeof botResponse === "string" ? botResponse : JSON.stringify(botResponse, null, 2),
      };
  
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: "assistant", content: "An error occurred. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div style={{ margin: "0 auto", maxWidth: "600px", textAlign: "center" }}>
      <h1>Chat Interface</h1>
      <MessageList messages={messages} />
      {loading && <p>Processing...</p>}
      <MessageInput onSendMessage={handleSendMessage} loading={loading} />
    </div>
  );
}

export default Chat;
