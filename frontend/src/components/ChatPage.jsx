import React, { useEffect, useRef, useState } from "react";
import { askQuestion } from "../api";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState(() => {
    return JSON.parse(localStorage.getItem("chat_history") || "[]");
  });
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    localStorage.setItem("chat_history", JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

const handleAsk = async () => {
  const trimmed = question.trim();
  if (!trimmed) return;

  setQuestion("");
  setLoading(true);

  try {
    const res = await askQuestion(trimmed);
    setMessages((prev) => [
      ...prev,
      { type: "question", text: trimmed },
      {
        type: "answer",
        text: res.answer,
        docs: res.documents,
      },
    ]);
  } catch (err) {
    setMessages((prev) => [
      ...prev,
      { type: "question", text: trimmed },
      {
        type: "answer",
        text: "❌ Erreur lors de l'appel au modèle.",
        docs: [],
      },
    ]);
  } finally {
    setLoading(false);
  }
};


  const clearChat = () => {
    localStorage.removeItem("chat_history");
    setMessages([]);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4 flex flex-col items-center">
      <div className="w-full max-w-2xl bg-white shadow-md rounded-lg p-6 flex flex-col space-y-4">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-700">💬 Chat ESTI</h1>
          <button
            onClick={clearChat}
            className="text-sm text-red-500 hover:underline"
          >
            🗑️ Effacer
          </button>
        </div>

        <div className="flex-1 overflow-y-auto max-h-[500px] space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-lg shadow text-sm ${
                msg.type === "question"
                  ? "bg-blue-100 self-end text-right"
                  : "bg-gray-100 self-start text-left"
              }`}
            >
              <p>{msg.text}</p>
              {msg.docs && (
                <ul className="mt-2 text-xs text-gray-600 list-disc list-inside">
                  {msg.docs.map((doc, i) => (
                    <li key={i}>{doc}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
          <div ref={chatEndRef}></div>
        </div>

        <div className="flex space-x-2">
          <input
            type="text"
            placeholder="Pose ta question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            className="flex-1 border border-blue-300 rounded px-4 py-2"
          />
          <button
            onClick={handleAsk}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          >
            {loading ? "..." : "Envoyer"}
          </button>
        </div>
      </div>
    </div>
  );
}
