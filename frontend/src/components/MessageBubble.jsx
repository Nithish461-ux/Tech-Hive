export default function MessageBubble({ message, onActionClick }) {
  const isUser = message.role === "user";
  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-xl bg-brand-500 text-white px-4 py-2.5 rounded-2xl rounded-tr-sm text-sm">
          {message.content}
        </div>
      </div>
    );
  }
  return (
    <div className="flex justify-start">
      <div className="max-w-2xl bg-white border border-gray-200 px-4 py-3 rounded-2xl rounded-tl-sm text-sm text-gray-800 shadow-sm">
        {message.category && (
          <span className="inline-block text-[11px] font-medium text-brand-600 bg-brand-50 px-2 py-0.5 rounded-full mb-2">
            {message.category}
          </span>
        )}
        <p className="whitespace-pre-line leading-relaxed">{message.content}</p>
        {message.sources && message.sources.length > 0 && (
          <div className="mt-3 border-t border-gray-100 pt-2">
            <p className="text-[11px] text-gray-400 mb-1">Sources referenced:</p>
            <div className="flex flex-wrap gap-1.5">
              {message.sources.map((s, i) => (
                <span
                  key={i}
                  title={s.snippet}
                  className="text-[11px] bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full cursor-help"
                >
                  {s.source}
                </span>
              ))}
            </div>
          </div>
        )}
        {message.suggested_actions && message.suggested_actions.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {message.suggested_actions.map((action, i) => (
              <button
                key={i}
                onClick={() => onActionClick(action)}
                className="text-xs border border-brand-200 text-brand-700 bg-brand-50 hover:bg-brand-100 px-2.5 py-1 rounded-full transition"
              >
                {action}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
