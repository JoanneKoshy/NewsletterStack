import { useState, useEffect } from "react";
import { extractData } from "../services/api";

export default function ExtractionPreview({ files, onComplete, onBack }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const run = async () => {
      try {
        const result = await extractData(files);
        setData(result.extracted_data);
      } catch (err) {
        setError(err.response?.data?.detail || err.message);
      } finally {
        setLoading(false);
      }
    };
    run();
  }, []);

  if (loading) {
    return (
      <div className="loading">
        <h2>Extracting data from reports...</h2>
        <p>AI is reading your reports and pulling out key information.</p>
        <div className="spinner" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <h2>Extraction Failed</h2>
        <p style={{ color: "#c0392b" }}>{error}</p>
        <div className="btn-row">
          <button className="btn btn-secondary" onClick={onBack}>Go Back</button>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Extracted Data</h2>
      <p className="subtitle">Review what the AI pulled from your reports</p>

      {data?.raw_summary && (
        <div className="data-section">
          <h3>Executive Summary</h3>
          <p style={{ fontSize: 14 }}>{data.raw_summary}</p>
        </div>
      )}

      {data?.financial_highlights && (
        <div className="data-section">
          <h3>Financial Highlights</h3>
          <table className="data-table">
            <tbody>
              {Object.entries(data.financial_highlights)
                .filter(([k, v]) => v && k !== "other_metrics")
                .map(([key, val]) => (
                  <tr key={key}>
                    <td>{key.replace(/_/g, " ")}</td>
                    <td>{val}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}

      {data?.key_wins?.length > 0 && (
        <div className="data-section">
          <h3>Key Wins</h3>
          <ul>{data.key_wins.map((w, i) => <li key={i}>{w}</li>)}</ul>
        </div>
      )}

      {data?.progress_updates?.length > 0 && (
        <div className="data-section">
          <h3>Progress Updates</h3>
          <ul>{data.progress_updates.map((p, i) => <li key={i}>{p}</li>)}</ul>
        </div>
      )}

      {data?.new_hires?.length > 0 && (
        <div className="data-section">
          <h3>New Hires</h3>
          <ul>{data.new_hires.map((h, i) => <li key={i}>{h}</li>)}</ul>
        </div>
      )}

      {data?.challenges?.length > 0 && (
        <div className="data-section">
          <h3>Challenges</h3>
          <ul>{data.challenges.map((c, i) => <li key={i}>{c}</li>)}</ul>
        </div>
      )}

      <div className="btn-row">
        <button className="btn btn-secondary" onClick={onBack}>Back</button>
        <button className="btn btn-primary" onClick={() => onComplete(data)}>
          Continue
        </button>
      </div>
    </div>
  );
}