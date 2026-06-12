export function getStoredSession() {
  return {
    token: localStorage.getItem("tma_token") || "",
    user: JSON.parse(localStorage.getItem("tma_user") || "null"),
  };
}

export function setStoredSession(token, user) {
  localStorage.setItem("tma_token", token);
  localStorage.setItem("tma_user", JSON.stringify(user));
}

export function clearStoredSession() {
  localStorage.removeItem("tma_token");
  localStorage.removeItem("tma_user");
}
