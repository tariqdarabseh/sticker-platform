'use client';

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://54.166.169.154";

export default function Home() {
  const [health, setHealth] = useState<string>("loading...");

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((r) => r.ok ? r.text() : Promise.reject(new Error(`HTTP ${r.status}`)))
      .then((t) => setHealth(t))
      .catch((e) => setHealth(`error: ${e.message}`));
  }, []);

  return (
    <main style={{ maxWidth: 900, margin: "40px auto", fontFamily: "system-ui" }}>
      <h1 style={{ fontSize: 32, marginBottom: 8 }}>Sticker Platform</h1>
      <p style={{ marginTop: 0, opacity: 0.8 }}>
        API Health: <b>{health}</b>
      </p>

      <hr style={{ margin: "24px 0" }} />

      <h2 style={{ fontSize: 20 }}>Gallery (placeholder)</h2>
      <p style={{ opacity: 0.8 }}>
        لاحقاً رح نجيب الصور من API/DB/S3. هسا بس إثبات إن الفرونت يشتغل ويحكي مع الباك.
      </p>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))",
        gap: 12
      }}>
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} style={{
            border: "1px solid #ddd",
            borderRadius: 12,
            padding: 12
          }}>
            <div style={{
              height: 120,
              background: "#f5f5f5",
              borderRadius: 10,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#777"
            }}>
              Image {i + 1}
            </div>
            <div style={{ marginTop: 10 }}>
              <b>Sticker #{i + 1}</b>
              <div style={{ opacity: 0.8 }}>Price: {Math.floor(3 + i)} JOD</div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
