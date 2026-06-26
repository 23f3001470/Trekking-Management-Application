const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || "";

async function request(path, token, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...(options.headers || {}),
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong. Please try again.");
  }

  return data;
}

export function getStaffDashboard(token) {
  return request("/staff/dashboard", token);
}

export function updateStaffTrek(token, trekId, payload) {
  return request(`/staff/treks/${trekId}`, token, {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}

export function getTrekParticipants(token, trekId) {
  return request(`/staff/treks/${trekId}/participants`, token);
}

export function updateParticipantStatus(token, trekId, bookingId, status) {
  return request(`/staff/treks/${trekId}/participants/${bookingId}/status`, token, {
    method: "PUT",
    body: JSON.stringify({ status })
  });
}

export function startStaffTrek(token, trekId) {
  return request(`/staff/treks/${trekId}/start`, token, { method: "PUT" });
}

export function completeStaffTrek(token, trekId) {
  return request(`/staff/treks/${trekId}/complete`, token, { method: "PUT" });
}
