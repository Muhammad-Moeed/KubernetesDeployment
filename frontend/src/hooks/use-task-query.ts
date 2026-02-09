import { useState, useCallback, useMemo } from "react";
import { TaskQueryParams } from "@/types/task";

export function useTaskQuery() {
  const [queryParamsState, setQueryParamsState] = useState<TaskQueryParams>({
    status: "all",
    priority: undefined,
    search: undefined,
    sort: "created_at",
    order: "desc",
  });

  // Memoize queryParams to prevent unnecessary re-renders
  const queryParams = useMemo(() => queryParamsState, [
    queryParamsState.status,
    queryParamsState.priority,
    queryParamsState.search,
    queryParamsState.sort,
    queryParamsState.order,
  ]);

  const updateQuery = useCallback((updates: Partial<TaskQueryParams>) => {
    setQueryParamsState((prev) => ({ ...prev, ...updates }));
  }, []);

  const clearFilters = useCallback(() => {
    setQueryParamsState({
      status: "all",
      priority: undefined,
      search: undefined,
      sort: "created_at",
      order: "desc",
    });
  }, []);

  const clearFilter = useCallback((key: string) => {
    setQueryParamsState((prev) => ({
      ...prev,
      [key]: key === "status" ? "all" : undefined,
    }));
  }, []);

  return {
    queryParams,
    updateQuery,
    clearFilters,
    clearFilter,
  };
}
