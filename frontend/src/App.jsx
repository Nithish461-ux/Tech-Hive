import { useEffect, useState, useCallback } from "react";
import Header from "./components/Header.jsx";
import Sidebar from "./components/Sidebar.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import UploadPanel from "./components/UploadPanel.jsx";
import { fetchDocuments, checkHealth } from "./api.js";

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [showUpload, setShowUpload] = useState(false);
  const [backendOnline, setBackendOnline] = useState(false);

  const loadDocuments = useCallback(async () => {
    try {
      const docs = await fetchDocuments();
      setDocuments(docs);
    } catch {
      setDocuments([]);
    }
  }, []);

  useEffect(() => {
    (async () => {
      try {
        await checkHealth();
        setBackendOnline(true);
      } catch {
        setBackendOnline(false);
      }
      loadDocuments();
    })();
  }, [loadDocuments]);

  return (
    <div className="h-screen flex flex-col">
      <Header backendOnline={backendOnline} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar documents={documents} onOpenUpload={() => setShowUpload(true)} />
        <ChatWindow />
      </div>
      {showUpload && (
        <UploadPanel
          onClose={() => setShowUpload(false)}
          onSourceAdded={loadDocuments}
        />
      )}
    </div>
  );
}
