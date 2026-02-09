import { Task, TaskCreateRequest, TaskUpdateRequest, TaskQueryParams } from "@/types/task";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private baseUrl: string;
  private tokenCache: { token: string | null; expiresAt: number } | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async getAuthToken(): Promise<string | null> {
    // Check if we have a cached token that's still valid
    if (this.tokenCache && this.tokenCache.expiresAt > Date.now()) {
      return this.tokenCache.token;
    }

    // Clear expired cache
    this.tokenCache = null;
    
    if (typeof window === "undefined") return null;

    try {
      // Get session from localStorage (mock auth)
      const savedSession = localStorage.getItem("session");
      if (!savedSession) {
        return null;
      }

      const session = JSON.parse(savedSession);
      const userId = session?.user?.id;
      const userEmail = session?.user?.email;

      if (!userId) {
        console.warn("⚠️ No user_id in session");
        return null;
      }
      
      console.log("🔑 Getting JWT token for:", userEmail, "user_id:", userId);

      // Get JWT token from bridge endpoint with user ID
      const response = await fetch("/api/auth/jwt-token", {
        method: "GET",
        headers: {
          "x-user-id": userId,
        },
        credentials: "include",
      });
      
      if (response.ok) {
        const data = await response.json();
        const token = data?.token || null;
        
        // Cache the token (expires in 23 hours to be safe)
        if (token) {
          this.tokenCache = {
            token,
            expiresAt: Date.now() + (23 * 60 * 60 * 1000), // 23 hours
          };
        }
        
        return token;
      }
      
      // If 401, user is not authenticated
      if (response.status === 401) {
        return null;
      }
      
      // For other errors, log but don't throw
      if (!response.ok) {
        console.warn("Failed to get JWT token:", response.status);
        return null;
      }
    } catch (error) {
      // Silently fail - no session available
      console.warn("Error getting JWT token:", error);
      return null;
    }
    return null;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getAuthToken();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
      console.log("API Request:", endpoint, "with token:", token.substring(0, 20) + "...");
    } else {
      console.warn("API Request without token:", endpoint);
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
      credentials: "include", // Include cookies for Better Auth session
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: "Request failed" }));
      const errorMessage = error.error || error.detail?.error || `HTTP ${response.status}: ${response.statusText}`;
      
      // Log detailed error for debugging
      console.error(`API Error [${response.status}]:`, {
        endpoint,
        status: response.status,
        error: errorMessage,
        details: error.detail,
      });
      
      throw new Error(errorMessage);
    }

    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  // Task API methods
  async getTasks(userId: string, params?: TaskQueryParams): Promise<Task[]> {
    console.log("📋 Fetching tasks for user_id:", userId);
    
    // Build query string, filtering out undefined/null values and "all" status
    const queryParams: Record<string, string> = {};
    
    if (params) {
      // Only include status if it's not "all"
      if (params.status && params.status !== "all") {
        queryParams.status = params.status;
      }
      if (params.priority) {
        queryParams.priority = params.priority;
      }
      if (params.search) {
        queryParams.search = params.search;
      }
      if (params.sort) {
        queryParams.sort = params.sort;
      }
      if (params.order) {
        queryParams.order = params.order;
      }
    }
    
    const queryString = Object.keys(queryParams).length > 0
      ? "?" + new URLSearchParams(queryParams).toString()
      : "";
    
    const tasks = await this.request<Task[]>(`/api/${userId}/tasks${queryString}`);
    console.log("✅ Fetched", tasks.length, "tasks from database for user_id:", userId);
    return tasks;
  }

  async getTask(userId: string, taskId: number): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`);
  }

  async createTask(userId: string, data: TaskCreateRequest): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async updateTask(
    userId: string,
    taskId: number,
    data: TaskUpdateRequest
  ): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async toggleTaskComplete(userId: string, taskId: number): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
  }

  async deleteTask(userId: string, taskId: number): Promise<void> {
    return this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  }

  clearTokenCache(): void {
    console.log("🗑️ Clearing token cache");
    this.tokenCache = null;
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
