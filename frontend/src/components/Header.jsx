export default function Header({ backendOnline }) {
  return (
    <header className="flex items-center justify-between px-6 py-4 bg-white border-b border-gray-200">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-brand-500 flex items-center justify-center text-white font-bold">
          AI
        </div>
        <div>
          <h1 className="text-lg font-semibold text-gray-900 leading-tight">
            AI Knowledge Assistant
          </h1>
          <p className="text-xs text-gray-500">Education Edition — powered by Claude</p>
        </div>
      </div>
      <div className="flex items-center gap-2 text-sm">
        <span
          className={`w-2 h-2 rounded-full ${backendOnline ? "bg-green-500" : "bg-red-500"}`}
        />
        <span className="text-gray-500">
          {backendOnline ? "Backend connected" : "Backend offline"}
        </span>
      </div>
    </header>
  );
}
