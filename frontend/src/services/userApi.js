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

export function getUserDashboard(token) {
  return request("/user/dashboard", token);
}

export function getUserTreks(token) {
  return request("/user/treks", token);
}

export function bookTrek(token, trekId, payload = {}) {
  return request(`/user/treks/${trekId}/book`, token, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getUserBookings(token) {
  return request("/user/bookings", token);
}

export function getBookingDetails(token, bookingId) {
  return request(`/user/bookings/${bookingId}`, token);
}

export function getUserHistory(token) {
  return request("/user/history", token);
}

export function updateProfile(token, payload) {
  return request("/user/profile", token, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function searchUserTreks(token, query) {
  return request(`/user/treks/search?q=${encodeURIComponent(query)}`, token);
}
