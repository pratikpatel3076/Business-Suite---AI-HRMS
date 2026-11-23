import { create } from "zustand";

export interface AuthUser {
  id: number;
  email: string;
  role: string | null;
  is_superuser: boolean;
  employee_id?: number | null;
}

interface AuthState {
  accessToken: string | null;
  user: AuthUser | null;
  isAuthenticated: boolean;
  isHydrated: boolean;
  setAccessToken: (accessToken: string) => void;
  setUser: (user: AuthUser) => void;
  logout: () => void;
  setHydrated: (isHydrated: boolean) => void;
}

// No persist middleware: the access token lives in memory only and the
// refresh token is an HttpOnly cookie managed by the browser. On a page load,
// bootstrapAuth() in services/api.ts silently exchanges the cookie for a new
// in-memory access token before the route guard makes a decision.
export const useAuthStore = create<AuthState>()((set) => ({
  accessToken: null,
  user: null,
  isAuthenticated: false,
  isHydrated: false,

  setAccessToken: (accessToken) => set({ accessToken, isAuthenticated: true }),
  setUser: (user) => set({ user }),
  setHydrated: (isHydrated) => set({ isHydrated }),

  logout: () =>
    set({
      accessToken: null,
      user: null,
      isAuthenticated: false,
    }),
}));
