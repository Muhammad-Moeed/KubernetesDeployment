"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useAuth } from "@/contexts/auth-context";
import { apiClient } from "@/lib/api-client";
import { Task, TaskCreateRequest, TaskUpdateRequest } from "@/types/task";
import { TaskList } from "@/components/tasks/task-list";
import { AddTaskModal } from "@/components/tasks/add-task-modal";
import { DeleteConfirmDialog } from "@/components/tasks/delete-confirm-dialog";
import { SearchBar } from "@/components/tasks/search-bar";
import { FilterBar } from "@/components/tasks/filter-bar";
import { SortDropdown } from "@/components/tasks/sort-dropdown";
import { ActiveFilters } from "@/components/tasks/active-filters";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { useTaskQuery } from "@/hooks/use-task-query";

export default function TasksPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);
  const { queryParams, updateQuery, clearFilters, clearFilter } = useTaskQuery();
  const loadingRef = useRef(false);
  const lastQueryRef = useRef<string>("");

  const loadTasks = useCallback(async () => {
    if (!user?.id || loadingRef.current) return;

    // Create a string key from query params to detect actual changes
    const queryKey = JSON.stringify({
      userId: user.id,
      status: queryParams.status,
      priority: queryParams.priority,
      search: queryParams.search,
      sort: queryParams.sort,
      order: queryParams.order,
    });

    // Skip if query hasn't actually changed
    if (lastQueryRef.current === queryKey) return;
    lastQueryRef.current = queryKey;

    loadingRef.current = true;
    try {
      setIsLoading(true);
      console.log("Loading tasks for user:", user.id, "with params:", queryParams);
      const fetchedTasks = await apiClient.getTasks(user.id, queryParams);
      console.log("Fetched tasks count:", fetchedTasks?.length || 0, fetchedTasks);
      setTasks(fetchedTasks || []);
    } catch (error: any) {
      console.error("Failed to load tasks:", error);
      console.error("Error details:", {
        message: error?.message,
        user_id: user.id,
        queryParams,
      });
      // Set empty array on error so user knows something went wrong
      setTasks([]);
    } finally {
      setIsLoading(false);
      loadingRef.current = false;
    }
  }, [user?.id, queryParams]);

  useEffect(() => {
    if (user?.id) {
      loadTasks();
    }
  }, [user?.id, loadTasks]);

  const handleSaveTask = async (data: TaskCreateRequest | TaskUpdateRequest) => {
    if (!user) return;

    try {
      if (editingTask) {
        // Update existing task
        const updatedTask = await apiClient.updateTask(
          user.id,
          editingTask.id,
          data as TaskUpdateRequest
        );
        setTasks(
          tasks.map((task) => (task.id === updatedTask.id ? updatedTask : task))
        );
        setEditingTask(null);
      } else {
        // Create new task
        const newTask = await apiClient.createTask(user.id, data as TaskCreateRequest);
        setTasks([newTask, ...tasks]);
      }
    } catch (error) {
      console.error("Failed to save task:", error);
      throw error;
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    if (!user) return;

    // Find the task to get current state
    const currentTask = tasks.find((t) => t.id === taskId);
    if (!currentTask) {
      console.error("Task not found:", taskId);
      return;
    }

    // Save original state for potential revert
    const originalTasks = [...tasks];

    // Optimistic update - update UI immediately
    const optimisticUpdate = tasks.map((task) =>
      task.id === taskId ? { ...task, completed: !task.completed } : task
    );
    setTasks(optimisticUpdate);

    try {
      console.log("Toggling task completion:", taskId, "for user:", user.id);
      const updatedTask = await apiClient.toggleTaskComplete(user.id, taskId);
      console.log("Task updated:", updatedTask);
      
      // Update with server response (more reliable than optimistic update)
      setTasks((prevTasks) =>
        prevTasks.map((task) => (task.id === updatedTask.id ? updatedTask : task))
      );
    } catch (error: any) {
      console.error("Failed to toggle task completion:", error);
      console.error("Error details:", {
        message: error?.message,
        taskId,
        userId: user.id,
      });
      
      // Revert optimistic update on error
      setTasks(originalTasks);
    }
  };

  const handleDeleteTask = async () => {
    if (!user || !deletingTask) return;

    try {
      await apiClient.deleteTask(user.id, deletingTask.id);
      setTasks(tasks.filter((task) => task.id !== deletingTask.id));
      setDeletingTask(null);
    } catch (error) {
      console.error("Failed to delete task:", error);
    }
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingTask(null);
  };

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Tasks
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              {tasks.length} {tasks.length === 1 ? "task" : "tasks"}
            </p>
          </div>
          <button
            onClick={() => setIsModalOpen(true)}
            className="px-6 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors flex items-center gap-2"
          >
            <span className="text-xl">+</span>
            Add Task
          </button>
        </div>

        {/* Search and Filters */}
        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-4 mb-6 space-y-4">
          <SearchBar
            onSearch={(query) => updateQuery({ search: query || undefined })}
            placeholder="Search tasks by title or description..."
          />

          <div className="grid md:grid-cols-2 gap-4">
            <FilterBar
              status={queryParams.status || "all"}
              priority={queryParams.priority || ""}
              onStatusChange={(status) => updateQuery({ status })}
              onPriorityChange={(priority) =>
                updateQuery({
                  priority: priority ? (priority as "high" | "medium" | "low") : undefined
                })
              }
            />

            <SortDropdown
              sortBy={queryParams.sort || "created_at"}
              order={queryParams.order || "desc"}
              onSortChange={(sort) => updateQuery({ sort })}
              onOrderChange={(order) => updateQuery({ order })}
            />
          </div>

          <ActiveFilters
            filters={{
              status: queryParams.status !== "all" ? queryParams.status : undefined,
              priority: queryParams.priority,
              search: queryParams.search,
            }}
            onClearFilter={clearFilter}
            onClearAll={clearFilters}
          />
        </div>

        <TaskList
          tasks={tasks}
          isLoading={isLoading}
          onToggleComplete={handleToggleComplete}
          onEdit={handleEdit}
          onDelete={setDeletingTask}
        />

        <AddTaskModal
          isOpen={isModalOpen}
          onClose={handleCloseModal}
          onSave={handleSaveTask}
          editTask={editingTask}
        />

        <DeleteConfirmDialog
          isOpen={!!deletingTask}
          onClose={() => setDeletingTask(null)}
          onConfirm={handleDeleteTask}
          taskTitle={deletingTask?.title || ""}
        />
      </div>
    </DashboardLayout>
  );
}
