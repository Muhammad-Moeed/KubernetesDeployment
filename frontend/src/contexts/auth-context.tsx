"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { User, UserSession } from "@/types/user";
import { apiClient } from "@/lib/api-client";

interface AuthContextType {
  user: User | null;
  session: UserSession | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<UserSession | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const savedSession = localStorage.getItem("session");
        if (savedSession) {
          const parsedSession: UserSession = JSON.parse(savedSession);

          if (new Date(parsedSession.expiresAt) > new Date()) {
            setSession(parsedSession);
            setUser(parsedSession.user);

            if (typeof document !== "undefined") {
              document.cookie = `better-auth.session_token=${parsedSession.token}; path=/; max-age=${7 * 24 * 60 * 60}`;
              document.cookie = `user-id=${parsedSession.user.id}; path=/; max-age=${7 * 24 * 60 * 60}`;
            }
          } else {
            localStorage.removeItem("session");
          }
        }
      } catch (error) {
        console.error("Failed to restore session:", error);
        localStorage.removeItem("session");
      } finally {
        setIsLoading(false);
      }
    };

    checkSession();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      // Get or create user_id for this email
      const usersMap = JSON.parse(localStorage.getItem("users_map") || "{}");
      let userId = usersMap[email];
      
      if (!userId) {
        // Create new user_id only if email doesn't exist
        userId = "user_" + Date.now();
        usersMap[email] = userId;
        localStorage.setItem("users_map", JSON.stringify(usersMap));
        console.log("✨ Created new user_id for", email, "→", userId);
      } else {
        console.log("🔄 Reusing existing user_id for", email, "→", userId);
      }
      
      const mockSession: UserSession = {
        user: {
          id: userId,  // Use consistent user_id
          email,
          createdAt: new Date().toISOString(),
        },
        token: "mock_token_" + Date.now(),
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
      };

      localStorage.setItem("session", JSON.stringify(mockSession));
      console.log("💾 Session saved with user_id:", userId);

      if (typeof document !== "undefined") {
        document.cookie = `better-auth.session_token=${mockSession.token}; path=/; max-age=${7 * 24 * 60 * 60}`;
        document.cookie = `user-id=${mockSession.user.id}; path=/; max-age=${7 * 24 * 60 * 60}`;
      }

      // Clear token cache to get fresh token
      apiClient.clearTokenCache();

      setSession(mockSession);
      setUser(mockSession.user);
    } catch (error) {
      console.error("Login failed:", error);
      throw new Error("Login failed");
    }
  };

  const signup = async (
    email: string,
    password: string,
    name?: string
  ) => {
    try {
      // Get or create user_id for this email
      const usersMap = JSON.parse(localStorage.getItem("users_map") || "{}");
      let userId = usersMap[email];
      
      if (!userId) {
        // Create new user_id for signup
        userId = "user_" + Date.now();
        usersMap[email] = userId;
        localStorage.setItem("users_map", JSON.stringify(usersMap));
        console.log("✨ Created new user_id for signup:", email, "→", userId);
      } else {
        console.log("🔄 User already exists, reusing user_id:", userId);
      }
      
      const mockSession: UserSession = {
        user: {
          id: userId,  // Use consistent user_id
          email,
          name, // ✅ name properly stored
          createdAt: new Date().toISOString(),
        },
        token: "mock_token_" + Date.now(),
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
      };

      localStorage.setItem("session", JSON.stringify(mockSession));
      console.log("💾 Signup session saved with user_id:", userId);

      if (typeof document !== "undefined") {
        document.cookie = `better-auth.session_token=${mockSession.token}; path=/; max-age=${7 * 24 * 60 * 60}`;
        document.cookie = `user-id=${mockSession.user.id}; path=/; max-age=${7 * 24 * 60 * 60}`;
      }

      // Clear token cache to get fresh token
      apiClient.clearTokenCache();

      setSession(mockSession);
      setUser(mockSession.user);
    } catch (error) {
      console.error("Signup failed:", error);
      throw new Error("Signup failed");
    }
  };

  const logout = async () => {
    try {
      // Only remove session, keep users_map for future logins
      localStorage.removeItem("session");
      console.log("👋 Logout: Session removed, users_map preserved");

      if (typeof document !== "undefined") {
        document.cookie = "better-auth.session_token=; path=/; max-age=0";
        document.cookie = "user-id=; path=/; max-age=0";
      }

      // Clear token cache on logout
      apiClient.clearTokenCache();

      setSession(null);
      setUser(null);
    } catch (error) {
      console.error("Logout failed:", error);
      throw new Error("Logout failed");
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        session,
        isLoading,
        isAuthenticated: !!user,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
