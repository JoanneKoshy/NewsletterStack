import { useState } from "react";
import { exportMarkdown, exportPDF, publishToHashnode } from "../services/api";

export default function ExportPanel({ markdown, onBack, onReset }) {
  const [exporting, setExporting] = useState(false);
  const [hashnodeTitle, setHashnodeTitle] = useState("");
  const [hashnodeTags, setHashnodeTags] = useState("");
  const [showHashnodeForm, setShowHashnodeForm] = useState(false);
  const [publishResult, setPublishResult] = useState(null);

  const handleMarkdownExport = async () => {
    setExporting(true);
    try {
      await exportMarkdown(markdown, "Investor_Newsletter");
    } catch (err) {
      alert("Export failed: " + err.message);
    } finally {
      setExporting(false);
    }
  };

  const handlePDFExport = async () => {
    setExporting(true);
    try {
      await exportPDF(markdown, "Investor_Newsletter");
    } catch (err) {
      alert("PDF export failed: " + err.message);
    } finally {
      setExporting(false);
    }
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(markdown);
    alert("Markdown copied to clipboard! Paste it into Substack.");
  };

  const handleHashnodePublish = async () => {
    if (!hashnodeTitle.trim()) {
      alert("Please enter a title for the post");
      return;
    }
    setExporting(true);
    try {
      const tags = hashnodeTags.split(",").map((t) => t.trim()).filter((t) => t);
      const result = await publishToHashnode(hashnodeTitle, markdown, tags);
      setPublishResult(result);
    } catch (err) {
      const msg = err.response?.data?.detail || err.message;
      alert("Hashnode publish failed: " + msg);
    } finally {
      setExporting(false);
    }
  };

  if (publishResult) {
    return (
      <div className="card">
        <h2>Published to Hashnode!</h2>
        <p style={{ marginTop: 12, fontSize: 14 }}>Your newsletter is live at:</p>
        <p style={{ marginTop: 8 }}>
          <a href={publishResult.url} target="_blank" rel="noopener noreferrer" style={{ color: "#2563eb", fontSize: 14 }}>
            {publishResult.url}
          </a>
        </p>
        <div className="btn-row">
          <button className="btn btn-success" onClick={onReset}>Start New Newsletter</button>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Export Newsletter</h2>
      <p className="subtitle">Download, copy, or publish your newsletter</p>

      <div className="export-options">
        <div className="export-card" onClick={handleCopyToClipboard}>
          <h3>Copy for Substack</h3>
          <p>Copy Markdown to clipboard and paste into Substack editor</p>
        </div>

        <div className="export-card" onClick={handleMarkdownExport}>
          <h3>Download .md</h3>
          <p>Save as a Markdown file</p>
        </div>

        <div className="export-card" onClick={handlePDFExport}>
          <h3>Download PDF</h3>
          <p>Save as a formatted PDF document</p>
        </div>

        <div className="export-card" onClick={() => setShowHashnodeForm(!showHashnodeForm)} style={{ borderColor: showHashnodeForm ? "#1a1a2e" : undefined, background: showHashnodeForm ? "#fafafa" : undefined }}>
          <h3>Publish to Hashnode</h3>
          <p>Publish directly to your Hashnode blog</p>
        </div>
      </div>

      {showHashnodeForm && (
        <div style={{ marginTop: 16, padding: 20, background: "#fafafa", borderRadius: 12 }}>
          <div style={{ marginBottom: 12 }}>
            <label style={{ fontSize: 13, fontWeight: 600, display: "block", marginBottom: 4 }}>Post Title</label>
            <input type="text" placeholder="e.g. Astrek Innovations — Investor Update Week 14" value={hashnodeTitle} onChange={(e) => setHashnodeTitle(e.target.value)} />
          </div>
          <div style={{ marginBottom: 12 }}>
            <label style={{ fontSize: 13, fontWeight: 600, display: "block", marginBottom: 4 }}>Tags (comma separated, optional)</label>
            <input type="text" placeholder="e.g. startup, investor-update, astrek" value={hashnodeTags} onChange={(e) => setHashnodeTags(e.target.value)} />
          </div>
          <button className="btn btn-primary" onClick={handleHashnodePublish} disabled={exporting}>
            {exporting ? "Publishing..." : "Publish Now"}
          </button>
        </div>
      )}

      <div className="btn-row">
        <button className="btn btn-secondary" onClick={onBack}>Back to Editor</button>
        <button className="btn btn-success" onClick={onReset}>Start New Newsletter</button>
      </div>
    </div>
  );
}