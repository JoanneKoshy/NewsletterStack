import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

// Upload report files (PDF, DOCX)
export const uploadFiles = async (files) => {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  const { data } = await api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

// Extract data from uploaded reports using Groq
export const extractData = async (files) => {
  const { data } = await api.post("/extract", { files });
  return data;
};

// Add a media link (YouTube, social media, etc.)
export const addMediaLink = async (url, title, type) => {
  const { data } = await api.post("/media/link", { url, title, type });
  return data;
};

// Upload an image/infographic
export const uploadImage = async (file, caption) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("caption", caption);
  const { data } = await api.post("/media/image", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

// Generate newsletter markdown from extracted data + media
export const generateNewsletter = async (extractedData, mediaLinks, tone) => {
  const { data } = await api.post("/generate-newsletter", {
    extracted_data: extractedData,
    media_links: mediaLinks,
    tone: tone || "formal",
  });
  return data;
};

// Regenerate with feedback
export const regenerateNewsletter = async (extractedData, mediaLinks, feedback, tone) => {
  const { data } = await api.post("/regenerate-newsletter", {
    extracted_data: extractedData,
    media_links: mediaLinks,
    feedback,
    tone: tone || "formal",
  });
  return data;
};

// Export as markdown file download
export const exportMarkdown = async (markdown, filename) => {
  const response = await api.post(
    "/export-markdown",
    { markdown, filename },
    { responseType: "blob" }
  );
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `${filename || "newsletter"}.md`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};

// Export as PDF download
export const exportPDF = async (htmlContent, filename) => {
  const response = await api.post(
    "/export-pdf",
    { html_content: htmlContent, filename },
    { responseType: "blob" }
  );
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `${filename || "newsletter"}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};