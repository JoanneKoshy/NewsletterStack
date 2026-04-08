import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { generateNewsletter, regenerateNewsletter } from "../services/api";

export default function NewsletterEditor({
  extractedData,
  mediaLinks,
  markdown,
  setMarkdown,
  onComplete,
  onBack,
}) {
  const [loading, setLoading] = useState(!markdown);
  const [feedback, setFeedback] = useState("");
  const [regenerating, setRegenerating] = useState(false);

  useEffect(() => {
    if (!markdown) {
      setLoading(true);
      generateNewsletter(extractedData, mediaLinks, "formal")
        .then((res) => {
          setMarkdown(res.markdown);
          setLoading(false);
        })
        .catch((err) => {
          alert("Failed to generate: " + (err.response?.data?.detail || err.message));
          setLoading(false);
        });
    }
  }, []);

  const handleRegenerate = async () => {
    if (!feedback.trim()) return;
    setRegenerating(true);
    try {
      const res = await regenerateNewsletter(extractedData, mediaLinks, feedback, "formal");
      setMarkdown(res.markdown);
      setFeedback("");
    } catch (err) {
      alert("Regeneration failed: " + err.message);
    } finally {
      setRegenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <h2>Generating newsletter...</h2>
        <p>AI is crafting a professional investor update.</p>
        <div className="spinner" />
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Edit Newsletter</h2>
      <p className="subtitle">
        Edit the Markdown on the left — live preview on the right
      </p>

      <div className="editor-container">
        <div className="editor-pane">
          <div className="pane-label">Markdown Editor</div>
          <textarea
            value={markdown}
            onChange={(e) => setMarkdown(e.target.value)}
          />
        </div>
        <div>
          <div className="pane-label">Live Preview</div>
          <div className="preview-pane">
            <ReactMarkdown
  components={{
    img: ({ src, alt }) => (
      <img
        src={src}
        alt={alt || ""}
        style={{ maxWidth: "100%", borderRadius: 8 }}
        onError={(e) => { e.target.style.display = "none"; }}
      />
    ),
  }}
>{markdown}</ReactMarkdown>
          </div>
        </div>
      </div>

      {/* Regenerate with feedback */}
      <div className="regen-bar">
        <input
          type="text"
          placeholder='e.g. "Add more detail on financials" or "Make it shorter"'
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleRegenerate()}
        />
        <button
          className="btn btn-secondary"
          onClick={handleRegenerate}
          disabled={regenerating}
        >
          {regenerating ? "Regenerating..." : "Regenerate"}
        </button>
      </div>

      <div className="btn-row">
        <button className="btn btn-secondary" onClick={onBack}>Back</button>
        <button className="btn btn-primary" onClick={onComplete}>
          Continue to Export
        </button>
      </div>
    </div>
  );
}