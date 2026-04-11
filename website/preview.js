/**
 * Jupyter nbviewer needs an absolute HTTPS URL to the .ipynb file.
 * Resolves data-nb-path links at runtime so previews work on any host (Vercel preview, custom domain, localhost).
 */
document.addEventListener("DOMContentLoaded", () => {
  const origin = window.location.origin;
  document.querySelectorAll("a[data-nb-path]").forEach((el) => {
    const p = el.getAttribute("data-nb-path");
    if (!p) return;
    const absolute = origin + p;
    el.href = "https://nbviewer.org/url/" + encodeURIComponent(absolute);
  });
});
