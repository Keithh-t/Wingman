import { createContext, useContext, useEffect, useState } from "react";
import type { MeResponse } from "../api/apiClient";
import {login as apiLogin, register as apiRegister, fetchMe, logout as apiLogout} from "../api/apiClient";

type AuthState = {
  user: MeResponse | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<MeResponse | null>(null);
  const [loading, setLoading] = useState(true);

  // refresh user on mount from cookie
  useEffect(() => {
    (async () => {
      try {
        const me = await fetchMe();
        setUser(me);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

    const login = async (email: string, password: string) => {
    await apiLogin({ email, password });
    const me = await fetchMe();
    setUser(me);
  };

  const register = async (email: string, username: string, password: string) => {
    await apiRegister({ email, username, password });
    const me = await fetchMe();
    setUser(me);
  };

  const logout = async () => {
    await apiLogout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
