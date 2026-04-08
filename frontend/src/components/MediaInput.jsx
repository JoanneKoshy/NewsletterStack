import { useState } from "react";
import { addMediaLink, uploadImage } from "../services/api";

export default function MediaInput({ mediaLinks, setMediaLinks, onComplete, onBack }) {
  const [url, setUrl] = useState("");
  const [title, setTitle] = useState("");
  const [linkType, setLinkType] = useState("youtube");
  const [adding, setAdding] = useState(false);

  const handleAddLink = async () => {
    if (!url.trim()) return;
    setAdding(true);
    try {
      const result = await addMediaLink(url, title, linkType);
      setMediaLinks((prev) => [...prev, { ...result, type: linkType }]);
      setUrl("");
      setTitle("");
    } catch (err) {
      alert("Failed to add link: " + err.message);
    } finally {
      setAdding(false);
    }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const caption = prompt("Enter a caption for this image (optional):", "") || "";
      const result = await uploadImage(file, caption);
      setMediaLinks((prev) => [
        ...prev,
        { type: "image", url: result.url, title: result.caption || file.name },
      ]);
    } catch (err) {
      alert("Failed to upload image: " + err.message);
    }
  };

  const removeMedia = (index) => {
    setMediaLinks((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="card">
      <h2>Add Media Content</h2>
      <p className="subtitle">
        Add YouTube links, social media posts, or images to include in the newsletter. This step is optional.
      </p>

      {/* Link input */}
      <div className="media-form">
        <select value={linkType} onChange={(e) => setLinkType(e.target.value)}>
          <option value="youtube">YouTube</option>
          <option value="twitter">Twitter/X</option>
          <option value="linkedin">LinkedIn</option>
          <option value="instagram">Instagram</option>
          <option value="other">Other</option>
        </select>
        <input
          type="url"
          placeholder="Paste link here..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAddLink()}
        />
        <button className="btn btn-primary" onClick={handleAddLink} disabled={adding}>
          Add
        </button>
      </div>

      {/* Optional title */}
      <input
        type="text"
        placeholder="Link title (optional)"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        style={{ marginBottom: 12 }}
      />

      {/* Image upload */}
      <div style={{ marginBottom: 16 }}>
        <label
          style={{ fontSize: 13, color: "#888", cursor: "pointer", textDecoration: "underline" }}
          onClick={() => document.getElementById("image-input").click()}
        >
          + Upload an image or infographic
        </label>
        <input
          id="image-input"
          type="file"
          accept="image/*"
          style={{ display: "none" }}
          onChange={handleImageUpload}
        />
      </div>

      {/* Added media list */}
      {mediaLinks.length > 0 && (
        <div>
          <h3 style={{ fontSize: 14, marginBottom: 8 }}>Added media:</h3>
          {mediaLinks.map((m, i) => (
            <div className="media-item" key={i}>
              <span className="media-type">{m.type}</span>
              <span className="media-url">{m.title || m.url}</span>
              <button className="remove-btn" onClick={() => removeMedia(i)}>Remove</button>
            </div>
          ))}
        </div>
      )}

      <div className="btn-row">
        <button className="btn btn-secondary" onClick={onBack}>Back</button>
        <button className="btn btn-primary" onClick={onComplete}>
          {mediaLinks.length > 0 ? "Continue with Media" : "Skip — No Media"}
        </button>
      </div>
    </div>
  );
}