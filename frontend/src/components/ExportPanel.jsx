import { useState } from "react";
import { exportMarkdown, exportPDF } from "../services/api";

export default function ExportPanel({ markdown, onBack, onReset }) {
  const [exporting, setExporting] = useState(false);

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

  return (
    <div className="card">
      <h2>Export Newsletter</h2>
      <p className="subtitle">Download or copy your newsletter for Substack</p>

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
      </div>

      <div className="btn-row">
        <button className="btn btn-secondary" onClick={onBack}>Back to Editor</button>
        <button className="btn btn-success" onClick={onReset}>Start New Newsletter</button>
      </div>
    </div>
  );
}