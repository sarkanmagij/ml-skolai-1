import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.join(__dirname, "..");
const OUT = path.join(__dirname, "assignments");

/** @type {{ id: number; title: string; blurb: string; ipynb: string; pdf: string }[]} */
const MODULES = [
  {
    id: 1,
    title: "Exploratory data analysis",
    blurb: "Palmer Penguins — load, inspect, missing values, plots.",
    ipynb: "02_EDA_Penguins_assignment_unsolved.ipynb",
    pdf: "02_EDA_Penguins_assignment_unsolved.pdf",
  },
  {
    id: 2,
    title: "Linear regression",
    blurb: "Auto MPG — train/test split, metrics, coefficients.",
    ipynb: "05_LinearRegression_AutoMPG_unsolved.ipynb",
    pdf: "05_LinearRegression_AutoMPG_unsolved.pdf",
  },
  {
    id: 3,
    title: "Logistic regression",
    blurb: "Iris — scaling, confusion matrix, decision boundary.",
    ipynb: "06_LogisticRegression_Iris_unsolved.ipynb",
    pdf: "06_LogisticRegression_Iris_unsolved.pdf",
  },
  {
    id: 4,
    title: "Decision trees",
    blurb: "Wine dataset — train a tree, plot, feature importance.",
    ipynb: "07_decision_trees_exercise.ipynb",
    pdf: "07_decision_trees_exercise.pdf",
  },
  {
    id: 5,
    title: "Random Forest",
    blurb: "Sonar — rock vs mine classification.",
    ipynb: "08_Exercise_02_RandomForest_RockOrMine_UNSOLVED (1).ipynb",
    pdf: "08_Exercise_02_RandomForest_RockOrMine_UNSOLVED (1).pdf",
  },
  {
    id: 6,
    title: "XGBoost",
    blurb: "Iris — DMatrix API and sklearn classifier.",
    ipynb: "11_XGBoost_unsolved.ipynb",
    pdf: "11_XGBoost_unsolved.pdf",
  },
  {
    id: 7,
    title: "Gradient boosting compared",
    blurb: "XGBoost, LightGBM, CatBoost on bank marketing data.",
    ipynb: "GBM_Comparison_UNSOLVED.ipynb",
    pdf: "GBM_Comparison_UNSOLVED.pdf",
  },
  {
    id: 8,
    title: "K-means clustering",
    blurb: "Mall customers — elbow method, segments, silhouette.",
    ipynb: "09_k-means_unsolved.ipynb",
    pdf: "09_k-means_unsolved.pdf",
  },
  {
    id: 9,
    title: "Principal component analysis",
    blurb: "Penguins & wine — variance, 2D projection, reconstruction.",
    ipynb: "Exercise_PCA_Basics_UNSOLVED (1).ipynb",
    pdf: "Exercise_PCA_Basics_UNSOLVED (1).pdf",
  },
  {
    id: 10,
    title: "Prophet forecasting",
    blurb: "Microsoft stock — seasonality, future horizon, MAE.",
    ipynb: "13_Prophet_unsolved (1).ipynb",
    pdf: "13_Prophet_unsolved (1).pdf",
  },
];

function copySafe(src, dest) {
  if (!fs.existsSync(src)) {
    console.warn(`Missing (skip): ${src}`);
    return false;
  }
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
  return true;
}

fs.rmSync(OUT, { recursive: true, force: true });

const manifest = [];

for (const m of MODULES) {
  const srcDir = path.join(REPO_ROOT, String(m.id));
  const ipynbSrc = path.join(srcDir, m.ipynb);
  const pdfSrc = path.join(srcDir, m.pdf);
  const destDir = path.join(OUT, String(m.id));
  const ipynbDest = path.join(destDir, m.ipynb);
  const pdfDest = path.join(destDir, m.pdf);

  const hasIpynb = copySafe(ipynbSrc, ipynbDest);
  const hasPdf = copySafe(pdfSrc, pdfDest);

  const ipynbHref = hasIpynb
    ? `/assignments/${m.id}/${encodeURIComponent(m.ipynb)}`
    : null;
  const pdfHref = hasPdf ? `/assignments/${m.id}/${encodeURIComponent(m.pdf)}` : null;

  manifest.push({
    id: m.id,
    title: m.title,
    blurb: m.blurb,
    ipynb: ipynbHref,
    pdf: pdfHref,
  });
}

fs.writeFileSync(path.join(__dirname, "manifest.json"), JSON.stringify(manifest, null, 2));

const cards = manifest
  .map((row) => {
    const ipynbBtn = row.ipynb
      ? `<a class="btn btn-ipynb" href="${row.ipynb}" download>Download .ipynb</a>`
      : `<span class="btn btn-disabled">Notebook missing — run build locally</span>`;
    const pdfBtn = row.pdf
      ? `<a class="btn btn-pdf" href="${row.pdf}" download>Download PDF</a>`
      : `<span class="btn btn-disabled">PDF missing — export locally</span>`;

    const nbviewerBtn = row.ipynb
      ? `<a class="btn btn-viewer" data-nb-path="${row.ipynb}" href="https://nbviewer.org/" target="_blank" rel="noopener noreferrer">View notebook online</a>`
      : "";

    const pdfPreview = row.pdf
      ? `<details class="preview-details">
      <summary class="preview-summary">Preview — PDF (exported with outputs). Click to expand.</summary>
      <div class="preview-shell" role="region" aria-label="Embedded PDF preview">
        <iframe class="preview-iframe" src="${row.pdf}#view=FitH" title="PDF preview for module ${row.id}" loading="lazy"></iframe>
      </div>
      <p class="preview-meta"><a href="${row.pdf}" target="_blank" rel="noopener">Open PDF in a new tab</a> if the embed does not load.</p>
    </details>`
      : `<div class="preview-fallback" role="note">
      <p><strong>No PDF on disk.</strong> Use <em>View notebook online</em> after deploy, or download the <code>.ipynb</code> and open in Jupyter.</p>
    </div>`;

    return `
    <article class="module" id="module-${row.id}">
      <header class="module-head">
        <span class="module-num">${String(row.id).padStart(2, "0")}</span>
        <div>
          <h2>${escapeHtml(row.title)}</h2>
          <p class="module-blurb">${escapeHtml(row.blurb)}</p>
        </div>
      </header>
      ${pdfPreview}
      <div class="module-actions">
        ${ipynbBtn}
        ${pdfBtn}
        ${nbviewerBtn}
      </div>
    </article>`;
  })
  .join("\n");

const nav = manifest
  .map(
    (row) =>
      `<a class="nav-link" href="#module-${row.id}">${String(row.id).padStart(2, "0")}</a>`
  )
  .join("");

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ML course — notebooks & PDFs</title>
  <link rel="stylesheet" href="/styles.css" />
  <script src="/preview.js" defer></script>
</head>
<body>
  <header class="site-header">
    <div class="inner">
      <h1>Machine learning — course materials</h1>
      <p class="tagline">Ten modules with Jupyter notebooks and PDF exports. Each section includes an embedded PDF preview and an optional online notebook viewer. Jump to a module below.</p>
      <nav class="toc" aria-label="Modules">${nav}</nav>
    </div>
  </header>
  <main class="inner">
    ${cards}
  </main>
  <footer class="site-footer inner">
    <p>Made with ❤️, more or less automatically.</p>
  </footer>
</body>
</html>`;

fs.writeFileSync(path.join(__dirname, "index.html"), html);
console.log("Wrote index.html, manifest.json, and copied files under assignments/");

function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
