for (const remote of ["account", "search", "report"]) {
  fetch(`/fragments/${remote}.html`)
    .then(response => response.text())
    .then(markup => document.getElementById(remote).innerHTML = markup);
}

