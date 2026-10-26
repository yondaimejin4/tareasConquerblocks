/** En desarrollo: proxy Vite (URL vacia). En produccion: VITE_API_BASE_URL. */
function resolveApiBase() {
  const fromEnv = import.meta.env.VITE_API_BASE_URL?.trim();
  if (import.meta.env.DEV) {
    return fromEnv || "";
  }
  /* Build servido por Django en :8000 → misma origen, sin CORS */
  return fromEnv || "";
}

export const API_BASE_URL = resolveApiBase();

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(";").shift();
  }
  return null;
}

export async function ensureCsrf() {
  await fetch(`${API_BASE_URL}/api/auth/csrf/`, { credentials: "include" });
}

export async function apiFetch(path, options = {}) {
  const headers = { ...options.headers };
  const hasBody = options.body !== undefined && options.body !== null;

  if (hasBody && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const method = (options.method || "GET").toUpperCase();
  if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
    const token = getCookie("csrftoken");
    if (token) {
      headers["X-CSRFToken"] = token;
    }
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
    credentials: "include",
  });

  let data = null;
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    data = await response.json();
  }

  return { response, data };
}

export async function fetchServices() {
  const [allRes, featuredRes] = await Promise.all([
    fetch(`${API_BASE_URL}/api/services/`),
    fetch(`${API_BASE_URL}/api/services/featured/`),
  ]);

  if (!allRes.ok || !featuredRes.ok) {
    throw new Error(`API error ${allRes.status}/${featuredRes.status}`);
  }

  const services = await allRes.json();
  const featured = await featuredRes.json();

  if (!Array.isArray(services) || !Array.isArray(featured)) {
    throw new Error("Invalid API response");
  }

  return { services, featured };
}
