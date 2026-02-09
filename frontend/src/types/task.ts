export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: "high" | "medium" | "low";
  tags: string[] | null;
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  priority?: "high" | "medium" | "low";
  tags?: string[];
  due_date?: string;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  priority?: "high" | "medium" | "low";
  tags?: string[];
  due_date?: string;
  completed?: boolean;
}

export interface TaskQueryParams {
  status?: "all" | "pending" | "completed";
  priority?: "high" | "medium" | "low";
  tag?: string;
  search?: string;
  sort?: "due_date" | "priority" | "created_at";
  order?: "asc" | "desc";
  due_before?: string;
}
