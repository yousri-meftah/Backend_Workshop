window.API_BASE = "";

window.apiUrl = function apiUrl(path) {
  return `${window.API_BASE}${path}`;
};
