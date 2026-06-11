const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || "";

async function request(path, token) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong. Please try again.");
  }

  return data;
}

export function getAdminDashboard(token) {
  return request("/admin/dashboard", token);
}
