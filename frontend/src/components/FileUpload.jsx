import { useState, useCallback } from "react";
import { uploadFiles } from "../services/api";

export default function FileUpload({ onComplete }) {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragActive(false);
    const dropped = Array.from(e.dataTransfer.files).filter((f) =>
      [".pdf", ".docx", ".doc", ".txt"].some((ext) =>
        f.name.toLowerCase().endsWith(ext)
      )
    );
    setFiles((prev) => [...prev, ...dropped]);
  }, []);

  const handleFileSelect = (e) => {
    setFiles((prev) => [...prev, ...Array.from(e.target.files)]);
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    setUploading(true);
    try {
      const result = await uploadFiles(files);
      onComplete(result.files);
    } catch (err) {
      alert("Upload failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card">
      <h2>Upload Reports</h2>
      <p className="subtitle">
        Upload weekly/monthly reports — MIS, Management Info, EOW reports (PDF or DOCX)
      </p>

      <div
        className={`dropzone ${dragActive ? "active" : ""}`}
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        onClick={() => document.getElementById("file-input").click()}
      >
        <p>Drag & drop files here, or click to browse</p>
        <input
          id="file-input"
          type="file"
          multiple
          accept=".pdf,.docx,.doc,.txt"
          style={{ display: "none" }}
          onChange={handleFileSelect}
        />
      </div>

      {files.length > 0 && (
        <div style={{ marginTop: 16 }}>
          {files.map((f, i) => (
            <div className="file-item" key={i}>
              <span>{f.name}</span>
              <button
                className="remove-btn"
                onClick={() => setFiles(files.filter((_, j) => j !== i))}
              >
                Remove
              </button>
            </div>
          ))}

          <div className="btn-row">
            <button
              className="btn btn-primary"
              onClick={handleUpload}
              disabled={uploading}
            >
              {uploading ? "Uploading..." : "Upload & Extract"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}