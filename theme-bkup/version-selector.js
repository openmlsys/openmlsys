// Version and Language selector for OpenMLSys mdbook
(function () {
  "use strict";

  var path = window.location.pathname;

  // Detect current version and language from URL
  var currentVersion = "v2";
  var currentLang = "en";

  if (path.match(/\/v1(\/|$)/)) {
    currentVersion = "v1";
  }
  if (path.match(/\/cn(\/|$)/)) {
    currentLang = "zh";
  }

  // Build base paths — always navigate to root of target version
  function basePath(version, lang) {
    // Determine site root: everything before /v1/, /cn/, or first path segment after /docs/
    var root = "/";
    var docsMatch = path.match(/^(\/docs\/)/);
    if (docsMatch) root = docsMatch[1];

    var p = root;
    if (version === "v1") p += "v1/";
    if (lang === "zh") p += "cn/";
    return p;
  }

  var container = document.createElement("span");
  container.className = "openmlsys-nav-selectors";

  // --- Version links: V1 | V2 ---
  var versions = [
    { label: "V1", value: "v1" },
    { label: "V2", value: "v2" },
  ];

  versions.forEach(function (v) {
    var a = document.createElement("a");
    a.className = "openmlsys-selector-link";
    a.textContent = v.label;
    a.href = basePath(v.value, currentLang);
    if (v.value === currentVersion) a.classList.add("active");
    container.appendChild(a);
  });

  // Separator
  var sep = document.createElement("span");
  sep.className = "openmlsys-selector-sep";
  container.appendChild(sep);

  // --- Language toggle: single button that switches to the other language ---
  var otherLang = currentLang === "zh" ? "en" : "zh";
  var langLink = document.createElement("a");
  langLink.className = "openmlsys-selector-link";
  langLink.textContent = currentLang === "zh" ? "EN" : "ZH";
  langLink.href = basePath(currentVersion, otherLang);
  container.appendChild(langLink);

  // Insert into .right-buttons, before existing icons
  function insertSelector() {
    var rightButtons = document.querySelector(".right-buttons");
    if (rightButtons) {
      rightButtons.insertBefore(container, rightButtons.firstChild);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", insertSelector);
  } else {
    insertSelector();
  }
})();
