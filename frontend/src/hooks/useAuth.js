import { useState, useEffect } from "react";
import { getUser, logout as doLogout } from "../utils/auth";

export function useAuth() {
  const [user, setUser] = useState(getUser);

  const logout = () => {
    doLogout();
    setUser(null);
    window.location.href = "/login";
  };

  return { user, setUser, logout };
}
