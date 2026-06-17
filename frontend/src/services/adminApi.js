const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || "";

async function request(path, token, options = {}) {
  const headers = {
    Authorization: `Bearer ${token}`,
    ...(options.body ? { "Content-Type": "application/json" } : {}),
  };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
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

export function getAdminTreks(token) {
  return request("/admin/treks", token);
}

export function createAdminTrek(token, trek) {
  return request("/admin/treks", token, {
    method: "POST",
    body: JSON.stringify(trek),
  });
}

export function deleteAdminTrek(token, trekId) {
  return request(`/admin/treks/${trekId}`, token, {
    method: "DELETE",
  });
}

export function getAdminUsers(token, role) {
  return request(`/admin/users${role ? `?role=${encodeURIComponent(role)}` : ""}`, token);
}

export function createAdminStaff(token, staff) {
  return request("/admin/staff", token, {
    method: "POST",
    body: JSON.stringify(staff),
  });
}

export function assignStaffToTrek(token, trekId, staffId) {
  return request(`/admin/treks/${trekId}/assign_staff`, token, {
    method: "PUT",
    body: JSON.stringify({ staff_id: staffId }),
  });
}

export function getAdminBookings(token) {
  return request("/admin/bookings", token);
}

export function searchAdminUsers(token, query) {
  return request(`/admin/search/users?q=${encodeURIComponent(query)}`, token);
}

export function searchAdminStaff(token, query) {
  return request(`/admin/search/staff?q=${encodeURIComponent(query)}`, token);
}

export function searchAdminTreks(token, query) {
  return request(`/admin/search/treks?q=${encodeURIComponent(query)}`, token);
}

export function deactivateAdminUser(token, userId) {
  return request(`/admin/users/${userId}/deactivate`, token, { method: "PUT" });
}

export function activateAdminUser(token, userId) {
  return request(`/admin/users/${userId}/activate`, token, { method: "PUT" });
}
