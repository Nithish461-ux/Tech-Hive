import { useState, useRef, useEffect } from "react";
import MessageBubble from "./MessageBubble.jsx";
import { sendChatMessage } from "../api.js";

const STARTER_PROMPTS = [
  "What is the minimum attendance required for exams?",
  "How do I apply for a scholarship?",
  "What are the hostel curfew timings?",
  "What's the average placement package?",
];

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! I'm your AI Knowledge Assistant. Ask me anything about academics, admissions, exams, library, hostel life, scholarships, or placements — I'll answer from the institute's knowledge base.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(text) {
    const query = (text ?? input).trim();
    if (!query || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setInput("");
    setLoading(true);

    try {
      const result = await sendChatMessage(query);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: result.answer,
          category: result.category,
          sources: result.sources,
          suggested_actions: result.suggested_actions,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `⚠️ ${err.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex-1 flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((m, i) => (
          <MessageBubble key={i} message={m} onActionClick={(a) => handleSend(a)} />
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 px-4 py-3 rounded-2xl rounded-tl-sm text-sm text-gray-400 shadow-sm">
              Thinking...
            </div>
          </div>
        )}
        {messages.length === 1 && (
          <div className="grid grid-cols-2 gap-2 pt-2">
            {STARTER_PROMPTS.map((p) => (
              <button
                key={p}
                onClick={() => handleSend(p)}
                className="text-left text-sm text-gray-600 bg-white border border-gray-200 rounded-xl px-3 py-2 hover:border-brand-400 hover:text-brand-600 transition"
              >
                {p}
              </button>
            ))}
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <div className="p-4 border-t border-gray-200 bg-white">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about admissions, exams, library, hostel, scholarships..."
            className="flex-1 border border-gray-300 rounded-full px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-brand-500 hover:bg-brand-600 disabled:opacity-50 text-white text-sm font-medium px-5 py-2.5 rounded-full transition"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}