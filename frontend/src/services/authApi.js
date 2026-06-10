const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || "";

async function request(path, payload) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong. Please try again.");
  }

  return data;
}

export function loginUser(credentials) {
  return request("/auth/login", credentials);
}

export function registerUser(details) {
  return request("/auth/register", details);
}
