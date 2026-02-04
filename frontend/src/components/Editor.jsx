export default function Editor() {
  return (
    <div className="editor">
      <div className="panel-header">
        <h2>Markdown Thesis Editor</h2>
        <button type="button" className="ghost">
          Save Draft
        </button>
      </div>
      <textarea
        placeholder="Draft your thesis sections here using Markdown..."
        defaultValue={`# Thesis: Mergers & Acquisitions\n\n## Research Question\n- How do M&A deals create value?\n\n## Notes\n- Add literature citations and data sources.`}
      />
      <div className="editor-meta">
        <span>RAG memory: drafts, PDFs, chats</span>
        <span>Auth: Firebase (connected)</span>
      </div>
    </div>
  );
}
