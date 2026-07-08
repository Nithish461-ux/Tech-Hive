const CATEGORY_COLORS = {
  Academics: "bg-blue-100 text-blue-700",
  Admissions: "bg-purple-100 text-purple-700",
  Exams: "bg-orange-100 text-orange-700",
  Library: "bg-teal-100 text-teal-700",
  "Hostel & Campus Life": "bg-pink-100 text-pink-700",
  "Scholarships & Fees": "bg-green-100 text-green-700",
  "Placements & Career": "bg-indigo-100 text-indigo-700",
  General: "bg-gray-100 text-gray-700",
};

export default function Sidebar({ documents, onOpenUpload }) {
  const grouped = documents.reduce((acc, doc) => {
    acc[doc.category] = acc[doc.category] || [];
    acc[doc.category].push(doc);
    return acc;
  }, {});

  return (
    <aside className="w-72 bg-white border-r border-gray-200 flex flex-col h-full">
      <div className="p-4 border-b border-gray-100">
        <button
          onClick={onOpenUpload}
          className="w-full py-2.5 rounded-lg bg-brand-500 text-white text-sm font-medium hover:bg-brand-600 transition"
        >
          + Add knowledge source
        </button>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
          Knowledge Base ({documents.length} sources)
        </p>
        {Object.keys(grouped).length === 0 && (
          <p className="text-sm text-gray-400">No sources loaded yet.</p>
        )}
        {Object.entries(grouped).map(([category, docs]) => (
          <div key={category}>
            <span
              className={`inline-block text-xs font-medium px-2 py-0.5 rounded-full mb-2 ${
                CATEGORY_COLORS[category] || CATEGORY_COLORS.General
              }`}
            >
              {category}
            </span>
            <ul className="space-y-1">
              {docs.map((doc) => (
                <li
                  key={doc.source}
                  className="text-sm text-gray-700 truncate px-2 py-1 rounded hover:bg-gray-50"
                  title={doc.source}
                >
                  📄 {doc.source}
                  <span className="text-gray-400 text-xs ml-1">({doc.chunks})</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </aside>
  );
}
