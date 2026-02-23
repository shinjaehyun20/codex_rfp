"use client";

import { useState } from "react";

export function DropzoneUpload({ onUpload }: { onUpload: (files: File[]) => Promise<void> }) {
  const [files, setFiles] = useState<File[]>([]);

  return (
    <div className="card">
      <div className="card-header">문서 업로드 (pdf/hwp/hwpx/docx)</div>
      <div className="card-body" style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
        <input
          type="file"
          multiple
          accept=".pdf,.hwp,.hwpx,.docx"
          onChange={(e) => setFiles(Array.from(e.target.files ?? []))}
        />
        <button className="button" onClick={() => onUpload(files)} disabled={files.length === 0}>
          Upload
        </button>
      </div>
    </div>
  );
}
