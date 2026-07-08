import { useState } from "react";
import { uploadDocument, addUrlSource } from "../api.js";

const CATEGORIES = [
  "Academics", "Admissions", "Exams", "Library",
  "Hostel & Campus Life", "Scholarships & Fees", "Placements & Career", "General",
];

export default function UploadPanel({ onClose, onSourceAdded }) {
  const [tab, setTab] = useState("file");
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");
  const [category, setCategory] = useState("General");
  const [status, setStatus] = useState(null);
  const [busy, setBusy] = useState(false);

  async function handleFileSubmit(e) {
    e.preventDefault();
    if (!file) return;
    setBusy(true);
    setStatus(null);
    try {
      const result = await uploadDocument(file, category);
      setStatus({ ok: true, msg: `Added "${result.source}" (${result.chunks_added} chunks).` });
      onSourceAdded();
    } catch (err) {
      setStatus({ ok: false, msg: err.message });
    } finally {
      setBusy(false);
    }
  }

  async function handleUrlSubmit(e) {
    e.preventDefault();
    if (!url.trim()) return;
    setBusy(true);
    setStatus(null);
    try {
      const result = await addUrlSource(url.trim(), category);
      setStatus({ ok: true, msg: `Added "${result.source}" (${result.chunks_added} chunks).` });
      onSourceAdded();
    } catch (err) {
      setStatus({ ok: false, msg: err.message });
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl w-full max-w-md p-6 shadow-xl">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-gray-900">Add knowledge source</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          <button
            onClick={() => setTab("file")}
            className={`flex-1 py-1.5 rounded-lg text-sm font-medium ${
              tab === "file" ? "bg-brand-500 text-white" : "bg-gray-100 text-gray-600"
            }`}
          >
            Upload file
          </button>
          <button
            onClick={() => setTab("url")}
            className={`flex-1 py-1.5 rounded-lg text-sm font-medium ${
              tab === "url" ? "bg-brand-500 text-white" : "bg-gray-100 text-gray-600"
            }`}
          >
            Live website
          </button>
        </div>
        <div className="mb-3">
          <label className="text-xs text-gray-500">Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm mt-1"
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
        {tab === "file" ? (
          <form onSubmit={handleFileSubmit} className="space-y-3">
            <input
              type="file"
              accept=".txt,.pdf,.docx"
              onChange={(e) => setFile(e.target.files[0])}
              className="w-full text-sm border border-dashed border-gray-300 rounded-lg p-3"
            />
            <button
              type="submit"
              disabled={busy || !file}
              className="w-full bg-brand-500 hover:bg-brand-600 disabled:opacity-50 text-white text-sm font-medium py-2 rounded-lg"
            >
              {busy ? "Uploading..." : "Upload & Index"}
            </button>
          </form>
        ) : (
          <form onSubmit={handleUrlSubmit} className="space-y-3">
            <input
              type="url"
              placeholder="https://example.edu/exam-policy"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
            />
            <button
              type="submit"
              disabled={busy || !url.trim()}
              className="w-full bg-brand-500 hover:bg-brand-600 disabled:opacity-50 text-white text-sm font-medium py-2 rounded-lg"
            >
              {busy ? "Fetching..." : "Fetch & Index"}
            </button>
          </form>
        )}
        {status && (
          <p className={`mt-3 text-sm ${status.ok ? "text-green-600" : "text-red-500"}`}>
            {status.msg}
          </p>
        )}
      </div>
    </div>
  );
}