import { execSync } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.join(__dirname, "..");
const OUT = path.join(__dirname, "assignments");

/**
 * Link to the notebook on GitHub (blob URL). GitHub renders .ipynb in the browser.
 * Nbviewer + deployment URL or raw.githubusercontent.com often 404 (private repo, or
 * nbviewer fetch failures). The blob page works for public repos; private repos need login.
 */
function getGithubContext() {
  const owner = process.env.VERCEL_GIT_REPO_OWNER;
  const slug = process.env.VERCEL_GIT_REPO_SLUG;
  const ref = process.env.VERCEL_GIT_COMMIT_REF || "main";
  if (owner && slug) {
    return { owner, slug, ref };
  }
  try {
    const url = execSync("git config --get remote.origin.url", {
      encoding: "utf-8",
      cwd: REPO_ROOT,
    }).trim();
    const m = url.match(/github\.com[:/]([^/]+)\/(.+?)(?:\.git)?$/i);
    if (!m) return null;
    let repoSlug = m[2].trim();
    if (repoSlug.endsWith(".git")) repoSlug = repoSlug.slice(0, -4);
    const branch = execSync("git rev-parse --abbrev-ref HEAD", {
      encoding: "utf-8",
      cwd: REPO_ROOT,
    }).trim();
    return { owner: m[1].trim(), slug: repoSlug, ref: branch };
  } catch {
    return null;
  }
}

/** @param {{ id: number|string; ipynb: string }} m @param {{ owner: string; slug: string; ref: string }} ctx */
function githubBlobIpynbUrl(m, ctx) {
  const fileEnc = encodeURIComponent(m.ipynb);
  return `https://github.com/${ctx.owner}/${ctx.slug}/blob/${ctx.ref}/${m.id}/${fileEnc}`;
}

function escapeAttr(s) {
  return s.replace(/&/g, "&amp;").replace(/"/g, "&quot;");
}

const githubCtx = getGithubContext();
if (!githubCtx) {
  console.warn(
    "No GitHub repo context (set VERCEL_GIT_* or run from a git clone with github.com remote). Omitting 'View on GitHub' links."
  );
}

/** @type {{ id: number|string; level: string; title: string; blurb: string; ipynb: string; pdf: string }[]} */
const MODULES = [
  // ML1 — Classical Machine Learning
  {
    id: 1,
    level: "ML1",
    title: "Exploratory data analysis",
    blurb: "Palmer Penguins — load, inspect, missing values, plots.",
    ipynb: "02_EDA_Penguins_assignment_unsolved.ipynb",
    pdf: "02_EDA_Penguins_assignment_unsolved.pdf",
  },
  {
    id: 2,
    level: "ML1",
    title: "Linear regression",
    blurb: "Auto MPG — train/test split, metrics, coefficients.",
    ipynb: "05_LinearRegression_AutoMPG_unsolved.ipynb",
    pdf: "05_LinearRegression_AutoMPG_unsolved.pdf",
  },
  {
    id: 3,
    level: "ML1",
    title: "Logistic regression",
    blurb: "Iris — scaling, confusion matrix, decision boundary.",
    ipynb: "06_LogisticRegression_Iris_unsolved.ipynb",
    pdf: "06_LogisticRegression_Iris_unsolved.pdf",
  },
  {
    id: 4,
    level: "ML1",
    title: "Decision trees",
    blurb: "Wine dataset — train a tree, plot, feature importance.",
    ipynb: "07_decision_trees_exercise.ipynb",
    pdf: "07_decision_trees_exercise.pdf",
  },
  {
    id: 5,
    level: "ML1",
    title: "Random Forest",
    blurb: "Sonar — rock vs mine classification.",
    ipynb: "08_Exercise_02_RandomForest_RockOrMine_UNSOLVED (1).ipynb",
    pdf: "08_Exercise_02_RandomForest_RockOrMine_UNSOLVED (1).pdf",
  },
  {
    id: 6,
    level: "ML1",
    title: "XGBoost",
    blurb: "Iris — DMatrix API and sklearn classifier.",
    ipynb: "11_XGBoost_unsolved.ipynb",
    pdf: "11_XGBoost_unsolved.pdf",
  },
  {
    id: 7,
    level: "ML1",
    title: "Gradient boosting compared",
    blurb: "XGBoost, LightGBM, CatBoost on bank marketing data.",
    ipynb: "GBM_Comparison_UNSOLVED.ipynb",
    pdf: "GBM_Comparison_UNSOLVED.pdf",
  },
  {
    id: 8,
    level: "ML1",
    title: "K-means clustering",
    blurb: "Mall customers — elbow method, segments, silhouette.",
    ipynb: "09_k-means_unsolved.ipynb",
    pdf: "09_k-means_unsolved.pdf",
  },
  {
    id: 9,
    level: "ML1",
    title: "Principal component analysis",
    blurb: "Penguins & wine — variance, 2D projection, reconstruction.",
    ipynb: "Exercise_PCA_Basics_UNSOLVED (1).ipynb",
    pdf: "Exercise_PCA_Basics_UNSOLVED (1).pdf",
  },
  {
    id: 10,
    level: "ML1",
    title: "Prophet forecasting",
    blurb: "Microsoft stock — seasonality, future horizon, MAE.",
    ipynb: "13_Prophet_unsolved (1).ipynb",
    pdf: "13_Prophet_unsolved (1).pdf",
  },

  // ML2 — Deep Learning
  {
    id: "2.1",
    level: "ML2",
    title: "Intro to PyTorch",
    blurb: "Tensors, autograd, and training a model with PyTorch.",
    ipynb: "igors_02_Intro_to_pytorch_UNSOLVED (1)_solved.ipynb",
    pdf: "igors_02_Intro_to_pytorch_UNSOLVED (1)_solved.pdf",
  },
  {
    id: "2.2",
    level: "ML2",
    title: "Simple neural network",
    blurb: "Build and train a feedforward network in PyTorch.",
    ipynb: "igors_03_Simple_Neural_Network_Exercise_UNSOLVED_solved.ipynb",
    pdf: "igors_03_Simple_Neural_Network_Exercise_UNSOLVED_solved.pdf",
  },
  {
    id: "2.3",
    level: "ML2",
    title: "Regularization & optimization",
    blurb: "Dropout, batch norm, and learning rate schedulers.",
    ipynb: "igors_04_Regularization_and_Optimization_Exercise_UNSOLVED_solved.ipynb",
    pdf: "igors_04_Regularization_and_Optimization_Exercise_UNSOLVED_solved.pdf",
  },
  {
    id: "2.4",
    level: "ML2",
    title: "CIFAR-10 CNN",
    blurb: "Convolutional neural network for image classification.",
    ipynb: "igors_05_cifar10_cnn_unsolved_solved.ipynb",
    pdf: "igors_05_cifar10_cnn_unsolved_solved.pdf",
  },
  {
    id: "2.5",
    level: "ML2",
    title: "Sales forecasting (LSTM)",
    blurb: "LSTM for sequence-based time-series prediction.",
    ipynb: "igors_07_Sales_Forecasting_with_LSTM_unsolved_solved.ipynb",
    pdf: "igors_07_Sales_Forecasting_with_LSTM_unsolved_solved.pdf",
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
    level: m.level,
    title: m.title,
    blurb: m.blurb,
    ipynb: ipynbHref,
    pdf: pdfHref,
  });
}

