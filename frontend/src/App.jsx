import React, { useState } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [fontUrl, setFontUrl] = useState(null);
  const [fontName, setFontName] = useState("MyHandwritingFont");
  const [previewText, setPreviewText] = useState(
    "The quick brown fox jumps over the lazy dog."
  );

  const BACKEND_URL = "https://hw-font-api.onrender.com";

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setStatus("Uploading and generating font... This may take 10-60s.");
    setFontUrl(null);

    const fd = new FormData();
    fd.append("sheet", file);
    fd.append("font_name", fontName);

    try {
      const res = await fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: fd,
      });

      if (!res.ok) {
        const err = await res.json();
        setStatus("Error: " + (err.error || JSON.stringify(err)));
        return;
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setFontUrl(url);

      const styleId = "user-font-style";
      let styleEl = document.getElementById(styleId);
      if (!styleEl) {
        styleEl = document.createElement("style");
        styleEl.id = styleId;
        document.head.appendChild(styleEl);
      }
      styleEl.innerHTML = `@font-face { font-family: 'UserHandFont'; src: url(${url}); }`;

      setStatus("Font ready! Scroll down to preview & download.");
    } catch (err) {
      setStatus("Upload failed: " + String(err));
    }
  };

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: 24 }}>
      <h1>Handwriting → Font (MVP)</h1>

      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files?.[0])}
        />
        <div style={{ marginTop: 8 }}>
          <label>Font name: </label>
          <input
            value={fontName}
            onChange={(e) => setFontName(e.target.value)}
          />
        </div>
        <button style={{ marginTop: 12 }} type="submit">
          Upload & Generate
        </button>
      </form>

      <p>{status}</p>

      {fontUrl && (
        <>
          <h2>Preview</h2>
          <textarea
            style={{
              fontFamily: "UserHandFont, sans-serif",
              fontSize: 20,
              width: "100%",
              height: 120,
            }}
            value={previewText}
            onChange={(e) => setPreviewText(e.target.value)}
          />
          <div style={{ marginTop: 12 }}>
            <a href={fontUrl} download={`${fontName}.ttf`}>
              Download .ttf
            </a>
          </div>
        </>
      )}
    </div>
  );
}
