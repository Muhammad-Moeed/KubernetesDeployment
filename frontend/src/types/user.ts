export interface User {
  id: string;
  email: string;
  name?: string;
  avatar?: string;
  createdAt: string;
}

export interface UserSession {
  user: User;
  token: string;
  expiresAt: string;
}

export interface UserPreferences {
  theme: "light" | "dark";
  language: "en" | "ur";
}