fs.writeFileSync(path.join(__dirname, "manifest.json"), JSON.stringify(manifest, null, 2));

const moduleById = new Map(MODULES.map((m) => [m.id, m]));

const cards = manifest
  .map((row) => {
    const ipynbBtn = row.ipynb
      ? `<a class="btn btn-ipynb" href="${row.ipynb}" download>Download .ipynb</a>`
      : `<span class="btn btn-disabled">Notebook missing — run build locally</span>`;
    const pdfBtn = row.pdf
      ? `<a class="btn btn-pdf" href="${row.pdf}" download>Download PDF</a>`
      : `<span class="btn btn-disabled">PDF missing — export locally</span>`;

    const mod = moduleById.get(row.id);
    let nbviewerBtn = "";
    if (row.ipynb && githubCtx && mod) {
      const viewUrl = githubBlobIpynbUrl(mod, githubCtx);
      nbviewerBtn = `<a class="btn btn-viewer" href="${escapeAttr(viewUrl)}" target="_blank" rel="noopener noreferrer">View on GitHub</a>`;
    }

    const pdfPreview = row.pdf
      ? `<details class="preview-details">
      <summary class="preview-summary">Preview — PDF (exported with outputs). Click to expand.</summary>
      <div class="preview-shell" role="region" aria-label="Embedded PDF preview">
        <iframe class="preview-iframe" src="${row.pdf}#view=FitH" title="PDF preview for module ${row.id}" loading="lazy"></iframe>
      </div>
      <p class="preview-meta"><a href="${row.pdf}" target="_blank" rel="noopener">Open PDF in a new tab</a> if the embed does not load.</p>
    </details>`
      : `<div class="preview-fallback" role="note">
      <p><strong>No PDF on disk.</strong> Download the <code>.ipynb</code> or use the online viewer when available.</p>
    </div>`;

    return `
    <article class="module" id="module-${row.id}" data-level="${row.level}">
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
      `<a class="nav-link" href="#module-${row.id}" data-level="${row.level}">${String(row.id).padStart(2, "0")}</a>`
  )
  .join("");

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ML course — notebooks & PDFs</title>
  <link rel="stylesheet" href="/styles.css" />
</head>
<body>
  <header class="site-header">
    <div class="inner">
      <h1>Machine learning — course materials</h1>
      <p class="tagline">Fifteen modules across two levels. ML1 covers classical machine learning; ML2 goes deeper into neural networks and PyTorch. Each section includes a PDF preview and a link to view the notebook on GitHub.</p>
      <div class="filter-bar" role="group" aria-label="Filter by level">
        <button class="filter-btn active" data-filter="all">All</button>
        <button class="filter-btn" data-filter="ML1">ML1</button>
        <button class="filter-btn" data-filter="ML2">ML2</button>
      </div>
      <nav class="toc" aria-label="Modules">${nav}</nav>
    </div>
  </header>
  <main class="inner">
    ${cards}
  </main>
  <footer class="site-footer inner">
    <p>Made with ❤️, more or less automatically.</p>
  </footer>
  <script>
    (function () {
      var btns = document.querySelectorAll('.filter-btn');
      btns.forEach(function (btn) {
        btn.addEventListener('click', function () {
          btns.forEach(function (b) { b.classList.remove('active'); });
          btn.classList.add('active');
          var filter = btn.dataset.filter;
          document.querySelectorAll('[data-level]').forEach(function (el) {
            el.style.display = (filter === 'all' || el.dataset.level === filter) ? '' : 'none';
          });
        });
      });
    })();
  </script>
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
