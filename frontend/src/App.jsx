import { useState } from "react";
import FileUpload from "./components/FileUpload";
import ExtractionPreview from "./components/ExtractionPreview";
import MediaInput from "./components/MediaInput";
import NewsletterEditor from "./components/NewsletterEditor";
import ExportPanel from "./components/ExportPanel";

const STEPS = ["upload", "extract", "media", "edit", "export"];

export default function App() {
  const [step, setStep] = useState("upload");
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [extractedData, setExtractedData] = useState(null);
  const [mediaLinks, setMediaLinks] = useState([]);
  const [markdown, setMarkdown] = useState("");

  return (
    <div>
      <header className="app-header">
        <h1>Investor Newsletter Tool</h1>
        <div className="steps-bar">
          {STEPS.map((s, i) => (
            <span
              key={s}
              className={`step-label ${step === s ? "active" : ""}`}
            >
              {i + 1}. {s}
            </span>
          ))}
        </div>
      </header>

      <main className="main-content">
        {step === "upload" && (
          <FileUpload
            onComplete={(files) => {
              setUploadedFiles(files);
              setStep("extract");
            }}
          />
        )}

        {step === "extract" && (
          <ExtractionPreview
            files={uploadedFiles}
            onComplete={(data) => {
              setExtractedData(data);
              setStep("media");
            }}
            onBack={() => setStep("upload")}
          />
        )}

        {step === "media" && (
          <MediaInput
            mediaLinks={mediaLinks}
            setMediaLinks={setMediaLinks}
            onComplete={() => setStep("edit")}
            onBack={() => setStep("extract")}
          />
        )}

        {step === "edit" && (
          <NewsletterEditor
            extractedData={extractedData}
            mediaLinks={mediaLinks}
            markdown={markdown}
            setMarkdown={setMarkdown}
            onComplete={() => setStep("export")}
            onBack={() => setStep("media")}
          />
        )}

        {step === "export" && (
          <ExportPanel
            markdown={markdown}
            onBack={() => setStep("edit")}
            onReset={() => {
              setStep("upload");
              setUploadedFiles([]);
              setExtractedData(null);
              setMediaLinks([]);
              setMarkdown("");
            }}
          />
        )}
      </main>
    </div>
  );
}